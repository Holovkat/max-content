# Shard 09: Newsletter Generation

## Content Repurposing Engine

**Est. Time:** 30-45 min | **Depends on:** Shard 06 | **Outcome:** 1 newsletter section generated

---

## Tasks

### 9.1 Add Gemini Node for Newsletter

1. [ ] From `Parse Ideas JSON` (parallel to other branches), add **Google Gemini Chat Model**
2. [ ] Name: `Generate Newsletter`
3. [ ] Model: `gemini-1.5-flash`, Temperature: `0.6`

### 9.2 Configure Prompt

```
Create 1 newsletter section summarizing this video for Liam Ottley's audience.

VIDEO: {{$json.video_title}}
URL: {{$json.video_url}}
IDEAS: {{JSON.stringify($json.ideas, null, 2)}}

STRUCTURE:
1. Opening hook (2-3 sentences setting context)
2. Key insight paragraph
3. 3-5 actionable takeaways (bullet points)
4. Framework summary if applicable
5. Soft CTA (reply, watch video, etc.)

Return ONLY JSON:
{
  "newsletter": {
    "subject_line": "Email subject (max 50 chars)",
    "opening": "Hook paragraph",
    "key_insight": "Main takeaway paragraph",
    "takeaways": ["Bullet 1", "Bullet 2", "Bullet 3"],
    "framework": {"name": "Name", "steps": ["Step 1", "Step 2"]},
    "closing": "Soft CTA sentence"
  }
}
```

### 9.3 Add Parse Code Node

Name: `Parse Newsletter`

```javascript
const response = $input.all()[0].json.text || $input.all()[0].json.content;
let data;
try {
  const jsonMatch = response.match(/\{[\s\S]*\}/);
  data = JSON.parse(jsonMatch[0]);
} catch (e) {
  data = { newsletter: {} };
}

const meta = $("Parse Ideas JSON").first().json;
const nl = data.newsletter;

// Compose full newsletter body
const body =
  `${nl.opening}\n\n${nl.key_insight}\n\n` +
  `KEY TAKEAWAYS:\n${(nl.takeaways || []).map((t) => `→ ${t}`).join("\n")}\n\n` +
  (nl.framework
    ? `THE FRAMEWORK:\n${nl.framework.name}\n${nl.framework.steps.map((s, i) => `${i + 1}. ${s}`).join("\n")}\n\n`
    : "") +
  nl.closing;

return [
  {
    json: {
      content_id: `${meta.video_id}-newsletter-1`,
      video_id: meta.video_id,
      platform: "newsletter",
      hook: nl.subject_line,
      body: body,
      cta: nl.closing,
      status: "draft",
      created_at: new Date().toISOString(),
    },
  },
];
```

### 9.4 Add Google Sheets Node

- Name: `Store Newsletter`
- Sheet: `Generated_Content`
- Map: content_id, video_id, platform, hook, body, cta, status, created_at

---

## Verification

- [ ] Execute workflow
- [ ] 1 newsletter in Generated_Content sheet
- [ ] Newsletter has subject, body with takeaways, CTA

**→ Next: Shard 10: Quality Gate Implementation**
