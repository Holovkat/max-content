# AGENTS.md — Max Content

> **AI-Powered Content Repurposing Engine**  
> n8n workflows that transform long-form content into platform-ready social posts.

---

## Project Snapshot

| Attribute     | Value                                             |
| ------------- | ------------------------------------------------- |
| **Type**      | n8n workflow automation                           |
| **Status**    | ✅ Implemented                                    |
| **AI Model**  | Google Gemini Flash                               |
| **Platforms** | X/Twitter, LinkedIn, Newsletter, Instagram, Skool |
| **Auto-Post** | X, LinkedIn, Newsletter (via Resend)              |
| **Copy-Only** | Instagram, Skool                                  |

---

## 🔧 Current Workflows

### 1. Content Generator (`content-generator.json`)

| Node                       | Purpose                                                    |
| -------------------------- | ---------------------------------------------------------- |
| **Content Form Webhook**   | Receives form submission with content + platform selection |
| **Prepare Input**          | Extracts and normalizes input data                         |
| **Generate Content**       | Calls Gemini to create platform-specific content           |
| **Build Preview Response** | Creates interactive HTML preview page                      |
| **Respond with HTML**      | Returns preview with approval button                       |

### 2. Content Approval (`content-approval.json`)

| Node                   | Purpose                                          |
| ---------------------- | ------------------------------------------------ |
| **Approval Webhook**   | Receives encoded payload from approval button    |
| **Decode Payload**     | Parses pipe-delimited format, decodes LLM output |
| **Prepare Tasks**      | Routes content to platform-specific posting      |
| **Post to X**          | Tweets via Twitter API OAuth 2.0                 |
| **Post to LinkedIn**   | Posts via LinkedIn API                           |
| **Build Email HTML**   | Generates newsletter email template              |
| **Send via Resend**    | Sends newsletter emails                          |
| **Build Confirmation** | Returns success/error page                       |

---

## 📁 Directory Map

### Workflow Files

| Path                                        | Purpose                          |
| ------------------------------------------- | -------------------------------- |
| `n8n-workflows/content-generator.json`      | Main content generation workflow |
| `n8n-workflows/content-approval.json`       | Approval and posting workflow    |
| `n8n-workflows/workflow-error-handler.json` | Error handling utilities         |
| `n8n-workflows/input-schema.md`             | Form input documentation         |
| `n8n-workflows/sheets-schema.md`            | Google Sheets schema             |
| `n8n-workflows/prompts/`                    | LLM prompt templates             |

### Scripts

| Path                          | Purpose                            |
| ----------------------------- | ---------------------------------- |
| `scripts/update-workflows.py` | Safely updates workflow JSON files |
| `scripts/fix-email-colors.py` | Fixes email template colors        |

### Documentation

| Path                                      | Purpose                         |
| ----------------------------------------- | ------------------------------- |
| `README.md`                               | Project overview                |
| `AGENTS.md`                               | This file - AI agent guidelines |
| `features/prd.md`                         | Product Requirements Document   |
| `features/technical-requirements-spec.md` | Technical architecture          |
| `features/voice-dna-framework.md`         | LLM prompts & voice calibration |

---

## 🔄 Payload Format

The system uses a **pipe-delimited** format to avoid JSON encoding issues with LLM output:

```
sessionId|x|linkedin|newsletter|instagram|skool|recipients|senderName|base64LlmText
```

| Position | Field              | Type                   |
| -------- | ------------------ | ---------------------- |
| 0        | Session ID         | String                 |
| 1        | X/Twitter enabled  | `1` or `0`             |
| 2        | LinkedIn enabled   | `1` or `0`             |
| 3        | Newsletter enabled | `1` or `0`             |
| 4        | Instagram enabled  | `1` or `0`             |
| 5        | Skool enabled      | `1` or `0`             |
| 6        | Recipients         | Comma-separated emails |
| 7        | Sender Name        | String                 |
| 8        | LLM Output         | Base64-encoded JSON    |

**Why pipe-delimited?**

- LLM output contains control characters that break JSON parsing
- Nested JSON structures are fragile when base64 encoded
- Pipe format keeps LLM output isolated in its own base64 segment

---

## 📧 Email Template Notes

The newsletter email uses **solid background colors** instead of CSS gradients for email client compatibility:

| Element   | Color                | Notes                    |
| --------- | -------------------- | ------------------------ |
| Header    | `#667eea` (purple)   | Solid color, no gradient |
| Content   | `#ffffff` (white)    | Dark text (#374151)      |
| Instagram | `#fce7f3` (pink)     | Solid fallback           |
| Skool     | `#e0e7ff` (lavender) | Solid fallback           |
| Footer    | `#374151` (gray)     | Light text (#d1d5db)     |

**Reason:** Outlook and many email clients don't support `linear-gradient()`, causing white text to appear on white backgrounds.

---

## 🎯 Content Generation

### LLM Output Structure

```json
{
  "key_ideas": ["idea1", "idea2", "idea3"],
  "tweets": [
    { "type": "hook", "content": "..." },
    { "type": "insight", "content": "..." },
    { "type": "cta", "content": "..." }
  ],
  "linkedin": {
    "hook": "...",
    "body": "...",
    "question": "..."
  },
  "newsletter": {
    "subject": "...",
    "intro": "...",
    "points": ["...", "..."],
    "cta": "..."
  },
  "instagram": [{ "hook": "...", "body": "...", "cta": "..." }],
  "skool": {
    "title": "...",
    "intro": "...",
    "takeaways": ["..."],
    "discussion": "..."
  }
}
```

### Hook → Value → CTA Pattern

Every post follows this structure:

| Component | Purpose                              |
| --------- | ------------------------------------ |
| **Hook**  | 1-2 sentences to capture attention   |
| **Value** | Detailed insight, specific examples  |
| **CTA**   | Natural, platform-appropriate action |

---

## 🔐 Required Credentials

Configure these in n8n Credentials Manager:

| Credential         | Type        | Used By               |
| ------------------ | ----------- | --------------------- |
| Google Gemini API  | API Key     | Generate Content node |
| Twitter OAuth 2.0  | OAuth2      | Post to X node        |
| LinkedIn OAuth 2.0 | OAuth2      | Post to LinkedIn node |
| Resend API         | HTTP Header | Send via Resend node  |

---

## 🚀 Quick Commands

### Update Workflow JSON

```bash
# Run the update script
python3 scripts/update-workflows.py

# Fix email colors
python3 scripts/fix-email-colors.py
```

### Validate JSON

```bash
python3 -c "import json; json.load(open('n8n-workflows/content-generator.json')); print('Valid!')"
python3 -c "import json; json.load(open('n8n-workflows/content-approval.json')); print('Valid!')"
```

### Git Workflow

```bash
# Create branch
git checkout -b feature/your-change origin/main

# Commit and push
git add .
git commit -m "feat: description"
git push origin feature/your-change

# Create PR
gh pr create --base main --title "feat: description"

# Merge with squash
gh pr merge <PR_NUMBER> --squash --delete-branch
```

---

## ⚠️ Common Issues

### "Bad control character in string literal"

**Cause:** LLM output contains control characters that break JSON parsing.

**Solution:** The system uses pipe-delimited payload format where LLM output is separately base64 encoded.

### White text on white background in emails

**Cause:** Email clients don't support CSS gradients.

**Solution:** All gradient backgrounds replaced with solid fallback colors.

### Workflow not posting

**Check:**

1. Credentials configured correctly in n8n
2. OAuth tokens not expired
3. API rate limits not exceeded
4. Platform selection flags set correctly

---

## 📝 Version History

| Date       | Change                                         |
| ---------- | ---------------------------------------------- |
| 2024-12-14 | Initial implementation complete                |
| 2024-12-14 | Added Instagram + Skool generation             |
| 2024-12-14 | Fixed payload encoding (pipe-delimited format) |
| 2024-12-14 | Fixed email template colors for Outlook        |
