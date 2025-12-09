# Shard 05: Core Workflow - Ingestion

## Content Repurposing Engine

**Estimated Time:** 30-45 minutes  
**Dependencies:** Shard 04 (Sheets structure ready)  
**Outcome:** Working input flow that stores transcripts

---

## Prerequisites

- [ ] Shard 04 complete (Google Sheets structure created)
- [ ] Sheet ID noted
- [ ] n8n open in browser

---

## Tasks

### 5.1 Create Main Workflow

1. [ ] In n8n, click **Add Workflow**
2. [ ] Rename: `Content Repurposing Engine`
3. [ ] Add description: "Transforms video transcripts into platform-ready social content"

- [ ] Workflow created

### 5.2 Add Form Trigger Node

1. [ ] Click **+** → Search for **n8n Form Trigger**
2. [ ] Configure:
   - Form Title: `Content Repurposing Engine`
   - Form Description: `Paste a video transcript to generate social media content`
3. [ ] Add Form Fields:

**Field 1:**

- Field Label: `Video Title`
- Field Type: Text
- Required: Yes

**Field 2:**

- Field Label: `Video URL`
- Field Type: Text
- Required: No

**Field 3:**

- Field Label: `Transcript`
- Field Type: Text (Multiline)
- Required: Yes

**Field 4:**

- Field Label: `Target Niche`
- Field Type: Dropdown
- Options: `AI/Business, Entrepreneurship, Tech, Other`
- Required: No

4. [ ] Click **Test Step** to generate form URL
5. [ ] Copy the Form URL

```
Form URL: ________________________________________________
```

- [ ] Form Trigger configured

### 5.3 Add Set Node (Metadata)

1. [ ] Connect new node after Form Trigger
2. [ ] Add **Set** node
3. [ ] Name: `Set Metadata`
4. [ ] Add fields:
   - `video_id`: Expression → `{{ $runIndex }}-{{ Date.now() }}`
   - `video_title`: Expression → `{{ $json.Video_Title }}`
   - `video_url`: Expression → `{{ $json.Video_URL || '' }}`
   - `transcript`: Expression → `{{ $json.Transcript }}`
   - `niche`: Expression → `{{ $json.Target_Niche || 'AI/Business' }}`
   - `created_at`: Expression → `{{ $now.toISO() }}`

- [ ] Set node configured

### 5.4 Add Google Sheets Node (Store Raw)

1. [ ] Connect new node after Set Metadata
2. [ ] Add **Google Sheets** node
3. [ ] Name: `Store Raw Transcript`
4. [ ] Configure:
   - Credential: (your Google Sheets credential)
   - Resource: Sheet Within Document
   - Operation: **Append Row**
   - Document: Select `Content Repurposing Engine`
   - Sheet: Select `Raw_Transcripts`
   - Mapping: Map from input → Define automatically
5. [ ] Map columns:
   - video_id → `{{ $json.video_id }}`
   - video_title → `{{ $json.video_title }}`
   - video_url → `{{ $json.video_url }}`
   - transcript → `{{ $json.transcript }}`
   - metadata → `{{ JSON.stringify({ niche: $json.niche }) }}`
   - created_at → `{{ $json.created_at }}`

- [ ] Google Sheets node configured

### 5.5 Add Sticky Notes for Organization

Add sticky notes to document the workflow:

1. [ ] Note 1 (above Form Trigger): "INPUT: Video transcript + metadata"
2. [ ] Note 2 (above Set Metadata): "PROCESS: Add IDs and timestamps"
3. [ ] Note 3 (above Sheets node): "STORE: Save raw transcript"

- [ ] Workflow documented with notes

---

## Verification: Test the Ingestion Flow

### 5.6 Test with Sample Data

1. [ ] Open the Form URL in a new browser tab
2. [ ] Fill in test data:
   - Video Title: `Test - How to Automate Any Business`
   - Video URL: `https://youtu.be/kQFW3bUrOu4`
   - Transcript:
     ```
     Today I'm going to show you the three phases of AI automation.
     Phase one is using no-code tools like Make and Zapier.
     Phase two is building custom solutions.
     Phase three is becoming an AI transformation partner.
     ```
   - Target Niche: `AI/Business`
3. [ ] Submit the form
4. [ ] Switch to n8n - execution should appear
5. [ ] Verify all nodes show green (success)
6. [ ] Check Google Sheets - new row should appear in `Raw_Transcripts`

- [ ] Test data flows through all nodes
- [ ] Test data appears in Google Sheets

### 5.7 Clean Up Test Data

- [ ] Delete test row from Google Sheets
- [ ] Keep the workflow saved

---

## Current Workflow State

At this point your workflow looks like:

```
┌──────────────────┐     ┌───────────────┐     ┌─────────────────────┐
│  Form Trigger    │────▶│  Set Metadata │────▶│  Store Raw          │
│  (transcript +   │     │  (add IDs)    │     │  Transcript         │
│   metadata)      │     │               │     │  (Google Sheets)    │
└──────────────────┘     └───────────────┘     └─────────────────────┘
```

---

## Troubleshooting

### Form not accessible

- Check n8n is running (`docker ps`)
- Verify webhook URL uses correct IP
- Try: `http://YOUR_VPS_IP:5678/form/form-id`

### Sheets node fails

- Re-authenticate Google Sheets credential
- Verify Sheet ID and sheet name are correct
- Check sheets node can browse the document

### Transcript not saving fully

- Check for character limits
- Use "Text (Multiline)" for transcript field
- Increase cell size in Google Sheets if needed

---

## Completion Checklist

- [ ] Main workflow created: "Content Repurposing Engine"
- [ ] Form Trigger configured with all fields
- [ ] Set Metadata node adds video_id and timestamps
- [ ] Google Sheets node stores to Raw_Transcripts
- [ ] Test submission successful
- [ ] Data appears in Google Sheets

---

## Record These Values

```
Workflow Name: Content Repurposing Engine
Form URL: http://________________:5678/form/________________
Sheet Name: Raw_Transcripts
```

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 06: Idea Extraction Node**

---

_Your ingestion pipeline is working! Next we'll add AI-powered idea extraction._
