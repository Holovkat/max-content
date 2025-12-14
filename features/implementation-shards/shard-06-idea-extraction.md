# Shard 06: Idea Extraction Node - ✅ COMPLETE

## Content Repurposing Engine

**Status:** ✅ Completed  
**Implementation:** Part of unified generation in `content-generator.json`

---

## What Was Planned

- Separate Gemini node for idea extraction
- Parse and store in Ideas_Extracted sheet
- Separate step before content generation

## What Was Actually Built

Idea extraction is **combined with content generation** in a single LLM call:

### Single "Generate Content" Node

The Gemini node generates both ideas AND content in one call:

```json
{
  "key_ideas": [
    "First key insight from content",
    "Second key insight from content",
    "Third key insight from content"
  ],
  "tweets": [ ... ],
  "linkedin": { ... },
  "newsletter": { ... },
  "instagram": [ ... ],
  "skool": { ... }
}
```

### Benefits of Combined Approach

| Separate Extraction           | Combined Generation      |
| ----------------------------- | ------------------------ |
| 2+ API calls                  | 1 API call               |
| More latency                  | Faster response          |
| Ideas may differ from content | Ideas align with content |
| More complex workflow         | Simpler workflow         |

---

## Key Ideas in Output

The `key_ideas` array appears in:

1. **Preview page** - "Key Ideas" section
2. **Confirmation page** - Context for what was generated

Example output:

```json
{
  "key_ideas": [
    "AI automation starts with understanding the problem, not the technology",
    "Three phases: no-code → custom solutions → transformation partner",
    "Start with $100k potential by solving specific business problems"
  ]
}
```

---

## Verification ✅

- [x] Key ideas extracted from content
- [x] Ideas are specific (not generic)
- [x] Ideas inform content generation
- [x] Ideas displayed in preview
- [x] 3-5 ideas typically extracted

---

## Key Files

| File                                         | Purpose                  |
| -------------------------------------------- | ------------------------ |
| `../../n8n-workflows/content-generator.json` | Contains generation node |
| `../../n8n-workflows/prompts/`               | Prompt templates         |

---

**→ Next: Shard 07: Twitter Generation (also complete)**
