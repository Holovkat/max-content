# Workflow Input Schema

## Content Repurposing Engine

This document defines all input parameters accepted by the workflow.

---

## Input Parameters

### Required Fields

| Field         | Type   | Validation    | Description                |
| ------------- | ------ | ------------- | -------------------------- |
| `video_title` | string | Min 3 chars   | Title of the source video  |
| `transcript`  | string | Min 100 chars | Full video transcript text |

### Optional Fields

| Field              | Type   | Default                               | Options   | Description                   |
| ------------------ | ------ | ------------------------------------- | --------- | ----------------------------- |
| `video_url`        | string | `""`                                  | Any URL   | YouTube or source URL         |
| `niche`            | enum   | `"AI/Business"`                       | See below | Target content niche          |
| `target_audience`  | enum   | `"Entrepreneurs"`                     | See below | Who the content is for        |
| `tone`             | enum   | `"practical"`                         | See below | Voice/energy modifier         |
| `platforms`        | array  | `["twitter","linkedin","newsletter"]` | See below | Which platforms to generate   |
| `tweet_count`      | number | `5`                                   | 1-10      | Number of tweets to generate  |
| `linkedin_count`   | number | `3`                                   | 1-5       | Number of LinkedIn posts      |
| `newsletter_count` | number | `1`                                   | 1-2       | Number of newsletter sections |

---

## Field Options

### Niche Options

```
AI/Business       (default)
Entrepreneurship
Tech/Software
Marketing
Finance
Health/Wellness
Education
Other
```

### Target Audience Options

```
Entrepreneurs     (default)
Agency Owners
Developers
Executives
Beginners
Advanced Practitioners
General Audience
```

### Tone Options

```
practical         (default) - Direct, actionable, numbers-focused
inspirational     - Motivating, story-driven, aspirational
controversial     - Contrarian, challenge assumptions, bold
educational       - Teaching-focused, step-by-step, patient
conversational    - Casual, friendly, relatable
```

### Platform Options (Multi-select)

```
twitter           - Generate tweets
linkedin          - Generate LinkedIn posts
newsletter        - Generate newsletter summary
```

---

## JSON Schema

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "required": ["video_title", "transcript"],
  "properties": {
    "video_title": {
      "type": "string",
      "minLength": 3,
      "description": "Title of the source video"
    },
    "video_url": {
      "type": "string",
      "format": "uri",
      "default": "",
      "description": "YouTube or source URL"
    },
    "transcript": {
      "type": "string",
      "minLength": 100,
      "description": "Full video transcript text"
    },
    "niche": {
      "type": "string",
      "enum": [
        "AI/Business",
        "Entrepreneurship",
        "Tech/Software",
        "Marketing",
        "Finance",
        "Health/Wellness",
        "Education",
        "Other"
      ],
      "default": "AI/Business"
    },
    "target_audience": {
      "type": "string",
      "enum": [
        "Entrepreneurs",
        "Agency Owners",
        "Developers",
        "Executives",
        "Beginners",
        "Advanced Practitioners",
        "General Audience"
      ],
      "default": "Entrepreneurs"
    },
    "tone": {
      "type": "string",
      "enum": [
        "practical",
        "inspirational",
        "controversial",
        "educational",
        "conversational"
      ],
      "default": "practical"
    },
    "platforms": {
      "type": "array",
      "items": {
        "type": "string",
        "enum": ["twitter", "linkedin", "newsletter"]
      },
      "default": ["twitter", "linkedin", "newsletter"],
      "minItems": 1
    },
    "tweet_count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 10,
      "default": 5
    },
    "linkedin_count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 5,
      "default": 3
    },
    "newsletter_count": {
      "type": "integer",
      "minimum": 1,
      "maximum": 2,
      "default": 1
    }
  }
}
```

---

## Form Field Mapping

### n8n Form Trigger Configuration

| Field Label     | Field Name        | Type         | Required | Options                       |
| --------------- | ----------------- | ------------ | -------- | ----------------------------- |
| Video Title     | `video_title`     | Text         | Yes      | -                             |
| Video URL       | `video_url`       | Text         | No       | -                             |
| Transcript      | `transcript`      | Textarea     | Yes      | -                             |
| Content Niche   | `niche`           | Dropdown     | No       | See niche options             |
| Target Audience | `target_audience` | Dropdown     | No       | See audience options          |
| Tone            | `tone`            | Dropdown     | No       | See tone options              |
| Platforms       | `platforms`       | Multi-select | No       | twitter, linkedin, newsletter |
| Tweet Count     | `tweet_count`     | Number       | No       | Default: 5                    |
| LinkedIn Count  | `linkedin_count`  | Number       | No       | Default: 3                    |

---

## Webhook Payload Example

```json
{
  "video_title": "How to Automate Any Business With AI in 3 Steps",
  "video_url": "https://youtu.be/kQFW3bUrOu4",
  "transcript": "Today I'm going to show you the three phases of AI automation...",
  "niche": "AI/Business",
  "target_audience": "Entrepreneurs",
  "tone": "practical",
  "platforms": ["twitter", "linkedin", "newsletter"],
  "tweet_count": 5,
  "linkedin_count": 3,
  "newsletter_count": 1
}
```

---

## Internal Fields (Auto-generated)

These fields are NOT user inputs - they're generated by the workflow:

| Field        | How Generated                      | Description       |
| ------------ | ---------------------------------- | ----------------- |
| `video_id`   | `${Date.now()}-${$runIndex}`       | Unique identifier |
| `created_at` | `$now.toISO()`                     | Timestamp         |
| `content_id` | `${video_id}-${platform}-${index}` | Content piece ID  |

---

## Usage in Prompts

The input fields are used to customize AI generation:

```
You are creating content for the {{niche}} space.
Target audience: {{target_audience}}
Tone: {{tone}} - {{tone_description}}
```

### Tone Descriptions for Prompts:

| Tone           | Prompt Modifier                                                |
| -------------- | -------------------------------------------------------------- |
| practical      | "Be direct, actionable, and include specific numbers/examples" |
| inspirational  | "Be motivating, use storytelling, focus on transformation"     |
| controversial  | "Challenge assumptions, be contrarian, make bold statements"   |
| educational    | "Be patient, use step-by-step explanations, define terms"      |
| conversational | "Be casual and friendly, use relateable language"              |

---

_This input schema is versioned with the codebase and serves as the source of truth for workflow inputs._
