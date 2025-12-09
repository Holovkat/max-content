# Multi-Model Architecture

## Content Repurposing Engine

This document describes the multi-model LLM orchestration strategy.

---

## Overview

The Content Repurposing Engine uses a **3-model ensemble approach**:

| Model      | Provider | Role                          |
| ---------- | -------- | ----------------------------- |
| **GLM-4**  | Zhipu AI | Idea extraction (creative)    |
| **Groq**   | Groq     | Content generation (fast)     |
| **Gemini** | Google   | Curation, ranking, web search |

---

## Model Roles

### GLM-4 (Idea Extraction)

| Attribute | Value                                              |
| --------- | -------------------------------------------------- |
| Provider  | Zhipu AI                                           |
| Model     | `glm-4-plus` or `glm-4.6`                          |
| Role      | Creative idea extraction from transcripts          |
| Strengths | Nuanced understanding, creative insight extraction |

**API Endpoints (use the one matching your account):**
| Account Type | Endpoint |
|--------------|----------|
| CodePlan (z.ai) | `https://api.z.ai/api/paas/v4/chat/completions` |
| BigModel (China) | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |

**Used for:**

- Idea extraction from transcripts
- Identifying key insights, quotes, frameworks, stories

---

### Groq (Content Generation)

| Attribute | Value                                             |
| --------- | ------------------------------------------------- |
| Provider  | Groq                                              |
| Model     | `llama-3.1-70b-versatile` or `mixtral-8x7b-32768` |
| Endpoint  | `https://api.groq.com/openai/v1/chat/completions` |
| Role      | Fast content generation                           |
| Strengths | Extremely fast inference, good quality output     |

**Free Tier:** 30 requests/minute, 14,400 requests/day

**Used for:**

- Tweet generation (5 tweets)
- LinkedIn post generation (3 posts)
- Newsletter generation (1 section)

---

### Gemini (Curator & Quality Gate)

| Attribute | Value                                       |
| --------- | ------------------------------------------- |
| Provider  | Google AI                                   |
| Model     | `gemini-1.5-flash`                          |
| Endpoint  | Native n8n node                             |
| Role      | Quality curation, ranking, and web search   |
| Strengths | Fast, analytical, grounding with web search |

**Free Tier:** 15 RPM, 1M tokens/day

**Used for:**

- Quality scoring (1-5 rubric on 5 dimensions)
- Content refinement suggestions
- **Web search for references/fact-checking**
- Final quality gate pass/fail
- Curating best outputs when multiple exist

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
   - Value: `Bearer YOUR_GLM4_API_KEY`

---

### HTTP Request Node for Groq

| Setting        | Value                                             |
| -------------- | ------------------------------------------------- |
| Method         | POST                                              |
| URL            | `https://api.groq.com/openai/v1/chat/completions` |
| Authentication | Header Auth                                       |
| Header Name    | Authorization                                     |
| Header Value   | `Bearer YOUR_GROQ_API_KEY`                        |
| Content-Type   | application/json                                  |

### Groq Request Body

```json
{
  "model": "llama-3.1-70b-versatile",
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
  "max_tokens": 2048
}
```

### Groq Credential Setup

1. Go to [console.groq.com](https://console.groq.com)
2. Create API key
3. In n8n, create **Header Auth** credential:
   - Name: `Groq API`
   - Name: `Authorization`
   - Value: `Bearer YOUR_GROQ_API_KEY`

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
