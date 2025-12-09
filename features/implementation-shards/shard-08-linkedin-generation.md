# Shard 08: LinkedIn Generation

## Content Repurposing Engine

**Est. Time:** 30-45 min | **Depends on:** Shard 06 | **Outcome:** 3 LinkedIn posts generated

---

## Tasks

### 8.1 Add Gemini Node for LinkedIn

1. [ ] From `Parse Ideas JSON` (parallel to Twitter branch), add **Google Gemini Chat Model**
2. [ ] Name: `Generate LinkedIn`
3. [ ] Model: `gemini-1.5-flash`, Temperature: `0.7`

### 8.2 Configure Prompt

```
Create 3 LinkedIn posts in Liam Ottley's voice - professional but direct, use white space.

VIDEO: {{$json.video_title}}
IDEAS: {{JSON.stringify($json.ideas, null, 2)}}

STRUCTURE per post:
- Lines 1-2: Hook that stops scroll
- Lines 3-15: Core insight with specifics
- Final 2 lines: TL;DR + question for engagement

Return ONLY JSON:
{
  "posts": [
    {
      "hook": "First 2 lines",
      "body": "Full post with line breaks",
      "cta": "Closing question",
      "type": "lesson|framework|story"
    }
  ]
}

Rules: 1200-1800 chars, one idea per line, include numbers/examples, end with genuine question.
```

### 8.3 Add Parse Code Node

Name: `Parse LinkedIn`

```javascript
const response = $input.all()[0].json.text || $input.all()[0].json.content;
let data;
try {
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  data = JSON.parse(jsonMatch[0]);
} catch (e) {
  data = { posts: [] };
}

const meta = $("Parse Ideas JSON").first().json;
return data.posts.map((p, i) => ({
  json: {
    content_id: `${meta.video_id}-linkedin-${i + 1}`,
    video_id: meta.video_id,
    platform: "linkedin",
    hook: p.hook,
    body: p.body,
    cta: p.cta,
    status: "draft",
    created_at: new Date().toISOString(),
  },
}));
```

### 8.4 Add Google Sheets Node

- Name: `Store LinkedIn`
- Sheet: `Generated_Content`
- Map: content_id, video_id, platform, hook, body, cta, status, created_at

---

## Verification

- [ ] Execute workflow
- [ ] 3 LinkedIn posts in Generated_Content sheet
- [ ] Posts use white space, have hook/body/CTA structure

**→ Next: Shard 09: Newsletter Generation**
