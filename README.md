# 🎬 Max Content - AI-Powered Content Repurposing Engine

> **Hostinger x n8n Hackathon – Content Management Build**  
> Transform long-form content into platform-ready social posts with a single click.

[![Status](https://img.shields.io/badge/Status-Complete-brightgreen)]()
[![Platform](https://img.shields.io/badge/Platform-n8n-orange)]()
[![AI](https://img.shields.io/badge/AI-Google%20Gemini-blue)]()

> 🎬 **[Watch Demo Video](https://www.loom.com/share/8acb2b032a324820bd7aa5448af064ab)** - See the full workflow in action!

---

## 🚀 What It Does

**Max Content** takes your long-form content (YouTube transcripts, podcast notes, articles) and automatically generates **platform-ready posts** for:

| Platform          | Content Type                       | Publishing              |
| ----------------- | ---------------------------------- | ----------------------- |
| 🐦 **X/Twitter**  | Punchy tweets with hooks           | ✅ Auto-post            |
| 💼 **LinkedIn**   | Professional posts (150-300 words) | ✅ Auto-post            |
| 📧 **Newsletter** | Email with key takeaways           | ✅ Auto-send via Resend |
| 📸 **Instagram**  | Emotionally-driven captions        | 📋 Copy-ready           |
| 🎓 **Skool**      | Community discussion starters      | 📋 Copy-ready           |

Every piece of content follows the **Hook → Value → CTA** structure to maximize engagement.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    WEB FORM INPUT                                │
│  Submit: YouTube URL, transcript, or raw ideas + platforms      │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONTENT GENERATOR WORKFLOW                          │
│  • Parse input and extract content                               │
│  • Generate platform-specific content via Gemini                 │
│  • Build interactive preview page                                │
│  • Encode payload for approval                                   │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              PREVIEW & APPROVAL PAGE                             │
│  • Visual preview of all generated content                       │
│  • Platform indicators (will post / copy only)                   │
│  • One-click "Approve and Post" button                          │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONTENT APPROVAL WORKFLOW                           │
│  • Decode payload and parse LLM output                          │
│  • Post to X/Twitter via API                                    │
│  • Post to LinkedIn via API                                     │
│  • Send newsletter via Resend                                   │
│  • Return success/error confirmation page                       │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Project Structure

```
max-content/
├── README.md                        # This file
├── AGENTS.md                        # AI agent guidelines
├── n8n-workflows/
│   ├── content-generator.json       # Main content generation workflow
│   ├── content-approval.json        # Approval & posting workflow
│   ├── workflow-error-handler.json  # Error handling utilities
│   ├── input-schema.md              # Form input documentation
│   ├── sheets-schema.md             # Google Sheets schema
│   ├── prompts/                     # LLM prompt templates
│   └── docs/                        # Workflow documentation
├── scripts/
│   ├── update-workflows.py          # Workflow JSON updater
│   └── fix-email-colors.py          # Email template fixer
└── features/
    ├── prd.md                        # Product Requirements
    ├── technical-requirements-spec.md
    ├── voice-dna-framework.md        # LLM prompts & voice calibration
    └── implementation-shards/        # Build guides
```

---

## 🔧 Workflows

### 1. Content Generator (`content-generator.json`)

**Trigger:** Webhook form submission

**Inputs:**

- Content source (YouTube URL, transcript, or raw text)
- Platform selection (X, LinkedIn, Newsletter, Instagram, Skool)
- Newsletter settings (recipient emails, sender name)

**Process:**

1. Parse and prepare input data
2. Call Gemini to generate platform-specific content
3. Build visual preview HTML page
4. Encode payload with pipe-delimited format for approval

**Output:** Interactive preview page with "Approve and Post" button

### 2. Content Approval (`content-approval.json`)

**Trigger:** Approval button click (webhook with encoded payload)

**Process:**

1. Decode pipe-delimited payload
2. Parse raw LLM JSON output
3. Route to platform-specific posting nodes
4. Post to X/Twitter, LinkedIn, send newsletters
5. Collect results and errors

**Output:** Confirmation page with success/error details

---

## 🛠️ Setup

### Prerequisites

- n8n instance (local Docker or Hostinger VPS)
- Google Gemini API key
- X/Twitter API credentials (for auto-posting)
- LinkedIn OAuth credentials (for auto-posting)
- Resend API key (for newsletters)

### Installation

1. **Import workflows into n8n:**
   - `n8n-workflows/content-generator.json`
   - `n8n-workflows/content-approval.json`

2. **Configure credentials in n8n:**
   - Google Gemini API
   - Twitter OAuth 2.0
   - LinkedIn OAuth 2.0
   - Resend API (HTTP Header Auth)

3. **Activate both workflows**

4. **Access the form:**
   - Navigate to: `https://your-n8n-instance/webhook/content-generator`

---

## 🖥️ Production Environment

**Hostinger VPS (Hackathon Submission)**

| Property   | Value                                  |
| ---------- | -------------------------------------- |
| Hostname   | `srv1197870.hstgr.cloud`               |
| IP Address | `72.62.71.116`                         |
| SSH        | `ssh root@72.62.71.116`                |
| n8n URL    | `https://n8n.hostinger.macinations.au` |

---

## 📋 Content Quality Standards

Every generated post follows the **Hook → Value → CTA** structure:

| Component | Purpose                              | Example                                  |
| --------- | ------------------------------------ | ---------------------------------------- |
| **Hook**  | 1-2 sentences to capture attention   | "Most people misunderstand AI agents..." |
| **Value** | Detailed insight or transformation   | Specific steps, examples, data           |
| **CTA**   | Natural, platform-appropriate action | "Reply 'guide' for the PDF"              |

### Anti-Slop Rules

- ✅ Specific examples, not vague advice
- ✅ Platform-native voice and length
- ✅ Something a creator would actually post
- ❌ Generic filler ("In today's fast-paced world...")
- ❌ Obvious AI-generated patterns

---

## 🔐 Security

- API keys stored in n8n Credentials Manager (encrypted)
- No hardcoded secrets in workflow JSON
- Payload uses base64 encoding for transport

---

## 📈 Payload Format

The system uses a pipe-delimited payload format to avoid JSON encoding issues:

```
sessionId|x|linkedin|newsletter|instagram|skool|recipients|senderName|base64LlmText
```

| Position | Field            | Example                     |
| -------- | ---------------- | --------------------------- |
| 0        | Session ID       | `session-1734175234567`     |
| 1-5      | Platform flags   | `1` (enabled) or `0`        |
| 6        | Recipient emails | `email1@x.com,email2@x.com` |
| 7        | Sender name      | `Max Content`               |
| 8        | LLM output       | Base64-encoded JSON         |

---

## 📄 License

MIT License – Built for the Hostinger x n8n Hackathon
