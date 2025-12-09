# AGENTS.md — Implementation Shards

> **Step-by-step build guides for the Content Repurposing Engine**

---

## Package Identity

This directory contains 13 sequential implementation shards that guide you through building the complete Content Repurposing Engine. Each shard is self-contained with explicit tasks, verification steps, and acceptance criteria.

**Total Estimated Time:** 8-12 hours

---

## Shard Execution Rules

### ✅ MUST

1. **Execute shards in order** — Dependencies are critical
2. **Check off tasks** as you complete them
3. **Run verification steps** before proceeding
4. **Troubleshoot blockers** before moving to next shard
5. **Refer to parent docs** when shard references `voice-dna-framework.md` or `technical-requirements-spec.md`

### ❌ DON'T

1. Skip shards (even if they seem optional)
2. Proceed if verification fails
3. Execute shards 07-09 before shard 06 is complete
4. Skip the quality gate (shard-10) — it's what differentiates this from generic AI content

---

## Shard Dependency Graph

```
[01] Hostinger VPS Setup
       │
       ▼
[02] n8n Installation ─────────┐
       │                       │
       ▼                       │
[03] Google Credentials        │
       │                       │
       ▼                       │
[04] Google Sheets Structure   │
       │                       │
       ▼                       │
[05] Core Ingestion            │
       │                       │
       ▼                       │
[06] Idea Extraction ──────────┼────────────┐
       │                       │            │
       ├───────┬───────┐       │            │
       ▼       ▼       ▼       │            │
    [07]    [08]    [09]       │            │
  Twitter LinkedIn Newsletter   │            │
       │       │       │       │            │
       └───────┴───────┘       │            │
               │               │            │
               ▼               │            │
[10] Quality Gate ◀────────────┘            │
       │                                    │
       ▼                                    │
[11] Testing & Refinement                   │
       │                                    │
       ▼                                    │
[12] Demo Assets ◀──────────────────────────┘
```

---

## Quick Navigation

| Day | Shards | Focus Area             |
| --- | ------ | ---------------------- |
| 1   | 01-03  | Infrastructure         |
| 2   | 04-06  | Foundation & Ingestion |
| 3   | 07-09  | Content Generation     |
| 4   | 10-11  | Quality & Testing      |
| 5   | 12     | Demo & Submission      |

---

## Shard File Format

Each shard follows this structure:

```markdown
# Shard NN: Title

**Est. Time:** X min | **Depends on:** Shard NN | **Outcome:** Description

---

## Part A: First Section

### N.1 First Task

- [ ] Step 1
- [ ] Step 2

### N.2 Second Task

...

---

## Verification

- [ ] Check 1
- [ ] Check 2
```

---

## JIT Index Hints

```bash
# List all shards in order
ls -1 shard-*.md

# Find a specific task
rg -n "TASK" shard-*.md

# Find verification steps
rg -n "Verification" shard-*.md

# Check which shard mentions a topic
rg -n "Gemini" shard-*.md

# View shard dependencies
rg -n "Depends on" shard-*.md
```

---

## Common Gotchas

1. **Shard 01 (Hostinger)**: VPS provisioning can take 5-10 minutes
2. **Shard 03 (Google Credentials)**: Both Gemini API key AND Sheets OAuth2 required
3. **Shard 06 (Idea Extraction)**: This is the foundation — all platform generators depend on it
4. **Shards 07-09**: Can be done in parallel if sufficient time, but test each independently
5. **Shard 10 (Quality Gate)**: Don't skip refinement logic — it's what prevents AI slop
6. **Shard 12 (Demo)**: Record on production (Hostinger) not local for submission proof

---

## Cross-References

- **Voice DNA Prompts**: `../voice-dna-framework.md`
- **Technical Specs**: `../technical-requirements-spec.md`
- **Submission Checklist**: `../submission-requirements.md`
- **Project Overview**: `../../AGENTS.md`
