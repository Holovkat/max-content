# AGENTS.md — Content Repurposing Engine

> **Hostinger x n8n Hackathon – Content Management Build**  
> Deadline: **December 14, 11:59 PM EST**

---

## ⚠️ MANDATORY: Git Workflow Requirements

> **ALL CHANGES MUST USE THE GRAPHITE STACKING WORKFLOW**

| Rule                       | Requirement                                              |
| -------------------------- | -------------------------------------------------------- |
| **Direct Commits to Main** | ❌ **NEVER** — all changes via PRs only                  |
| **Merge Type**             | **ALWAYS squash merge** — no exceptions                  |
| **Rebasing**               | **MUST rebase regularly** — keep stack in sync with main |
| **PR Size**                | Small, focused — ONE logical change per PR               |
| **Tooling**                | Use `gh pr merge --squash --delete-branch`               |

**Violation of these rules is not acceptable. All PRs that do not follow this workflow will be rejected.**

### Quick Reference: Stacking Workflow

```bash
# 1. Create first branch from main
git fetch origin
git checkout -b feature/part-1-setup origin/main
# ... make changes ...
git add . && git commit -m "feat: description"
git push origin feature/part-1-setup
gh pr create --base main --title "Part 1: Setup"

# 2. Stack next branch FROM previous (not main!)
git checkout -b feature/part-2-implementation
# ... make changes ...
git add . && git commit -m "feat: description"
git push origin feature/part-2-implementation
gh pr create --base feature/part-1-setup --title "Part 2: Implementation"

# 3. Merge bottom-up with squash
gh pr merge <PR_NUMBER> --squash --delete-branch
git fetch origin
git checkout feature/part-2-implementation
git rebase origin/main
git push --force-with-lease
gh pr edit <pr-number> --base main
```

**Full workflow documentation**: See [`github-workflow.md`](https://github.com/...) or project templates.

---

## Project Snapshot

- **Type**: n8n workflow automation project (not a traditional codebase)
- **Stack**: n8n + Docker Desktop (local) → Hostinger VPS (production) + LLM APIs + Airtable/Sheets
- **Goal**: Convert long-form video transcripts → platform-ready social content
- **Phase**: Planning & Documentation (PRD complete, implementation pending)
- **Development**: **Local-first** with Docker Desktop, then deploy to Hostinger
- **Status Tracking**: See `features/` for PRD and submission checklist

---

## Directory Map (JIT Index)

### Core Documentation

| Path                                      | Purpose                                       |
| ----------------------------------------- | --------------------------------------------- |
| `features/prd.md`                         | Full Product Requirements Document            |
| `features/technical-requirements-spec.md` | Technical architecture & implementation specs |
| `features/voice-dna-framework.md`         | LLM prompt templates & voice calibration      |
| `features/submission-requirements.md`     | Hackathon submission checklist                |
| `features/sprint-artifacts/`              | Sprint-related deliverables                   |

### Implementation Shards (Execute in Order)

| Shard | File                                                               | Purpose                   | Est. Time |
| ----- | ------------------------------------------------------------------ | ------------------------- | --------- |
| 00    | `features/implementation-shards/shard-00-overview.md`              | Overview & execution plan | -         |
| 01    | `features/implementation-shards/shard-01-hostinger-setup.md`       | VPS provisioning          | 30-45 min |
| 02    | `features/implementation-shards/shard-02-n8n-setup.md`             | n8n installation          | 20-30 min |
| 03    | `features/implementation-shards/shard-03-google-credentials.md`    | API credentials           | 30-45 min |
| 04    | `features/implementation-shards/shard-04-sheets-structure.md`      | Google Sheets setup       | 15-20 min |
| 05    | `features/implementation-shards/shard-05-core-ingestion.md`        | Transcript ingestion      | 30-45 min |
| 06    | `features/implementation-shards/shard-06-idea-extraction.md`       | LLM idea extraction       | 30-45 min |
| 07    | `features/implementation-shards/shard-07-twitter-generation.md`    | Twitter content gen       | 30-45 min |
| 08    | `features/implementation-shards/shard-08-linkedin-generation.md`   | LinkedIn content gen      | 30-45 min |
| 09    | `features/implementation-shards/shard-09-newsletter-generation.md` | Newsletter gen            | 30-45 min |
| 10    | `features/implementation-shards/shard-10-quality-gate.md`          | Quality scoring system    | 45-60 min |
| 11    | `features/implementation-shards/shard-11-testing.md`               | Testing & validation      | 60-90 min |
| 12    | `features/implementation-shards/shard-12-demo-assets.md`           | Demo video & submission   | 60-90 min |

### BMAD Configuration

| Path                       | Purpose                   |
| -------------------------- | ------------------------- |
| `.agent/workflows/bmad/`   | BMAD workflow definitions |
| `.bmad/`                   | BMAD configuration        |
| `bmad-custom-modules-src/` | Custom BMAD modules       |
| `bmad-custom-src/`         | BMAD customizations       |

### Sub-Directory AGENTS.md Files

For detailed guidance when working in specific directories:

- **Features documentation**: [`features/AGENTS.md`](features/AGENTS.md)
- **Implementation shards**: [`features/implementation-shards/AGENTS.md`](features/implementation-shards/AGENTS.md)

---

## n8n Workflow Architecture

### Core Workflows (to be built)

```
┌─────────────────────────────────────────────────────────────────┐
│                    TRANSCRIPT INPUT                              │
│  (Webhook / Manual trigger with video transcript + metadata)     │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              WORKFLOW A: Transcript_Ingestion                    │
│  • Receive transcript & metadata                                 │
│  • Store raw transcript in Airtable/Sheet                        │
│  • Trigger Content_Generation workflow                           │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              WORKFLOW B: Content_Generation                      │
│  • Chunk & extract key ideas (LLM call)                         │
│  • Generate platform-specific content:                          │
│    - LinkedIn: 150-300+ words, structured                       │
│    - X/Twitter: Short punchy posts, threads                     │
│    - Instagram: Emotional hooks with CTA                        │
│    - Skool: Informative posts with engagement questions         │
│    - Newsletter: Summary sections                               │
│  • Enforce Hook–Value–CTA structure                             │
│  • (Optional) Quality review pass                               │
│  • Persist to data storage                                       │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                     OUTPUT STORAGE                               │
│  Airtable / Notion / Google Sheets / PostgreSQL                  │
│  Fields: platform, post_type, hook, body, cta, topic, status     │
└─────────────────────────────────────────────────────────────────┘
```

---

## Content Structure Pattern

Every generated post MUST follow this structure:

| Component | Purpose                                     | Example                                  |
| --------- | ------------------------------------------- | ---------------------------------------- |
| **Hook**  | 1-2 sentences to capture attention          | "Most people misunderstand AI agents..." |
| **Value** | Detailed insight, how-to, or transformation | (Main content body)                      |
| **CTA**   | Natural, platform-appropriate action        | "Reply 'guide' for the PDF"              |

### Quality Criteria (Anti-Slop)

- ✅ Specific examples, not vague advice
- ✅ Niche-relevant content
- ✅ Clear, simple language
- ✅ Something a creator would actually post
- ❌ Generic filler ("In today's fast-paced world...")
- ❌ Repetitive structure across posts
- ❌ Obvious AI-generated patterns

### Voice DNA Framework

**Full Reference:** See [`features/voice-dna-framework.md`](features/voice-dna-framework.md)

| Voice Profile      | Liam Ottley / Morningside AI                              |
| ------------------ | --------------------------------------------------------- |
| **Energy**         | High-drive, urgent, building-while-speaking               |
| **Tone**           | Direct, practical, transparently ambitious                |
| **Style**          | Tutorial-meets-vlog, educational with real numbers        |
| **Evidence Style** | Numbers-forward ($100k, 60+ team, 1M views)               |
| **CTAs**           | Action-oriented: "Build your first AI agent this weekend" |

**Prompt Templates Available:**

- Idea Extraction Prompt
- Twitter Generation Prompt
- LinkedIn Generation Prompt
- Newsletter Generation Prompt
- Quality Critique Prompt
- Refinement Prompt

### Quality Gate Scoring

**Full Reference:** See [`features/technical-requirements-spec.md`](features/technical-requirements-spec.md#5-quality-gate-specification)

| Criterion              | Weight | Scoring Range |
| ---------------------- | ------ | ------------- |
| **Hook Clarity**       | 20%    | 1-5           |
| **Specificity**        | 20%    | 1-5           |
| **Voice Authenticity** | 20%    | 1-5           |
| **Value Density**      | 20%    | 1-5           |
| **CTA Naturalness**    | 20%    | 1-5           |

**Pass Thresholds:**

- Twitter: 16/25 minimum
- LinkedIn: 18/25 minimum
- Newsletter: 20/25 minimum

## Hackathon Requirements

### Judging Criteria

1. **Input**: Accept video transcript (long-form preferred)
2. **Output**: Multi-platform content with hook + value + CTA
3. **Quality**: No AI slop, niche-aligned, post-ready
4. **Infrastructure**: Self-hosted n8n on Hostinger VPS

### Deliverables

- [ ] n8n workflows deployed on Hostinger VPS
- [ ] Storage populated with sample outputs
- [ ] 1-2 minute demo video
- [ ] 100-300 word write-up
- [ ] (Optional) Simple input UI

---

## Local Development Environment

> **Build locally first, then deploy to Hostinger for final submission.**

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- LLM API key (OpenAI/Gemini/Anthropic)
- Data storage account (Airtable/Notion/Sheets)

### Local n8n Setup (Docker Desktop)

```bash
# Create local n8n instance with Docker
docker run -d \
  --name n8n-local \
  -p 5678:5678 \
  -v ~/.n8n:/home/node/.n8n \
  n8nio/n8n

# Access n8n at http://localhost:5678

# View logs
docker logs -f n8n-local

# Stop/Start
docker stop n8n-local
docker start n8n-local

# Remove (data persists in ~/.n8n)
docker rm n8n-local
```

### With Docker Compose (Recommended)

Create `docker-compose.yml`:

```yaml
version: "3.8"
services:
  n8n:
    image: n8nio/n8n
    container_name: n8n-local
    ports:
      - "5678:5678"
    volumes:
      - ~/.n8n:/home/node/.n8n
    environment:
      - N8N_BASIC_AUTH_ACTIVE=true
      - N8N_BASIC_AUTH_USER=admin
      - N8N_BASIC_AUTH_PASSWORD=changeme
    restart: unless-stopped
```

Then run:

```bash
docker-compose up -d
```

### Workflow Export/Import

```bash
# Export workflows from local for backup
# (Use n8n UI: Settings → Export All Workflows)

# Save exports to: features/sprint-artifacts/workflows/
```

---

## Implementation Phases

| Phase | Description                                    | Environment  | Status     |
| ----- | ---------------------------------------------- | ------------ | ---------- |
| 1     | Local Environment Setup (Docker Desktop + n8n) | 🏠 Local     | 🔲 Pending |
| 2     | Minimal Viable Workflow (LinkedIn only)        | 🏠 Local     | 🔲 Pending |
| 3     | Multi-Platform Expansion                       | 🏠 Local     | 🔲 Pending |
| 4     | Quality Layer (LLM review pass)                | 🏠 Local     | 🔲 Pending |
| 5     | Polish & Observability                         | 🏠 Local     | 🔲 Pending |
| 6     | **Pre-Release**: Deploy to Hostinger VPS       | ☁️ Hostinger | 🔲 Pending |
| 7     | Demo & Submission Assets                       | ☁️ Hostinger | 🔲 Pending |

### Deployment to Hostinger (Phase 6)

```bash
# 1. Provision Hostinger VPS (KVM2)
# 2. Install n8n via Hostinger one-click template or Docker Compose
# 3. Export workflows from local n8n
# 4. Import workflows to Hostinger n8n
# 5. Configure credentials (API keys) in Hostinger n8n
# 6. Test end-to-end on production
```

---

## Quick Commands

### Git Workflow (Mandatory)

```bash
# Create new branch for changes
git checkout -b feature/your-change origin/main

# After changes, push and create PR
git push origin feature/your-change
gh pr create --base main --title "feat: your description"

# Merge with squash (never regular merge)
gh pr merge <PR_NUMBER> --squash --delete-branch
```

### BMAD Workflows

```bash
# Initialize project workflow
/workflow-init

# Check workflow status
/workflow-status

# Create next story from epics
/create-story
```

### Search & Navigate

```bash
# Find in PRD
rg -n "PATTERN" features/prd.md

# Find in technical requirements spec
rg -n "PATTERN" features/technical-requirements-spec.md

# Find in voice DNA framework (prompts)
rg -n "PATTERN" features/voice-dna-framework.md

# Find across all implementation shards
rg -n "PATTERN" features/implementation-shards/

# Find specific shard by number
ls features/implementation-shards/shard-*.md

# Find submission requirements
rg -n "PATTERN" features/submission-requirements.md

# Find across all features documentation
rg -n "PATTERN" features/
```

---

## Security & Secrets

- **NEVER commit API keys** (OpenAI, Anthropic, etc.)
- Store credentials in n8n Credentials Manager (encrypted)
- Use environment variables on Hostinger VPS (not hardcoded in workflows)
- Keep `.env` files in `.gitignore`

---

## Definition of Done (Pre-Submission)

Before final submission, verify:

- [ ] Hostinger VPS is active with n8n accessible via HTTPS
- [ ] Both workflows run without errors
- [ ] At least one realistic transcript processed E2E
- [ ] Outputs stored with clear fields (platform, hook, body, CTA, status)
- [ ] Each post has clear hook, concrete value, natural CTA
- [ ] Demo video is 1-2 minutes, shows Hostinger proof
- [ ] Write-up is 100-300 words

---

## Resources

### Project Documentation

- **PRD**: [`features/prd.md`](features/prd.md)
- **Technical Spec**: [`features/technical-requirements-spec.md`](features/technical-requirements-spec.md)
- **Voice DNA Framework**: [`features/voice-dna-framework.md`](features/voice-dna-framework.md)
- **Submission Checklist**: [`features/submission-requirements.md`](features/submission-requirements.md)
- **Implementation Shards**: [`features/implementation-shards/`](features/implementation-shards/) (start with `shard-00-overview.md`)

### External Resources

- **Hackathon Info**: Hostinger x n8n Hackathon on Skool
- **n8n Docs**: https://docs.n8n.io/
- **Google AI Studio**: https://aistudio.google.com/
- **Google Sheets API**: https://developers.google.com/sheets/api
