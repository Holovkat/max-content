# Workflow Setup: Parallel Content Generation

## Shard 07 - Implementation Guide

This document provides instructions for setting up parallel content generation with GLM-4.6 and Kimi-K2, followed by Gemini curation.

---

## Overview

```
                     PARALLEL GENERATION

     ┌───────────────────────────────────────────────────────┐
     │                                                       │
     │   ┌────────────────┐      ┌────────────────┐         │
     │   │  GLM-4.6       │      │  Kimi-K2       │         │
     │   │  Generator     │      │  Generator     │         │
     │   │                │      │                │         │
     │   │  • Tweets      │      │  • Tweets      │         │
     │   │  • LinkedIn    │      │  • LinkedIn    │         │
     │   │  • Newsletter  │      │  • Newsletter  │         │
     │   └───────┬────────┘      └───────┬────────┘         │
     │           │                       │                   │
     │           └───────────┬───────────┘                   │
     │                       ▼                               │
     │            ┌────────────────────┐                     │
     │            │  Gemini Curator    │                     │
     │            │  + Web Search      │                     │
     │            └─────────┬──────────┘                     │
     │                      ▼                                │
     │            ┌────────────────────┐                     │
     │            │  Final Curated     │                     │
     │            │  Content           │                     │
     │            └────────────────────┘                     │
     │                                                       │
     └───────────────────────────────────────────────────────┘
```

---

## Workflow Structure in n8n

After `Parse Ideas`, the workflow splits into parallel branches:

```
Parse Ideas
    │
    ├──────────────────────┬──────────────────────┐
    ▼                      ▼                      ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│ Twitter │          │LinkedIn │          │Newsletter
│ Branch  │          │ Branch  │          │ Branch  │
└────┬────┘          └────┬────┘          └────┬────┘
     │                    │                    │
     │   (Each branch has GLM + Kimi parallel) │
     │                    │                    │
     ├────────────────────┼────────────────────┤
     ▼                    ▼                    ▼
┌─────────────────────────────────────────────────┐
│              Merge All Content                   │
└─────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│              Gemini Curator                      │
│              (compares, picks best, web search)  │
└─────────────────────────────────────────────────┘
     │
     ▼
┌─────────────────────────────────────────────────┐
│              Store Final Content                 │
└─────────────────────────────────────────────────┘
```

---

## Node Setup: Twitter Generation (Parallel)

### GLM-4.6 Twitter Node

1. Add **HTTP Request** node
2. Name: `Generate Tweets (GLM-4.6)`
3. Configure:
   - Method: POST
   - URL: `https://api.z.ai/api/paas/v4/chat/completions`
   - Auth: Header Auth (GLM-4 API credential)

4. Request Body:

```json
{
  "model": "glm-4.6",
  "messages": [
    {
      "role": "user",
      "content": "{{ See prompts/twitter-generation.md }}"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### Kimi-K2 Twitter Node

1. Add **HTTP Request** node (parallel to GLM)
2. Name: `Generate Tweets (Kimi-K2)`
3. Configure:
   - Method: POST
   - URL: `https://api.groq.com/openai/v1/chat/completions`
   - Auth: Header Auth (Groq API credential)

4. Request Body:

```json
{
  "model": "moonshotai/kimi-k2-instruct-0905",
  "messages": [
    {
      "role": "user",
      "content": "{{ See prompts/twitter-generation.md }}"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 2048
}
```

### Parse Both Outputs

Add Code nodes after each generator:

- `Parse Tweets (GLM)` - Uses `code-nodes/parse-tweets.js`
- `Parse Tweets (Kimi)` - Uses same code

Add `_generator` field in Code node to track source.

---

## Node Setup: LinkedIn Generation (Parallel)

Same pattern as Twitter:

1. `Generate LinkedIn (GLM-4.6)` - HTTP Request
2. `Generate LinkedIn (Kimi-K2)` - HTTP Request (parallel)
3. `Parse LinkedIn (GLM)` - Code node
4. `Parse LinkedIn (Kimi)` - Code node

Use `prompts/linkedin-generation.md` for the prompt.

---

## Node Setup: Newsletter Generation (Parallel)

Same pattern:

1. `Generate Newsletter (GLM-4.6)` - HTTP Request
2. `Generate Newsletter (Kimi-K2)` - HTTP Request (parallel)
3. `Parse Newsletter (GLM)` - Code node
4. `Parse Newsletter (Kimi)` - Code node

Use `prompts/newsletter-generation.md` for the prompt.

---

## Node Setup: Merge All Content

1. Add **Merge** node
2. Name: `Merge All Content`
3. Mode: `Combine` (All inputs together)
4. Connect all 6 parse nodes to this merge

---

## Node Setup: Gemini Curator

1. Add **Google Gemini Chat Model** node
2. Name: `Curate Content`
3. Model: `gemini-1.5-flash`
4. Enable: `Web Search` (if available in n8n Gemini node)

5. Prompt constructed to include:
   - All GLM outputs as "Generator A"
   - All Kimi outputs as "Generator B"
   - Instructions from `prompts/gemini-curation.md`

### Curation Prompt Template

```
You are the Curator...

## OUTPUTS FROM GENERATOR A (GLM-4.6)
{{ JSON.stringify($json.glm_outputs) }}

## OUTPUTS FROM GENERATOR B (Kimi-K2)
{{ JSON.stringify($json.kimi_outputs) }}

{{ Rest of prompts/gemini-curation.md }}
```

---

## Node Setup: Parse & Store Curated

1. Add **Code** node after Gemini
2. Name: `Parse Curated`
3. Use: `code-nodes/parse-curated.js`

4. Add **Google Sheets** node
5. Name: `Store Final Content`
6. Sheet: `Generated_Content`
7. Map curated content to columns

---

## Variable Substitution Reference

For all generation prompts, replace:

| Template              | n8n Expression                      |
| --------------------- | ----------------------------------- |
| `{{video_title}}`     | `{{ $json.video_title }}`           |
| `{{niche}}`           | `{{ $json.niche }}`                 |
| `{{target_audience}}` | `{{ $json.target_audience }}`       |
| `{{tone}}`            | `{{ $json.tone }}`                  |
| `{{ideas_json}}`      | `{{ JSON.stringify($json.ideas) }}` |
| `{{tweet_count}}`     | `{{ $json.tweet_count }}`           |
| `{{linkedin_count}}`  | `{{ $json.linkedin_count }}`        |
| `{{video_url}}`       | `{{ $json.video_url }}`             |

---

## Testing

### Test Each Branch

1. Execute workflow with test transcript
2. Check GLM-4.6 response - should return JSON with tweets
3. Check Kimi-K2 response - should return JSON with tweets
4. Check Parse nodes - should extract structured content
5. Check Merge - should combine all outputs
6. Check Gemini Curator - should pick best versions
7. Check Sheets - should have final curated content

### Expected Output

For each run, you should end up with:

- 5 curated tweets (best from either generator)
- 3 curated LinkedIn posts
- 1 curated newsletter section

Plus metadata showing which generator won each piece.

---

## Troubleshooting

### Generator returns error

- Check API credentials
- Verify model name is correct
- Check rate limits

### Parallel nodes not running

- Ensure nodes are connected in parallel (not series)
- Check n8n execution settings

### Curation fails

- Verify both generator outputs are being passed
- Check JSON formatting in Gemini prompt

---

_Parallel generation enables best-of-both-worlds content quality._
