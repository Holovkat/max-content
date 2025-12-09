# Shard 07: Twitter Generation

## Content Repurposing Engine

**Est. Time:** 30-45 min | **Depends on:** Shard 06 | **Outcome:** 5 tweets generated

---

## Tasks

### 7.1 Add Gemini Node for Twitter

1. [ ] From `Parse Ideas JSON`, add **Google Gemini Chat Model** node
2. [ ] Name: `Generate Tweets`
3. [ ] Model: `gemini-1.5-flash`, Temperature: `0.8`

### 7.2 Configure Prompt

Set User Message (see `/features/voice-dna-framework.md` for full prompt):

```
Create 5 tweets in Liam Ottley's voice - direct, practical, numbers-focused.

VIDEO: {{$json.video_title}}
IDEAS: {{JSON.stringify($json.ideas, null, 2)}}

Return ONLY JSON:
{
  "tweets": [
    {"content": "Tweet text (max 280 chars)", "type": "contrarian|tactical|mistake|framework|observation"}
  ]
}

Rules: Under 280 chars, specific not generic, mix of types, no emoji spam.
```

### 7.3 Add Parse Code Node

Name: `Parse Tweets`

```javascript
const response = $input.all()[0].json.text || $input.all()[0].json.content;
let data;
try {
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  data = JSON.parse(jsonMatch[0]);
} catch (e) {
  data = { tweets: [] };
}

const meta = $("Parse Ideas JSON").first().json;
return data.tweets.map((t, i) => ({
  json: {
    content_id: `${meta.video_id}-twitter-${i + 1}`,
    video_id: meta.video_id,
    platform: "twitter",
    body: t.content,
    status: "draft",
    created_at: new Date().toISOString(),
  },
}));
```

### 7.4 Add Google Sheets Node

- Name: `Store Tweets`
- Sheet: `Generated_Content`
- Map: content_id, video_id, platform, body, status, created_at

---

## Verification

- [ ] Execute workflow with test data
- [ ] 5 tweets appear in Generated_Content sheet
- [ ] Tweets are under 280 chars and specific

**→ Next: Shard 08: LinkedIn Generation**
