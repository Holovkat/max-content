# Workflow Setup Guide

## Content Repurposing Engine - n8n Workflows

This document explains how to import and configure the n8n workflows.

---

## Workflow Overview

| #   | Workflow File                      | Purpose                               | Triggered By     |
| --- | ---------------------------------- | ------------------------------------- | ---------------- |
| 1   | `workflow-ingestion.json`          | Form input → Store transcript         | Form submission  |
| 2   | `workflow-idea-extraction.json`    | Parallel idea extraction (GLM + Kimi) | Execute Workflow |
| 3   | `workflow-content-generation.json` | Parallel content creation             | Execute Workflow |
| 4   | `workflow-curation.json`           | Gemini picks best output              | Execute Workflow |
| 5   | `workflow-error-handler.json`      | Central error handling                | Error events     |

---

## Status Indicators

All content rows use emoji status indicators:

| Emoji | Status  | Meaning                        |
| ----- | ------- | ------------------------------ |
| ⭐    | Sent    | Content exported/published     |
| ✅    | Created | Content generated successfully |
| ❌    | Error   | Exception during processing    |
| ⏳    | Pending | In progress                    |

---

## Installation Order

**Install in this order:**

1. **Error Handler first** (other workflows reference it)
2. **Ingestion workflow**
3. **Idea Extraction workflow**
4. **Content Generation workflow**
5. **Curation workflow**

---

## Step-by-Step Installation

### 1. Import Error Handler

1. Open n8n in browser
2. Click **+** to create new workflow
3. Click **⋮** menu → **Import from File**
4. Select: `workflow-error-handler.json`
5. Configure:
   - Click **Log Error to Sheets** node
   - Select your Google Sheets credential
   - Select `Content Repurposing Engine` spreadsheet
   - Select `Error_Logs` sheet (create if needed)
6. **Save and Activate** the workflow

### 2. Import Ingestion Workflow

1. Import `workflow-ingestion.json`
2. Configure:
   - **Store Raw Transcript** node: Select your spreadsheet/sheet
   - **Execute Workflow** node: Link to Idea Extraction workflow
3. **Save and Activate**

### 3. Import Idea Extraction Workflow

1. Import `workflow-idea-extraction.json`
2. Configure credentials:
   - **Extract Ideas (GLM-4.6)**: Add GLM-4 Header Auth credential
   - **Extract Ideas (Kimi-K2)**: Add Groq Header Auth credential
   - **Store Ideas**: Select your spreadsheet/sheet
3. Link error workflow in Settings → Error Workflow
4. **Save** (don't activate - it's triggered by another workflow)

### 4. Import Content Generation Workflow

1. Import `workflow-content-generation.json`
2. Configure credentials for all 6 HTTP Request nodes:
   - GLM nodes: GLM-4 API credential
   - Kimi nodes: Groq API credential
3. Link error workflow in Settings
4. **Save**

### 5. Import Curation Workflow

1. Import `workflow-curation.json`
2. Configure:
   - **Curate Content**: Add Gemini API credential
   - **Store Curated Content**: Select your spreadsheet/sheet
3. Link error workflow in Settings
4. **Save**

---

## Credential Setup

### GLM-4 API (Header Auth)

1. Go to **Settings → Credentials → Add Credential**
2. Type: **Header Auth**
3. Configure:
   - Name: `GLM-4 API`
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_GLM4_API_KEY`

### Groq API (Header Auth)

1. Add another **Header Auth** credential
2. Configure:
   - Name: `Groq API`
   - Header Name: `Authorization`
   - Header Value: `Bearer YOUR_GROQ_API_KEY`

Get key from: [console.groq.com](https://console.groq.com)

### Gemini API

1. Add **Google Gemini** credential
2. Enter your API key from [aistudio.google.com](https://aistudio.google.com)

### Google Sheets OAuth

1. Add **Google Sheets OAuth2** credential
2. Connect your Google account
3. Authorize access to Sheets

---

## Google Sheets Setup

### Required Sheets

Your `Content Repurposing Engine` spreadsheet needs these sheets:

| Sheet Name          | Purpose               |
| ------------------- | --------------------- |
| `Raw_Transcripts`   | Input storage         |
| `Ideas_Extracted`   | GLM + Kimi ideas      |
| `Generated_Content` | Final curated content |
| `Error_Logs`        | Error tracking        |

### Column Headers

**Raw_Transcripts:**

```
status | video_id | video_title | video_url | transcript | metadata | created_at
```

**Ideas_Extracted:**

```
status | idea_id | video_id | glm_ideas | kimi_ideas | extracted_at
```

**Generated_Content:**

```
status | content_id | video_id | curated_tweets | curated_linkedin | curated_newsletter | summary | created_at
```

**Error_Logs:**

```
error_id | workflow_name | node_name | error_message | execution_id | timestamp | status
```

---

## Error Handling

All workflows are configured to:

1. Continue on error (don't stop entire workflow)
2. Route errors to the Error Handler workflow
3. Log errors to Error_Logs sheet
4. Update status column with ❌ emoji

### Email Notifications (Optional)

To add email alerts for errors:

1. Open `workflow-error-handler.json` in n8n
2. After **Log Error to Sheets**, add **Send Email** node
3. Configure with your email settings
4. Connect the nodes

---

## Testing

### Test Ingestion

1. Open the Ingestion workflow
2. Click **Test Step** on Form Trigger
3. Open the form URL in browser
4. Submit test data
5. Check:
   - ✅ Row appears in Raw_Transcripts
   - ✅ Status shows ✅ or ⏳

### Test Full Pipeline

1. Submit a real transcript via form
2. Watch executions in n8n
3. Check each sheet for data
4. Verify no errors in Error_Logs

---

## Troubleshooting

### Workflow not triggering

- Check workflow is activated (toggle on)
- Verify Execute Workflow node points to correct workflow

### API errors

- Check credentials are configured correctly
- Verify API keys are valid
- Check rate limits

### Empty content

- Check API response in execution log
- Verify prompt is being sent correctly

### Sheets not updating

- Re-authorize Google Sheets credential
- Check sheet names match exactly

---

## Execution Flow

```
Form Submit
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ INGESTION WORKFLOW                                              │
│ Form → Set Metadata → Store → Execute Idea Extraction           │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ IDEA EXTRACTION WORKFLOW                                        │
│ GLM-4.6 ─┐                                                      │
│          ├─→ Merge & Parse → Store → Execute Content Generation │
│ Kimi-K2 ─┘                                                      │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ CONTENT GENERATION WORKFLOW                                     │
│ 6 parallel API calls (GLM + Kimi × 3 platforms)                │
│ → Merge All → Execute Curation                                  │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
┌─────────────────────────────────────────────────────────────────┐
│ CURATION WORKFLOW                                               │
│ Gemini → Compare → Pick Best → Store Final Content              │
└─────────────────────────────────────────────────────────────────┘
    │
    ▼
Done! Content in Generated_Content sheet with ✅ status
```

---

_For detailed prompt content, see the `/prompts/` folder as reference._
