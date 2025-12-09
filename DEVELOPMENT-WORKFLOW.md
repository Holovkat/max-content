# Development Workflow Guide

## Content Repurposing Engine

**IMPORTANT:** This project follows the Graphite Stacking Workflow. All changes must go through the proper branch → PR → UAT → approval → squash merge process.

---

## ⚠️ MANDATORY REQUIREMENTS

| Rule           | Requirement                                              |
| -------------- | -------------------------------------------------------- |
| **Merge Type** | **ALWAYS use squash merge** — no exceptions              |
| **Rebasing**   | **MUST rebase regularly** — keep stack in sync with main |
| **PR Size**    | Small, focused — ONE shard per PR                        |
| **Approval**   | Tony must UAT and approve before merge                   |

---

## Execution Order

### Phase 1: Code-First (No VPS Yet)

We complete ALL n8n workflow code and configurations locally/in repo before touching VPS:

| Step | Shard | Branch Name                      | Description                       |
| ---- | ----- | -------------------------------- | --------------------------------- |
| 1    | 04    | `shard/04-sheets-structure`      | Google Sheets schema definition   |
| 2    | 05    | `shard/05-core-ingestion`        | n8n workflow JSON for ingestion   |
| 3    | 06    | `shard/06-idea-extraction`       | Gemini prompts + code nodes       |
| 4    | 07    | `shard/07-twitter-generation`    | Twitter generation prompts        |
| 5    | 08    | `shard/08-linkedin-generation`   | LinkedIn generation prompts       |
| 6    | 09    | `shard/09-newsletter-generation` | Newsletter generation prompts     |
| 7    | 10    | `shard/10-quality-gate`          | Quality scoring + refinement      |
| 8    | 13    | `shard/13-custom-ui`             | Optional web UI (if time permits) |

### Phase 2: Infrastructure (With Tony)

After code is approved, Tony walks through infrastructure setup:

| Step | Shard | Description                                   |
| ---- | ----- | --------------------------------------------- |
| 9    | 01    | Hostinger VPS provisioning (manual with Tony) |
| 10   | 02    | n8n Docker installation (manual with Tony)    |
| 11   | 03    | Google credentials setup (manual with Tony)   |
| 12   | 11    | Import workflow, testing, refinement          |
| 13   | 12    | Demo video + submission                       |

---

## Per-Shard Workflow

For each code shard, follow this process:

### 1. Create Branch

```bash
git fetch origin
git checkout -b shard/XX-name origin/main
# OR if stacking:
git checkout -b shard/XX-name shard/XX-1-previous-name
```

### 2. Implement Changes

- Create/modify files as specified in shard
- Commit with clear messages:
  ```bash
  git add .
  git commit -m "feat(shard-XX): description of change"
  ```

### 3. Push & Create PR

```bash
git push origin shard/XX-name
gh pr create --base main --title "Shard XX: Name"
```

### 4. UAT Instructions

After implementation, provide Tony with:

- What was built
- How to verify/test
- Expected outcomes
- Files to review

### 5. Tony Reviews & Approves

Tony reviews code and either:

- ✅ Approves → proceed to step 6
- 🔄 Requests changes → implement and repeat from step 2

### 6. Update Documentation

After approval, before merge:

- Update any relevant docs
- Add notes to shard file if needed
- Commit documentation updates

### 7. Squash Merge

```bash
gh pr merge <PR_NUMBER> --squash --delete-branch
git checkout main
git pull origin main
```

### 8. Rebase Next Branch (if stacking)

```bash
git checkout shard/XX+1-next-name
git rebase origin/main
git push --force-with-lease
```

---

## File Structure for n8n Export

Since we can't run n8n locally, we'll store:

```
/n8n-workflows/
├── workflow-content-repurposing-engine.json  (exportable n8n workflow)
├── prompts/
│   ├── idea-extraction.md
│   ├── twitter-generation.md
│   ├── linkedin-generation.md
│   ├── newsletter-generation.md
│   └── quality-critique.md
└── code-nodes/
    ├── parse-ideas.js
    ├── parse-tweets.js
    ├── parse-linkedin.js
    ├── parse-newsletter.js
    └── parse-quality.js
```

This allows us to:

- Version control all prompts and code
- Review changes in PRs
- Import into n8n once VPS is ready

---

## Reference

Full workflow documentation:
`/Users/tonyholovka/workspace/designs/templates/instructional-documents/github-workflow.md`

---

_All code changes must follow this workflow without exception._
