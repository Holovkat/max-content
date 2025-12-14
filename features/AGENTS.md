# AGENTS.md — Features Documentation

> **Reference documentation for Max Content - AI-Powered Content Repurposing Engine**

---

## ✅ Implementation Status

| Feature                   | Status      | Notes                                     |
| ------------------------- | ----------- | ----------------------------------------- |
| Content Input Form        | ✅ Complete | YouTube URL, transcript, or raw text      |
| Multi-Platform Generation | ✅ Complete | X, LinkedIn, Newsletter, Instagram, Skool |
| Preview Page              | ✅ Complete | Visual preview with platform indicators   |
| X/Twitter Auto-Post       | ✅ Complete | OAuth 2.0 integration                     |
| LinkedIn Auto-Post        | ✅ Complete | OAuth 2.0 integration                     |
| Newsletter Send           | ✅ Complete | Via Resend API                            |
| Instagram/Skool           | ✅ Complete | Copy-ready (no API posting)               |
| Email Template            | ✅ Complete | Outlook-compatible solid colors           |
| Payload Encoding          | ✅ Complete | Pipe-delimited format                     |

---

## Documentation Structure

### Core Documents

| File                             | Purpose                         | Status           |
| -------------------------------- | ------------------------------- | ---------------- |
| `prd.md`                         | Product Requirements Document   | 📋 Original spec |
| `technical-requirements-spec.md` | Technical architecture          | 📋 Original spec |
| `voice-dna-framework.md`         | LLM prompts & voice calibration | 📋 Original spec |
| `submission-requirements.md`     | Hackathon submission checklist  | 📋 Original spec |

### Implementation Shards

**Location:** `implementation-shards/`

These were the planned build guides. The actual implementation deviated based on real-world requirements:

| Shard | Planned Purpose        | Actual Implementation                                 |
| ----- | ---------------------- | ----------------------------------------------------- |
| 00-04 | Infrastructure setup   | ✅ n8n local + Hostinger VPS                          |
| 05-06 | Ingestion + extraction | ✅ Combined into content-generator.json               |
| 07    | Twitter generation     | ✅ Part of unified generation                         |
| 08    | LinkedIn generation    | ✅ Part of unified generation                         |
| 09    | Newsletter generation  | ✅ Part of unified generation + Instagram/Skool added |
| 10    | Quality gate           | ⏭️ Deferred (LLM output quality sufficient)           |
| 11-12 | Testing + Demo         | ✅ Testing done iteratively                           |

---

## Actual Workflow Architecture

```
┌──────────────────────────────────────────────────────────────┐
│  content-generator.json                                       │
├──────────────────────────────────────────────────────────────┤
│  Form Webhook → Prepare Input → Gemini → Preview → Response  │
│                                                               │
│  Key Nodes:                                                   │
│  • Content Form Webhook (trigger)                             │
│  • Prepare Input (extract/normalize data)                     │
│  • Generate Content (Gemini API call)                         │
│  • Build Preview Response (HTML + encoded payload)            │
└──────────────────────────────────────────────────────────────┘
                          │
                          ▼
┌──────────────────────────────────────────────────────────────┐
│  content-approval.json                                        │
├──────────────────────────────────────────────────────────────┤
│  Approval Webhook → Decode → Route → Post → Confirm          │
│                                                               │
│  Key Nodes:                                                   │
│  • Approval Webhook (trigger from preview button)             │
│  • Decode Payload (pipe-delimited → JSON)                     │
│  • Prepare Tasks (route by platform)                          │
│  • Post to X / Post to LinkedIn / Send via Resend             │
│  • Build Confirmation (success/error page)                    │
└──────────────────────────────────────────────────────────────┘
```

---

## Content Output Structure

### LLM Response Format

```json
{
  "key_ideas": ["...", "...", "..."],
  "tweets": [
    { "type": "hook", "content": "..." },
    { "type": "insight", "content": "..." },
    { "type": "cta", "content": "..." }
  ],
  "linkedin": {
    "hook": "Opening line",
    "body": "Main content",
    "question": "Engagement prompt"
  },
  "newsletter": {
    "subject": "Email subject",
    "intro": "Opening paragraph",
    "points": ["Key point 1", "Key point 2"],
    "cta": "Call to action"
  },
  "instagram": [
    { "hook": "Caption hook", "body": "Caption body", "cta": "Call to action" }
  ],
  "skool": {
    "title": "Post title",
    "intro": "Introduction",
    "takeaways": ["Takeaway 1", "Takeaway 2"],
    "discussion": "Discussion prompt"
  }
}
```

---

## Payload Format

The system uses **pipe-delimited** encoding to avoid JSON escaping issues:

```
sessionId|x|linkedin|newsletter|instagram|skool|recipients|senderName|base64LlmText
         ^   ^         ^           ^        ^       ^            ^          ^
         |   |         |           |        |       |            |          |
        1/0 1/0       1/0         1/0      1/0   emails       name     Base64
```

**Why not JSON?**  
LLM output contains control characters that break `JSON.parse()` when nested inside another JSON object. The pipe format keeps the LLM output isolated.

---

## Email Template

The newsletter uses **solid colors** for email client compatibility:

```
┌─────────────────────────────────┐
│  HEADER (#667eea purple)        │  ← White text
│  Subject + Sender               │
├─────────────────────────────────┤
│  INTRO (#ffffff white)          │  ← Dark text (#374151)
│  Newsletter introduction        │
├─────────────────────────────────┤
│  KEY TAKEAWAYS (#f8fafc)        │  ← Dark text
│  Bullet points                  │
├─────────────────────────────────┤
│  INSTAGRAM (#fce7f3 pink)       │  ← Dark text
│  (if selected)                  │
├─────────────────────────────────┤
│  SKOOL (#e0e7ff lavender)       │  ← Dark text
│  (if selected)                  │
├─────────────────────────────────┤
│  FOOTER (#374151 gray)          │  ← Light text (#d1d5db)
└─────────────────────────────────┘
```

**No gradients** - Outlook doesn't support them.

---

## Common Issues & Solutions

### "Bad control character in string literal"

**Cause:** LLM output has control characters (newlines, tabs, etc.)  
**Solution:** Pipe-delimited payload with separate base64 encoding for LLM output

### White text on white background

**Cause:** CSS gradients don't work in Outlook  
**Solution:** Solid fallback background colors

### Newsletter not sending

**Check:**

1. Resend API key configured
2. Recipients have valid email format
3. From address verified in Resend

---

## Related Files

| File                | Purpose                    |
| ------------------- | -------------------------- |
| `../README.md`      | Project overview           |
| `../AGENTS.md`      | AI agent guidelines        |
| `../n8n-workflows/` | Actual workflow JSON files |
| `../scripts/`       | Utility scripts            |
