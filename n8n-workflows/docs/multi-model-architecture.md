# Multi-Model Architecture

## Content Repurposing Engine

This document describes the multi-model LLM orchestration strategy.

---

## Overview

The Content Repurposing Engine uses a **parallel generation + curation approach**:

| Model       | Provider             | Role                                      |
| ----------- | -------------------- | ----------------------------------------- |
| **GLM-4.6** | Zhipu AI             | Parallel generator (ideas + content)      |
| **Kimi-K2** | Moonshot AI via Groq | Parallel generator (ideas + content)      |
| **Gemini**  | Google               | Curator, ranker, web search, final output |

**How it works:**

1. Both GLM-4.6 and Kimi-K2 independently generate ideas and content
2. Gemini compares both outputs and curates the best
3. Gemini can search the web for references if needed
4. Final output is the best-of-both combined

---

## Model Roles

### GLM-4.6 (Parallel Generator A)

| Attribute | Value                                     |
| --------- | ----------------------------------------- |
| Provider  | Zhipu AI                                  |
| Model     | `glm-4.6`                                 |
| Role      | Creative generation (ideas + all content) |
| Strengths | Nuanced understanding, creative writing   |

**API Endpoints (use the one matching your account):**
| Account Type | Endpoint |
|--------------|----------|
| CodePlan (z.ai) | `https://api.z.ai/api/paas/v4/chat/completions` |
| BigModel (China) | `https://open.bigmodel.cn/api/paas/v4/chat/completions` |

**Generates:**

- Idea extraction (key ideas, quotes, frameworks, stories)
- 5 Tweets
- 3 LinkedIn posts
- 1 Newsletter section

---

### Kimi-K2 (Parallel Generator B)

| Attribute | Value                                             |
| --------- | ------------------------------------------------- |
| Provider  | Moonshot AI (via Groq)                            |
| Model     | `moonshotai/kimi-k2-instruct-0905`                |
| Endpoint  | `https://api.groq.com/openai/v1/chat/completions` |
| Role      | Creative generation (ideas + all content)         |
| Strengths | Strong reasoning, different creative perspective  |

**Free Tier:** 30 requests/minute via Groq

**Generates:**

- Idea extraction (key ideas, quotes, frameworks, stories)
- 5 Tweets
- 3 LinkedIn posts
- 1 Newsletter section

---

### Gemini (Curator & Editor)

| Attribute | Value                                      |
| --------- | ------------------------------------------ |
| Provider  | Google AI                                  |
| Model     | `gemini-1.5-flash`                         |
| Endpoint  | Native n8n node                            |
| Role      | Curate, rank, web search, finalize         |
| Strengths | Fast analytical, grounding with web search |

**Free Tier:** 15 RPM, 1M tokens/day

**Responsibilities:**

- Compare outputs from GLM-4.6 and Kimi-K2
- Pick the best version of each content piece
- Optionally merge/combine best elements from both
- Search web for references to validate claims
- Quality score final selections
- Produce the final curated output

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

### HTTP Request Node for Kimi-K2 (via Groq)

| Setting        | Value                                             |
| -------------- | ------------------------------------------------- |
| Method         | POST                                              |
| URL            | `https://api.groq.com/openai/v1/chat/completions` |
| Authentication | Header Auth                                       |
| Header Name    | Authorization                                     |
| Header Value   | `Bearer YOUR_GROQ_API_KEY`                        |
| Content-Type   | application/json                                  |

### Kimi-K2 Request Body

```json
{
  "model": "moonshotai/kimi-k2-instruct-0905",
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

### Groq/Kimi-K2 Credential Setup

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
