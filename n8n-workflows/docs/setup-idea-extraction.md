# Workflow Setup: Idea Extraction

## Shard 06 - Implementation Guide

This document provides instructions for adding the Idea Extraction nodes to your workflow.

---

## Overview

The idea extraction phase uses Gemini to analyze the transcript and extract:

- **Key Ideas** (4-6) - Core insights for content
- **Quotable Moments** (3-5) - Memorable phrases
- **Frameworks** (1-3) - Methods/processes mentioned
- **Stories** (1-2) - Anecdotes and examples

---

## Workflow Addition

Add these nodes after `Store Raw Transcript`:

```
┌─────────────────────┐     ┌──────────────┐     ┌─────────────┐     ┌─────────────┐
│  Store Raw          │────▶│  Extract     │────▶│  Parse      │────▶│  Store      │
│  Transcript         │     │  Ideas       │     │  Ideas      │     │  Ideas      │
│  (existing)         │     │  (Gemini)    │     │  (Code)     │     │  (Sheets)   │
└─────────────────────┘     └──────────────┘     └─────────────┘     └─────────────┘
```

---

## Node 1: Extract Ideas (Gemini)

### Setup

1. Add **Google Gemini Chat Model** node after `Store Raw Transcript`
2. Name: `Extract Ideas`
3. Connect credential: Your Gemini API credential

### Configuration

| Setting           | Value              |
| ----------------- | ------------------ |
| Model             | `gemini-1.5-flash` |
| Temperature       | `0.7`              |
| Max Output Tokens | `4096`             |

### Prompt

Copy the content from `prompts/idea-extraction.md` into the User Message field.

**Variable substitution in n8n:**
Replace the template variables with n8n expressions:

| Template              | n8n Expression                |
| --------------------- | ----------------------------- |
| `{{video_title}}`     | `{{ $json.video_title }}`     |
| `{{niche}}`           | `{{ $json.niche }}`           |
| `{{target_audience}}` | `{{ $json.target_audience }}` |
| `{{tone}}`            | `{{ $json.tone }}`            |
| `{{transcript}}`      | `{{ $json.transcript }}`      |

### Full Prompt (n8n ready)

```
You are a senior content strategist at The Atlantic who also deeply understands the AI automation and startup space.

## CONTEXT

Video Title: {{ $json.video_title }}
Content Niche: {{ $json.niche }}
Target Audience: {{ $json.target_audience }}
Tone: {{ $json.tone }}

## TRANSCRIPT

"""
{{ $json.transcript }}
"""

## TASK

Analyze this transcript and extract content for repurposing. Return ONLY valid JSON (no markdown, no explanation).

{
  "key_ideas": [
    {
      "title": "Brief insight title",
      "insight": "Core insight in 1-2 sentences",
      "evidence": "Supporting quote from transcript",
      "platforms": ["twitter", "linkedin"]
    }
  ],
  "quotable_moments": [
    {
      "quote": "Memorable quote from transcript",
      "context": "Why this is powerful",
      "type": "contrarian | framework | tactical | emotional | numerical"
    }
  ],
  "frameworks": [
    {
      "name": "Framework name",
      "steps": ["Step 1", "Step 2", "Step 3"],
      "application": "When to use this"
    }
  ],
  "stories": [
    {
      "summary": "Brief story summary",
      "lesson": "What it teaches",
      "emotional_hook": "Why it resonates"
    }
  ]
}

Extract 4-6 key ideas, 3-5 quotes, 1-3 frameworks, 1-2 stories.
Return ONLY the JSON object.
```

---

## Node 2: Parse Ideas (Code)

### Setup

1. Add **Code** node after `Extract Ideas`
2. Name: `Parse Ideas`
3. Mode: `Run Once for All Items`
4. Language: JavaScript

### Code

Copy the content from `code-nodes/parse-ideas.js` into the Code field.

---

## Node 3: Store Ideas (Google Sheets)

### Setup

1. Add **Google Sheets** node after `Parse Ideas`
2. Name: `Store Ideas`
3. Connect credential: Your Google Sheets credential

### Configuration

| Setting   | Value                      |
| --------- | -------------------------- |
| Operation | Append Row                 |
| Document  | Content Repurposing Engine |
| Sheet     | Ideas_Extracted            |

### Column Mapping

| Column           | Expression                                            |
| ---------------- | ----------------------------------------------------- |
| idea_id          | `={{ $json.video_id }}-ideas`                         |
| video_id         | `={{ $json.video_id }}`                               |
| idea_title       | `=Extracted Ideas`                                    |
| key_ideas        | `={{ JSON.stringify($json.ideas.key_ideas) }}`        |
| quotable_moments | `={{ JSON.stringify($json.ideas.quotable_moments) }}` |
| frameworks       | `={{ JSON.stringify($json.ideas.frameworks) }}`       |

---

## Testing

### Test with Sample Data

1. Execute workflow from Form Trigger with test transcript
2. Check `Extract Ideas` output - should show JSON
3. Check `Parse Ideas` output - should show structured ideas
4. Check Google Sheets - row should appear in Ideas_Extracted

### Expected Output Structure

```json
{
  "video_id": "1733712000000-0",
  "video_title": "How to Automate Any Business",
  "ideas": {
    "key_ideas": [...],
    "quotable_moments": [...],
    "frameworks": [...],
    "stories": [...]
  },
  "extraction_counts": {
    "key_ideas": 5,
    "quotable_moments": 4,
    "frameworks": 2,
    "stories": 1
  }
}
```

---

## Troubleshooting

### Gemini returns error

- Check API key is valid
- Verify free tier limits (15 RPM, 1M tokens/day)
- Reduce transcript length if very long

### JSON parsing fails

- Check the Parse Ideas node output for `_parse_error`
- Gemini may wrap JSON in markdown - the code handles this
- Check `_raw_response` for debugging

### Empty ideas returned

- Transcript may be too short
- Check the prompt is complete
- Verify transcript contains actual content

### Rate limiting

- Add a **Wait** node (2s) before Gemini if hitting limits
- Consider batching for multiple runs

---

## Connections

After this node is working, it connects to:

- Shard 07: Twitter Generation
- Shard 08: LinkedIn Generation
- Shard 09: Newsletter Generation

The `Parse Ideas` output contains everything needed for content generation.

---

_This node is the "intelligence" layer - quality here affects all generated content._
