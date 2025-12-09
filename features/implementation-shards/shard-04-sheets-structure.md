# Shard 04: Google Sheets Structure

## Content Repurposing Engine

**Estimated Time:** 15-20 minutes  
**Dependencies:** Shard 03 (Google Sheets connected)  
**Outcome:** Structured spreadsheet ready for content storage

---

## Prerequisites

- [ ] Shard 03 complete (Google Sheets OAuth working in n8n)
- [ ] Access to Google Drive

---

## Tasks

### 4.1 Create Main Spreadsheet

1. [ ] Go to: https://sheets.google.com
2. [ ] Click **Blank** to create new spreadsheet
3. [ ] Rename it: `Content Repurposing Engine`
4. [ ] Note the Sheet ID from URL:
   ```
   https://docs.google.com/spreadsheets/d/[THIS_IS_YOUR_SHEET_ID]/edit
   ```

```
Sheet ID: ________________________________________________
```

- [ ] Spreadsheet created and ID noted

### 4.2 Create Sheet: Raw_Transcripts

1. [ ] Right-click the default "Sheet1" tab → Rename to `Raw_Transcripts`
2. [ ] Add headers in Row 1:

| A            | B               | C             | D              | E            | F              |
| ------------ | --------------- | ------------- | -------------- | ------------ | -------------- |
| **video_id** | **video_title** | **video_url** | **transcript** | **metadata** | **created_at** |

3. [ ] Format headers:
   - Bold
   - Freeze row 1 (View → Freeze → 1 row)
   - Background color: Light gray

- [ ] Raw_Transcripts sheet configured

### 4.3 Create Sheet: Ideas_Extracted

1. [ ] Click **+** to add new sheet
2. [ ] Name it: `Ideas_Extracted`
3. [ ] Add headers:

| A           | B            | C              | D           | E         | F             |
| ----------- | ------------ | -------------- | ----------- | --------- | ------------- |
| **idea_id** | **video_id** | **idea_title** | **summary** | **quote** | **idea_type** |

4. [ ] Format headers (same as above)

- [ ] Ideas_Extracted sheet configured

### 4.4 Create Sheet: Generated_Content

1. [ ] Add new sheet: `Generated_Content`
2. [ ] Add headers:

| A              | B            | C            | D                | E        | F        | G       | H                 | I          | J              |
| -------------- | ------------ | ------------ | ---------------- | -------- | -------- | ------- | ----------------- | ---------- | -------------- |
| **content_id** | **video_id** | **platform** | **content_type** | **hook** | **body** | **cta** | **quality_score** | **status** | **created_at** |

3. [ ] Format headers
4. [ ] For column C (platform), add data validation:
   - Select column C (excluding header)
   - Data → Data validation
   - Criteria: Dropdown
   - Values: `twitter, linkedin, newsletter`

- [ ] Generated_Content sheet configured

### 4.5 Create Sheet: Quality_Logs

1. [ ] Add new sheet: `Quality_Logs`
2. [ ] Add headers:

| A          | B              | C              | D                     | E               | F               | G             |
| ---------- | -------------- | -------------- | --------------------- | --------------- | --------------- | ------------- |
| **log_id** | **content_id** | **hook_score** | **specificity_score** | **voice_score** | **value_score** | **cta_score** |

| H               | I        | J            | K             |
| --------------- | -------- | ------------ | ------------- |
| **total_score** | **pass** | **feedback** | **timestamp** |

3. [ ] Format headers

- [ ] Quality_Logs sheet configured

### 4.6 (Optional) Add Sheet: Config

1. [ ] Add new sheet: `Config`
2. [ ] Add configuration values:

| A                            | B         |
| ---------------------------- | --------- |
| **Setting**                  | **Value** |
| quality_threshold_twitter    | 16        |
| quality_threshold_linkedin   | 18        |
| quality_threshold_newsletter | 20        |
| max_refine_attempts          | 2         |
| tweets_per_video             | 5         |
| linkedin_per_video           | 3         |
| newsletter_per_video         | 1         |

- [ ] Config sheet added (optional)

---

## Sheet Structure Summary

Your spreadsheet should now have 4-5 tabs:

```
📊 Content Repurposing Engine
├── 📋 Raw_Transcripts (6 columns)
├── 📋 Ideas_Extracted (6 columns)
├── 📋 Generated_Content (10 columns)
├── 📋 Quality_Logs (11 columns)
└── 📋 Config (optional - 2 columns)
```

---

## Verification Checklist

### 4.7 Verify in n8n

1. [ ] Open n8n → Create test workflow
2. [ ] Add **Google Sheets** node
3. [ ] Operation: **Append Row**
4. [ ] Select your `Content Repurposing Engine` spreadsheet
5. [ ] Verify all 4 sheets appear in dropdown
6. [ ] Verify column headers load correctly

- [ ] All sheets accessible from n8n

### 4.8 Test Write Operation

1. [ ] In n8n Google Sheets node:
   - Sheet: `Raw_Transcripts`
   - Operation: Append Row
2. [ ] Add test data:
   ```
   video_id: test-001
   video_title: Test Video
   transcript: This is a test
   created_at: (use expression: {{$now.toISO()}})
   ```
3. [ ] Execute node
4. [ ] Check spreadsheet - row should appear

- [ ] Test row written successfully
- [ ] Delete test row from spreadsheet

---

## Troubleshooting

### Sheets not appearing in n8n

- Refresh the node
- Re-authorize Google Sheets credential
- Check sheet is in same Google account

### Columns not loading

- Ensure Row 1 has headers
- No merged cells in headers
- Refresh n8n node

### Permission denied

- Ensure Google account has edit access to sheet
- Check OAuth scopes include Drive access

---

## Completion Checklist

- [ ] Spreadsheet created: "Content Repurposing Engine"
- [ ] Sheet: Raw_Transcripts (6 columns)
- [ ] Sheet: Ideas_Extracted (6 columns)
- [ ] Sheet: Generated_Content (10 columns)
- [ ] Sheet: Quality_Logs (11 columns)
- [ ] All sheets accessible from n8n
- [ ] Test write successful

---

## Record These Values

```
Spreadsheet Name: Content Repurposing Engine
Spreadsheet ID: ________________________________________________
Sheet Names: Raw_Transcripts, Ideas_Extracted, Generated_Content, Quality_Logs
```

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 05: Core Workflow - Ingestion**

---

_Your storage layer is now ready for the workflow!_
