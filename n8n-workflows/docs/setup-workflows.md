# n8n Workflows Documentation

> **Max Content - AI-Powered Content Repurposing Engine**

---

## Workflow Overview

The system consists of two main workflows that work together:

```
┌────────────────────────────────────────────────────────────────┐
│                     USER SUBMITS FORM                          │
│  (YouTube URL, transcript, or raw content + platform selection) │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│             CONTENT GENERATOR WORKFLOW                          │
│  content-generator.json                                         │
│                                                                 │
│  1. Receive form submission via webhook                         │
│  2. Prepare and normalize input data                            │
│  3. Call Gemini to generate platform content                    │
│  4. Build interactive preview page                              │
│  5. Return HTML with "Approve and Post" button                  │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│                    PREVIEW PAGE                                 │
│  Shows all generated content with platform indicators           │
│  User clicks "Approve and Post" to proceed                      │
└─────────────────────────┬──────────────────────────────────────┘
                          │
                          ▼
┌────────────────────────────────────────────────────────────────┐
│             CONTENT APPROVAL WORKFLOW                           │
│  content-approval.json                                          │
│                                                                 │
│  1. Receive approval click via webhook                          │
│  2. Decode payload (pipe-delimited format)                      │
│  3. Parse LLM JSON output                                       │
│  4. Post to enabled platforms:                                  │
│     - X/Twitter (auto-post via API)                             │
│     - LinkedIn (auto-post via API)                              │
│     - Newsletter (send via Resend)                              │
│  5. Return success/error confirmation page                      │
└────────────────────────────────────────────────────────────────┘
```

---

## Workflow Files

| File                          | Purpose                          |
| ----------------------------- | -------------------------------- |
| `content-generator.json`      | Main content generation workflow |
| `content-approval.json`       | Approval and posting workflow    |
| `workflow-error-handler.json` | Error handling utilities         |

---

## Content Generator Nodes

### 1. Content Form Webhook

- **Type:** Webhook
- **Path:** `/content-generator`
- **Method:** POST
- **Purpose:** Receives form submission

### 2. Prepare Input

- **Type:** Code
- **Purpose:** Extracts and normalizes input data
- **Outputs:** sessionId, platforms, content source, newsletter settings

### 3. Generate Content

- **Type:** Google Gemini Chat Model
- **Purpose:** Generates platform-specific content
- **Model:** gemini-1.5-flash
- **Output:** JSON with tweets, linkedin, newsletter, instagram, skool

### 4. Build Preview Response

- **Type:** Code
- **Purpose:** Creates interactive HTML preview
- **Key Functions:**
  - Parses LLM JSON output
  - Sanitizes control characters
  - Creates pipe-delimited payload
  - Encodes payload as base64
  - Generates responsive preview HTML

### 5. Respond with HTML

- **Type:** Respond to Webhook
- **Purpose:** Returns preview page to user

---

## Content Approval Nodes

### 1. Approval Webhook

- **Type:** Webhook
- **Path:** `/content-approval-confirm`
- **Purpose:** Receives approval click with encoded payload

### 2. Decode Payload

- **Type:** Code
- **Purpose:** Decodes pipe-delimited payload
- **Process:**
  1. Base64 decode outer payload
  2. Split by pipe delimiter
  3. Extract platform flags and settings
  4. Base64 decode LLM text
  5. JSON parse LLM output

### 3. Prepare Tasks

- **Type:** Code
- **Purpose:** Routes content to platform-specific nodes

### 4. Platform Routing (IF nodes)

- **Is X?** → Post to X
- **Is LinkedIn?** → Post to LinkedIn
- **Is Newsletter?** → Build Email HTML → Send via Resend

### 5. Post to X

- **Type:** Twitter (X) OAuth2
- **Purpose:** Posts tweets via API

### 6. Post to LinkedIn

- **Type:** LinkedIn OAuth2
- **Purpose:** Posts to LinkedIn feed

### 7. Build Email HTML

- **Type:** Code
- **Purpose:** Generates newsletter email template
- **Features:**
  - Solid color backgrounds (Outlook compatible)
  - Includes Instagram/Skool content if selected
  - Responsive table-based layout

### 8. Send via Resend

- **Type:** HTTP Request
- **Purpose:** Sends email via Resend API

### 9. Build Confirmation

- **Type:** Code
- **Purpose:** Creates success/error page with results

---

## Payload Format

The system uses a **pipe-delimited** format instead of JSON:

```
sessionId|x|linkedin|newsletter|instagram|skool|recipients|senderName|base64LlmText
```

| Position | Field       | Example                     |
| -------- | ----------- | --------------------------- |
| 0        | Session ID  | `session-1734175234567`     |
| 1        | X/Twitter   | `1` (enabled) or `0`        |
| 2        | LinkedIn    | `1` or `0`                  |
| 3        | Newsletter  | `1` or `0`                  |
| 4        | Instagram   | `1` or `0`                  |
| 5        | Skool       | `1` or `0`                  |
| 6        | Recipients  | `email1@x.com,email2@x.com` |
| 7        | Sender Name | `Newsletter Name`           |
| 8        | LLM Output  | Base64-encoded JSON         |

**Why pipe-delimited?**

- LLM output contains control characters that break JSON parsing
- Nested JSON structures are fragile when base64 encoded
- Pipe format keeps LLM output isolated in its own base64 segment

---

## Required Credentials

Configure in n8n Settings → Credentials:

| Credential        | Type             | Used By          |
| ----------------- | ---------------- | ---------------- |
| **Google Gemini** | API Key          | Generate Content |
| **Twitter (X)**   | OAuth 2.0        | Post to X        |
| **LinkedIn**      | OAuth 2.0        | Post to LinkedIn |
| **Resend**        | HTTP Header Auth | Send via Resend  |

---

## Importing Workflows

1. Open n8n
2. Go to Workflows → Import from File
3. Select `content-generator.json`
4. Repeat for `content-approval.json`
5. Configure credentials in each workflow
6. Activate both workflows

---

## Testing

1. **Test Generator:**
   - POST to `/webhook/content-generator` with form data
   - Verify preview page appears

2. **Test Approval:**
   - Click "Approve and Post" on preview
   - Verify posts appear on platforms
   - Check confirmation page for errors

---

## Troubleshooting

### Preview shows "Error parsing AI response"

- Check Gemini API key is valid
- Verify prompt format in Generate Content node

### "Bad control character" error

- Fixed in current version with pipe-delimited payload
- Re-import workflows if using old version

### Posts not appearing

- Check OAuth credentials are valid
- Verify API rate limits not exceeded
- Check n8n execution logs

### Newsletter not sending

- Verify Resend API key
- Check recipient email format
- Confirm "From" address is verified in Resend
