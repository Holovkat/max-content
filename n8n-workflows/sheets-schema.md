# Google Sheets Structure Definition

## Content Repurposing Engine

This document defines the exact structure for the Google Sheets database used by the Content Repurposing Engine.

---

## Spreadsheet Setup

**Spreadsheet Name:** `Content Repurposing Engine`

---

## Sheet 1: Raw_Transcripts

Stores the original video transcripts and metadata.

| Column | Name        | Type          | Required | Description                                          |
| ------ | ----------- | ------------- | -------- | ---------------------------------------------------- |
| A      | video_id    | string        | Yes      | Unique identifier (format: `{timestamp}-{runIndex}`) |
| B      | video_title | string        | Yes      | Title of the source video                            |
| C      | video_url   | string        | No       | YouTube or source URL                                |
| D      | transcript  | string        | Yes      | Full transcript text                                 |
| E      | metadata    | JSON string   | No       | Additional metadata (niche, audience, etc.)          |
| F      | created_at  | ISO timestamp | Yes      | When the transcript was ingested                     |

**Metadata JSON Structure:**

```json
{
  "niche": "AI/Business",
  "target_audience": "Entrepreneurs",
  "tone": "practical",
  "platforms": ["twitter", "linkedin", "newsletter"],
  "tweet_count": 5,
  "linkedin_count": 3,
  "newsletter_count": 1
}
```

**Example Row:**

```
| 1733712000000-0 | How to Automate Any Business | https://youtu.be/xxx | "Today I'm going to..." | {"niche":"AI/Business","target_audience":"Entrepreneurs",...} | 2024-12-09T00:00:00.000Z |
```

---

## Sheet 2: Ideas_Extracted

Stores the AI-extracted ideas from each transcript.

| Column | Name             | Type        | Required | Description                                      |
| ------ | ---------------- | ----------- | -------- | ------------------------------------------------ |
| A      | idea_id          | string      | Yes      | Unique identifier (format: `{video_id}-ideas`)   |
| B      | video_id         | string      | Yes      | Foreign key to Raw_Transcripts                   |
| C      | idea_title       | string      | Yes      | Brief title for the extracted ideas              |
| D      | key_ideas        | JSON string | Yes      | Array of key ideas with title, insight, evidence |
| E      | quotable_moments | JSON string | Yes      | Array of memorable quotes with type              |
| F      | frameworks       | JSON string | No       | Array of frameworks if any found                 |

**Example Row:**

```
| 1733712000000-0-ideas | 1733712000000-0 | Morningside Method | [{"title":"3 Phases",...}] | [{"quote":"Start with problems...",...}] | [{"name":"Morningside Method",...}] |
```

---

## Sheet 3: Generated_Content

Stores all generated content pieces across platforms.

| Column | Name          | Type          | Required | Description                                         |
| ------ | ------------- | ------------- | -------- | --------------------------------------------------- |
| A      | content_id    | string        | Yes      | Unique ID (format: `{video_id}-{platform}-{index}`) |
| B      | video_id      | string        | Yes      | Foreign key to Raw_Transcripts                      |
| C      | platform      | enum          | Yes      | `twitter`, `linkedin`, or `newsletter`              |
| D      | content_type  | string        | Yes      | Type of content (tweet, post, summary)              |
| E      | hook          | string        | Yes      | Opening hook/headline                               |
| F      | body          | string        | Yes      | Full content body                                   |
| G      | cta           | string        | No       | Call to action text                                 |
| H      | quality_score | number        | No       | Score from quality gate (0-25)                      |
| I      | status        | enum          | Yes      | `draft`, `reviewed`, `refined`, `approved`          |
| J      | created_at    | ISO timestamp | Yes      | When content was generated                          |

**Platform Values:** `twitter`, `linkedin`, `newsletter`  
**Status Values:** `draft`, `reviewed`, `refined`, `approved`

**Example Row:**

```
| 1733712000000-0-twitter-1 | 1733712000000-0 | twitter | tweet | Most AI projects fail... | Full tweet text here | | 18 | reviewed | 2024-12-09T00:01:00.000Z |
```

---

## Sheet 4: Quality_Logs

Stores quality scoring details for each content piece.

| Column | Name              | Type          | Required | Description                                |
| ------ | ----------------- | ------------- | -------- | ------------------------------------------ |
| A      | log_id            | string        | Yes      | Unique ID (format: `{content_id}-quality`) |
| B      | content_id        | string        | Yes      | Foreign key to Generated_Content           |
| C      | hook_score        | number        | Yes      | Score 1-5 for hook clarity                 |
| D      | specificity_score | number        | Yes      | Score 1-5 for specificity                  |
| E      | voice_score       | number        | Yes      | Score 1-5 for voice authenticity           |
| F      | value_score       | number        | Yes      | Score 1-5 for value density                |
| G      | cta_score         | number        | Yes      | Score 1-5 for CTA naturalness              |
| H      | total_score       | number        | Yes      | Sum of all scores (5-25)                   |
| I      | pass              | boolean       | Yes      | Whether content passed threshold           |
| J      | feedback          | string        | No       | Quality critique feedback                  |
| K      | timestamp         | ISO timestamp | Yes      | When quality check was performed           |

**Example Row:**

```
| 1733712000000-0-twitter-1-quality | 1733712000000-0-twitter-1 | 4 | 3 | 4 | 4 | 3 | 18 | TRUE | Good hook, could use more specifics | 2024-12-09T00:02:00.000Z |
```

---

## Sheet 5: Config (Optional)

Stores configuration values for the workflow.

| Column | Name    | Type   | Description         |
| ------ | ------- | ------ | ------------------- |
| A      | setting | string | Configuration key   |
| B      | value   | string | Configuration value |

**Default Configuration:**

```
| quality_threshold_twitter | 16 |
| quality_threshold_linkedin | 18 |
| quality_threshold_newsletter | 20 |
| max_refine_attempts | 2 |
| tweets_per_video | 5 |
| linkedin_per_video | 3 |
| newsletter_per_video | 1 |
```

---

## Data Validation Rules

### Platform Column (Generated_Content.C)

- Dropdown: `twitter`, `linkedin`, `newsletter`

### Status Column (Generated_Content.I)

- Dropdown: `draft`, `reviewed`, `refined`, `approved`

### Score Columns (Quality_Logs.C-G)

- Number validation: 1-5 only

### Total Score Column (Quality_Logs.H)

- Formula could be used: `=SUM(C:G)` or calculated by n8n

---

## Column Formatting

### All Sheets - Row 1 (Headers)

- **Bold**
- **Freeze Row 1**
- **Background:** Light gray (#f3f4f6)

### Transcript Column (Raw_Transcripts.D)

- **Column Width:** Wide (300px+)
- **Text Wrap:** Enabled

### JSON Columns

- **Column Width:** Medium (200px)
- **Text Wrap:** Enabled

---

## Quick Setup Script (Manual)

When creating the spreadsheet:

1. Create new Google Sheet
2. Rename "Sheet1" to "Raw_Transcripts"
3. Add headers from table above
4. Create "Ideas_Extracted" sheet with headers
5. Create "Generated_Content" sheet with headers
6. Create "Quality_Logs" sheet with headers
7. (Optional) Create "Config" sheet with defaults
8. Format all headers (bold, freeze, gray background)
9. Add data validation to platform and status columns

---

## n8n Column Mapping Reference

When configuring Google Sheets nodes in n8n, use these mappings:

### Append to Raw_Transcripts:

```javascript
{
  video_id: {{ $json.video_id }},
  video_title: {{ $json.video_title }},
  video_url: {{ $json.video_url || '' }},
  transcript: {{ $json.transcript }},
  metadata: {{ JSON.stringify({
    niche: $json.niche || 'AI/Business',
    target_audience: $json.target_audience || 'Entrepreneurs',
    tone: $json.tone || 'practical',
    platforms: $json.platforms || ['twitter', 'linkedin', 'newsletter'],
    tweet_count: $json.tweet_count || 5,
    linkedin_count: $json.linkedin_count || 3,
    newsletter_count: $json.newsletter_count || 1
  }) }},
  created_at: {{ $now.toISO() }}
}
```

### Append to Generated_Content:

```javascript
{
  content_id: {{ $json.content_id }},
  video_id: {{ $json.video_id }},
  platform: {{ $json.platform }},
  content_type: {{ $json.content_type }},
  hook: {{ $json.hook }},
  body: {{ $json.body }},
  cta: {{ $json.cta || '' }},
  quality_score: {{ $json.quality_score || '' }},
  status: {{ $json.status }},
  created_at: {{ $json.created_at }}
}
```

---

_This schema is versioned with the codebase and serves as the source of truth for sheet structure._
