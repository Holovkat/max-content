# 🎬 Content Repurposing Engine

> **Hostinger x n8n Hackathon – Content Management Build**  
> Transform long-form video transcripts into platform-ready social content.

[![Deadline](https://img.shields.io/badge/Deadline-December%2014%2C%202024-red)]()
[![Platform](https://img.shields.io/badge/Platform-n8n-orange)]()
[![Hosting](https://img.shields.io/badge/Hosting-Hostinger%20VPS-blue)]()
[![Workflow](https://img.shields.io/badge/Git-Graphite%20Stacking-purple)]()

---

## ⚠️ Git Workflow (Mandatory)

> **ALL changes MUST use the Graphite stacking workflow. No direct commits to main.**

| Rule            | Requirement                         |
| --------------- | ----------------------------------- |
| **Main Branch** | ❌ **NEVER** commit directly        |
| **Merge Type**  | ✅ **ALWAYS squash merge**          |
| **Rebasing**    | ✅ Keep stack in sync with main     |
| **PR Size**     | Small, focused — ONE logical change |

```bash
# Quick workflow
git checkout -b feature/your-change origin/main
# ... make changes ...
git push origin feature/your-change
gh pr create --base main --title "feat: description"
gh pr merge <PR_NUMBER> --squash --delete-branch
```

See [AGENTS.md](AGENTS.md) for full workflow documentation.

---

## 🚀 What It Does

The **Content Repurposing Engine** takes a single long-form video transcript and automatically generates **platform-ready posts** for:

- 💼 **LinkedIn** – Professional posts (150-300+ words)
- 🐦 **X/Twitter** – Punchy tweets and threads
- 📸 **Instagram** – Emotionally-driven captions
- 🎓 **Skool** – Community engagement posts
- 📧 **Newsletter** – Summary sections with CTAs

Every piece of content follows the **Hook → Value → CTA** structure to maximize engagement while avoiding generic "AI slop."

---

## 🏗️ Architecture

```
Transcript → n8n Workflow → LLM Processing → Multi-Platform Content → Storage
```

| Component         | Local Dev            | Production           |
| ----------------- | -------------------- | -------------------- |
| **Orchestration** | n8n (Docker Desktop) | n8n (self-hosted)    |
| **Hosting**       | localhost:5678       | Hostinger VPS (KVM2) |
| **AI/LLM**        | Google Gemini Flash  | Google Gemini Flash  |
| **Storage**       | Google Sheets        | Google Sheets        |

> 💰 **Zero-cost stack**: Gemini Flash free tier (1M tokens/day) + Google Sheets (free)

---

## 📁 Project Structure

```
max-content/
├── AGENTS.md                    # AI agent guidelines & quick reference
├── README.md                    # This file
├── features/
│   ├── prd.md                   # Product Requirements Document
│   ├── technical-requirements-spec.md  # Full technical architecture
│   ├── voice-dna-framework.md   # LLM prompts & voice calibration
│   ├── submission-requirements.md  # Hackathon checklist
│   ├── implementation-shards/   # 13 step-by-step build guides
│   │   ├── shard-00-overview.md     # Execution plan
│   │   ├── shard-01-hostinger-setup.md
│   │   ├── shard-02-n8n-setup.md
│   │   ├── shard-03 to 12...        # Infrastructure to Demo
│   │   └── shard-12-demo-assets.md  # Final submission
│   └── sprint-artifacts/        # Sprint deliverables
├── .agent/workflows/bmad/       # BMAD workflow definitions
└── .bmad/                       # BMAD configuration
```

---

## 📋 Implementation Roadmap

> **Local-first development** → Deploy to Hostinger for final submission

| Phase | Description                             | Environment | Status |
| ----- | --------------------------------------- | ----------- | ------ |
| 1️⃣    | Local Setup (Docker Desktop + n8n)      | 🏠 Local    | 🔲     |
| 2️⃣    | Minimal Viable Workflow (LinkedIn only) | 🏠 Local    | 🔲     |
| 3️⃣    | Multi-Platform Expansion                | 🏠 Local    | 🔲     |
| 4️⃣    | Quality Layer (LLM review)              | 🏠 Local    | 🔲     |
| 5️⃣    | Polish & Observability                  | 🏠 Local    | 🔲     |
| 6️⃣    | **Deploy to Hostinger VPS**             | ☁️ Prod     | 🔲     |
| 7️⃣    | Demo & Submission                       | ☁️ Prod     | 🔲     |

---

## 🎯 Hackathon Deliverables

- [ ] n8n workflows deployed on Hostinger VPS
- [ ] Data storage with sample output posts
- [ ] **1-2 minute demo video**
- [ ] **100-300 word write-up**
- [ ] (Optional) Simple input UI

---

## 📖 Documentation

| Document                                                                     | Description                               |
| ---------------------------------------------------------------------------- | ----------------------------------------- |
| [AGENTS.md](AGENTS.md)                                                       | AI agent guidelines & quick reference     |
| [PRD](features/prd.md)                                                       | Full Product Requirements                 |
| [Technical Spec](features/technical-requirements-spec.md)                    | Architecture, data flow, success criteria |
| [Voice DNA Framework](features/voice-dna-framework.md)                       | LLM prompts & voice calibration           |
| [Implementation Shards](features/implementation-shards/shard-00-overview.md) | Step-by-step build guide (13 shards)      |
| [Submission Checklist](features/submission-requirements.md)                  | Pre-submission verification               |

---

## 🔧 Getting Started

### Prerequisites

- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running
- LLM API key (OpenAI/Gemini/Anthropic)
- Data storage account (Airtable/Notion/Sheets)
- (For deployment) Hostinger VPS (KVM2)

### Local Development Setup

```bash
# Quick start with Docker
docker run -d --name n8n-local -p 5678:5678 -v ~/.n8n:/home/node/.n8n n8nio/n8n

# Access n8n at http://localhost:5678

# Or use Docker Compose (see AGENTS.md for full config)
docker-compose up -d
```

### BMAD Workflows

This project uses [BMAD Method](https://github.com/bmad-code-org/BMAD-METHOD) for project management:

```bash
# Initialize project workflow
/workflow-init

# Check status
/workflow-status

# Create development story
/create-story
```

---

## 📝 Content Quality Standards

Every generated post must:

✅ Have a **clear hook** (1-2 sentences)  
✅ Deliver **concrete value** (specific insights, not vague advice)  
✅ End with a **natural CTA** (platform-appropriate)  
✅ Be something a creator would **actually post**

❌ No generic filler ("In today's fast-paced world...")  
❌ No repetitive patterns  
❌ No obvious AI-generated language

---

## ⏰ Deadline

**December 14, 2024 – 11:59 PM EST**

Submit via Skool → Hostinger Hackathon category → Official submission form.

---

## 📄 License

MIT License – Built for the Hostinger x n8n Hackathon
