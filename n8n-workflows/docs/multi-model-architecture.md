# Multi-Model Architecture

## Content Repurposing Engine

This document describes the multi-model LLM orchestration strategy.

---

## Overview

The Content Repurposing Engine uses multiple AI models in an ensemble approach:

1. **GLM-4 (z.ai)** - Creative extraction and generation
2. **Gemini (Google)** - Curation, ranking, and quality gate

---

## Model Roles

### GLM-4 (Creative Model)

| Attribute | Value                                     |
| --------- | ----------------------------------------- |
| Provider  | Zhipu AI                                  |
| Model     | `glm-4-plus` or `glm-4.6`                 |
| Role      | Primary content extraction and generation |
| Strengths | Creative writing, nuanced understanding   |

**API Endpoints (use the one matching your account):**
| Account Type | Endpoint |
|--------------|----------|
| CodePlan (z.ai) | `https://api.z.ai/api/paas/v4/chat/completions` |
| BigModel (China) | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |

**Used for:**

- Idea extraction from transcripts
- Tweet generation
- LinkedIn post generation
- Newsletter generation

### Gemini (Curator Model)

| Attribute | Value                                           |
| --------- | ----------------------------------------------- |
| Provider  | Google AI                                       |
| Model     | `gemini-1.5-flash`                              |
| Endpoint  | Native n8n node                                 |
| Role      | Quality curation and ranking                    |
| Strengths | Fast, analytical, good at structured evaluation |

**Used for:**

- Quality scoring (1-5 rubric)
- Content refinement suggestions
- Best-of selection when multiple outputs exist
- Final quality gate pass/fail

---

## API Configuration

### GLM-4 Request Format

```bash
curl -X POST "https://api.z.ai/api/paas/v4/chat/completions" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "glm-4-plus",
    "messages": [
      {"role": "system", "content": "You are a content strategist..."},
      {"role": "user", "content": "Analyze this transcript..."}
    ],
    "temperature": 0.7,
    "max_tokens": 4096
  }'
```

### Response Format

```json
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "{ ... JSON response ... }"
      }
    }
  ]
}
```

---

## n8n Integration

### HTTP Request Node for GLM-4

Since n8n doesn't have a native GLM-4 node, use **HTTP Request**:

| Setting        | Value                                           |
| -------------- | ----------------------------------------------- |
| Method         | POST                                            |
| URL            | `https://api.z.ai/api/paas/v4/chat/completions` |
| Authentication | Header Auth                                     |
| Header Name    | Authorization                                   |
| Header Value   | `Bearer {{$credentials.glm4ApiKey}}`            |
| Content-Type   | application/json                                |

### Request Body

```json
{
  "model": "glm-4-plus",
  "messages": [
    {
      "role": "system",
      "content": "{{ $json.systemPrompt }}"
    },
    {
      "role": "user",
      "content": "{{ $json.userPrompt }}"
    }
  ],
  "temperature": 0.7,
  "max_tokens": 4096
}
```

### Credential Setup

1. In n8n, go to **Settings → Credentials**
2. Create **Header Auth** credential:
   - Name: `GLM-4 API`
   - Name: `Authorization`
   - Value: `Bearer YOUR_API_KEY_HERE`

---

## Workflow Flow

```
┌────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│ Set Metadata   │────▶│ Store Transcript│────▶│ Extract Ideas   │
│                │     │ (Sheets)        │     │ (GLM-4)         │
└────────────────┘     └─────────────────┘     └────────┬────────┘
                                                        │
                                                        ▼
┌─────────────────┐     ┌─────────────────┐     ┌───────────────┐
│ Store Ideas     │◀────│ Curate Ideas    │◀────│ Parse GLM-4   │
│ (Sheets)        │     │ (Gemini)        │     │ Response      │
└────────┬────────┘     └─────────────────┘     └───────────────┘
         │
         ▼
┌─────────────────────────────────────────────────────────────────┐
│              CONTENT GENERATION (GLM-4 for each)                │
│  ┌─────────┐     ┌─────────────┐     ┌──────────────┐          │
│  │ Tweets  │     │  LinkedIn   │     │  Newsletter  │          │
│  │ (GLM-4) │     │  (GLM-4)    │     │  (GLM-4)     │          │
│  └────┬────┘     └──────┬──────┘     └───────┬──────┘          │
└───────┼─────────────────┼────────────────────┼──────────────────┘
        │                 │                    │
        └────────────────┬┴────────────────────┘
                         ▼
              ┌─────────────────┐     ┌─────────────────┐
              │ Quality Gate    │────▶│ Store Content   │
              │ (Gemini)        │     │ (Sheets)        │
              └─────────────────┘     └─────────────────┘
```

---

## Cost Implications

| Model  | Free Tier         | Cost After         |
| ------ | ----------------- | ------------------ |
| GLM-4  | Check z.ai limits | Pay per token      |
| Gemini | 1M tokens/day     | Free for hackathon |

**Optimization:** Use GLM-4 for creative work (generation), Gemini for quick analytical tasks (scoring).

---

## Fallback Strategy

If GLM-4 fails or rate limits:

1. Log the error
2. Fall back to Gemini for that step
3. Continue workflow

This ensures the demo never fully breaks.

---

_Multi-model architecture enables best-of-both-worlds content quality._
