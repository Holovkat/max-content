# Shard 10: Quality Gate Implementation

## Content Repurposing Engine

**Est. Time:** 45-60 min | **Depends on:** Shards 07-09 | **Outcome:** Content scored and refined

---

## Overview

The Quality Gate adds a second LLM pass to critique and optionally refine each piece of content.

**Thresholds:** Twitter: 16/25, LinkedIn: 18/25, Newsletter: 20/25

---

## Tasks

### 10.1 Merge Content Branches

1. [ ] All three generation branches (Twitter, LinkedIn, Newsletter) should merge
2. [ ] Add **Merge** node after all Store nodes
3. [ ] Name: `Merge All Content`
4. [ ] Mode: Wait for all inputs

### 10.2 Add Loop for Quality Check

1. [ ] After Merge, add **Split In Batches** node
2. [ ] Batch Size: 1 (process each content item individually)
3. [ ] Name: `Process Each Content`

### 10.3 Add Gemini Critique Node

1. [ ] After Split, add **Google Gemini Chat Model**
2. [ ] Name: `Quality Critique`
3. [ ] Temperature: `0.3` (more deterministic for scoring)

Prompt:

```
Score this content on 5 criteria (1-5 each):

CONTENT:
Platform: {{$json.platform}}
Body: {{$json.body}}

CRITERIA:
1. Hook Clarity - Does it stop the scroll? (1=generic, 5=compelling)
2. Specificity - Concrete examples/numbers? (1=vague, 5=specific)
3. Voice - Sounds human, not AI? (1=robotic, 5=authentic)
4. Value - Every sentence earns place? (1=filler, 5=dense)
5. CTA - Natural, not pushy? (1=desperate, 5=genuine)

Return ONLY JSON:
{
  "scores": {"hook": N, "specificity": N, "voice": N, "value": N, "cta": N},
  "total": N,
  "pass": true/false,
  "feedback": "1-2 sentences on main improvement needed"
}

Threshold: twitter=16, linkedin=18, newsletter=20
```

### 10.4 Add Parse Quality Code Node

Name: `Parse Quality`

```javascript
const response = $input.all()[0].json.text || $input.all()[0].json.content;
const content = $("Process Each Content").first().json;

let quality;
try {
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  quality = JSON.parse(jsonMatch[0]);
} catch (e) {
  quality = {
    scores: { hook: 3, specificity: 3, voice: 3, value: 3, cta: 3 },
    total: 15,
    pass: false,
  };
}

// Determine threshold
const thresholds = { twitter: 16, linkedin: 18, newsletter: 20 };
const threshold = thresholds[content.platform] || 16;
quality.pass = quality.total >= threshold;

return [
  {
    json: {
      ...content,
      quality_score: quality.total,
      quality_pass: quality.pass,
      quality_feedback: quality.feedback,
      quality_scores: quality.scores,
    },
  },
];
```

### 10.5 Add IF Node for Refinement Decision

1. [ ] Add **IF** node after Parse Quality
2. [ ] Condition: `{{ $json.quality_pass }}` equals `false`
3. [ ] True branch → Refinement
4. [ ] False branch → Skip to storage

### 10.6 Add Refinement Node (Optional Path)

1. [ ] On True (needs refinement), add **Google Gemini Chat Model**
2. [ ] Name: `Refine Content`
3. [ ] Prompt:

```
Improve this content based on feedback:

ORIGINAL: {{$json.body}}
PLATFORM: {{$json.platform}}
FEEDBACK: {{$json.quality_feedback}}
SCORES: {{JSON.stringify($json.quality_scores)}}

Return ONLY the improved content text, nothing else.
```

### 10.7 Update Quality Log

1. [ ] Add **Google Sheets** node (both branches merge here)
2. [ ] Name: `Log Quality`
3. [ ] Sheet: `Quality_Logs`
4. [ ] Map: log_id, content_id, scores, total_score, pass, feedback, timestamp

### 10.8 Update Generated Content Status

1. [ ] Add **Google Sheets** node
2. [ ] Operation: **Update Row**
3. [ ] Match on content_id
4. [ ] Update: quality_score, status (draft→reviewed or refined)

---

## Verification

- [ ] Execute full workflow
- [ ] Quality_Logs sheet has entries for each content piece
- [ ] Content with low scores shows refinement attempt
- [ ] Generated_Content shows quality_score values

**→ Next: Shard 11: Testing & Refinement**
