# Workflow Setup: Core Ingestion

## Shard 05 - Implementation Guide

This document provides step-by-step instructions for setting up the core ingestion workflow in n8n.

---

## Overview

The ingestion workflow handles:

1. Receiving transcript input via web form
2. Adding metadata (IDs, timestamps, defaults)
3. Storing raw transcript to Google Sheets

---

## Workflow Structure

```
┌──────────────────┐     ┌───────────────┐     ┌─────────────────────┐
│  Form Trigger    │────▶│  Set Metadata │────▶│  Store Raw          │
│  (user input)    │     │  (add IDs)    │     │  Transcript         │
└──────────────────┘     └───────────────┘     └─────────────────────┘
```

---

## Option A: Import Workflow JSON

**Fastest method - import pre-built workflow:**

1. Open n8n in browser
2. Click **+** to create new workflow
3. Click **⋮** menu → **Import from File**
4. Select: `n8n-workflows/workflow-ingestion.json`
5. The workflow will load with all nodes configured
6. **Update credentials** (see Post-Import Setup below)

---

## Option B: Manual Setup

### Node 1: Form Trigger

1. Add **n8n Form Trigger** node
2. Configure:
   - Form Title: `Content Repurposing Engine`
   - Form Description: `Transform video transcripts into platform-ready social content`

3. Add Form Fields:

| Order | Label           | Type     | Required | Options/Placeholder                                                                                       |
| ----- | --------------- | -------- | -------- | --------------------------------------------------------------------------------------------------------- |
| 1     | Video Title     | Text     | Yes      | "e.g., How to Automate Any Business"                                                                      |
| 2     | Video URL       | Text     | No       | "https://youtube.com/..."                                                                                 |
| 3     | Transcript      | Textarea | Yes      | "Paste your video transcript here..."                                                                     |
| 4     | Content Niche   | Dropdown | No       | AI/Business, Entrepreneurship, Tech/Software, Marketing, Finance, Health/Wellness, Education, Other       |
| 5     | Target Audience | Dropdown | No       | Entrepreneurs, Agency Owners, Developers, Executives, Beginners, Advanced Practitioners, General Audience |
| 6     | Tone            | Dropdown | No       | practical, inspirational, controversial, educational, conversational                                      |
| 7     | Tweet Count     | Number   | No       | "5"                                                                                                       |
| 8     | LinkedIn Count  | Number   | No       | "3"                                                                                                       |

### Node 2: Set Metadata

1. Add **Set** node
2. Name: `Set Metadata`
3. Mode: Manual
4. Add these assignments:

| Field           | Expression                          |
| --------------- | ----------------------------------- | --- | ------------------- |
| video_id        | `={{ Date.now() }}-{{ $runIndex }}` |
| video_title     | `={{ $json['Video Title'] }}`       |
| video_url       | `={{ $json['Video URL']             |     | '' }}`              |
| transcript      | `={{ $json['Transcript'] }}`        |
| niche           | `={{ $json['Content Niche']         |     | 'AI/Business' }}`   |
| target_audience | `={{ $json['Target Audience']       |     | 'Entrepreneurs' }}` |
| tone            | `={{ $json['Tone']                  |     | 'practical' }}`     |
| tweet_count     | `={{ $json['Tweet Count']           |     | 5 }}`               |
| linkedin_count  | `={{ $json['LinkedIn Count']        |     | 3 }}`               |
| created_at      | `={{ $now.toISO() }}`               |

### Node 3: Store Raw Transcript

1. Add **Google Sheets** node
2. Name: `Store Raw Transcript`
3. Configure:
   - Credential: (Select your Google Sheets OAuth credential)
   - Operation: **Append Row**
   - Document: Select `Content Repurposing Engine` spreadsheet
   - Sheet: Select `Raw_Transcripts`

4. Column Mapping:

| Sheet Column | Value Expression                                                                                                                                                                |
| ------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| video_id     | `={{ $json.video_id }}`                                                                                                                                                         |
| video_title  | `={{ $json.video_title }}`                                                                                                                                                      |
| video_url    | `={{ $json.video_url }}`                                                                                                                                                        |
| transcript   | `={{ $json.transcript }}`                                                                                                                                                       |
| metadata     | `={{ JSON.stringify({ niche: $json.niche, target_audience: $json.target_audience, tone: $json.tone, tweet_count: $json.tweet_count, linkedin_count: $json.linkedin_count }) }}` |
| created_at   | `={{ $json.created_at }}`                                                                                                                                                       |

### Connect Nodes

```
Form Trigger → Set Metadata → Store Raw Transcript
```

---

## Post-Import Setup

After importing the workflow JSON, you must:

### 1. Connect Google Sheets Credential

1. Click on **Store Raw Transcript** node
2. Click the credential dropdown
3. Select or create Google Sheets OAuth2 credential
4. Authorize access to your Google account

### 2. Select Your Spreadsheet

1. In **Store Raw Transcript** node
2. Click Document dropdown
3. Browse and select `Content Repurposing Engine`
4. Verify Sheet is set to `Raw_Transcripts`

### 3. Test the Form

1. Click **Test Step** on Form Trigger
2. Copy the generated Form URL
3. Open URL in new browser tab
4. Fill in test data and submit
5. Verify:
   - All nodes show green (success)
   - Row appears in Google Sheets

---

## Form URL

After setup, your form will be available at:

```
http://YOUR_VPS_IP:5678/form/[generated-form-id]
```

Note this URL for demo purposes.

---

## Verification Checklist

- [ ] Form Trigger shows all 8 fields
- [ ] Set Metadata creates all 10 output fields
- [ ] Google Sheets credential connected
- [ ] Spreadsheet and sheet selected correctly
- [ ] Test submission creates row in Raw_Transcripts
- [ ] All required fields stored correctly
- [ ] Optional fields use defaults when empty

---

## Troubleshooting

### Form not loading

- Check n8n is running: `docker ps`
- Verify workflow is active (toggle on)
- Check firewall allows port 5678

### Sheets node fails

- Re-authorize Google Sheets credential
- Verify spreadsheet exists with correct name
- Check Sheet name matches exactly: `Raw_Transcripts`

### Transcript not saving fully

- Google Sheets cells have a 50,000 character limit
- Very long transcripts may need to be chunked

---

## Next Steps

After this workflow is verified, it will be extended with:

- Shard 06: Idea Extraction (Gemini node)
- Shard 07-09: Content Generation nodes
- Shard 10: Quality Gate

The ingestion pipeline will connect to these via the `Set Metadata` output.

---

_This workflow serves as the foundation for all content generation._
