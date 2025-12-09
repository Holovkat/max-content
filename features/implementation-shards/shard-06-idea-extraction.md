# Shard 06: Idea Extraction Node

## Content Repurposing Engine

**Estimated Time:** 30-45 minutes  
**Dependencies:** Shard 05 (Ingestion flow working)  
**Outcome:** AI extracts key ideas from transcripts

---

## Prerequisites

- [ ] Shard 05 complete (Form → Metadata → Store working)
- [ ] Gemini API credential in n8n
- [ ] Workflow open in n8n editor

---

## Tasks

### 6.1 Add Gemini Node for Idea Extraction

1. [ ] Open your `Content Repurposing Engine` workflow
2. [ ] After the `Store Raw Transcript` node, add new node
3. [ ] Search for **Google Gemini Chat Model** (or "Gemini")
4. [ ] Name: `Extract Ideas`
5. [ ] Configure:
   - Credential: Select your Gemini API credential
   - Model: `gemini-1.5-flash`
   - Temperature: `0.7`

- [ ] Gemini node added

### 6.2 Configure Idea Extraction Prompt

In the Gemini node, set the **User Message**:

```
You are a senior content strategist analyzing video transcripts to extract repurposable insights.

TASK: Analyze this transcript and extract content for a creator in the {{$json.niche}} space.

TRANSCRIPT:
"""
{{$json.transcript}}
"""

VIDEO TITLE: {{$json.video_title}}

Extract and return as valid JSON only (no markdown, no explanation):

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
      "quote": "Exact memorable quote",
      "type": "contrarian | framework | tactical | emotional"
    }
  ],
  "frameworks": [
    {
      "name": "Framework name",
      "steps": ["Step 1", "Step 2", "Step 3"]
    }
  ]
}

RULES:
- Extract 3-5 key ideas minimum
- Extract 3-5 quotable moments
- Extract 1-2 frameworks if present
- Be specific, not generic
- Use actual content from the transcript
- Return ONLY valid JSON, nothing else
```

- [ ] Prompt configured in Gemini node

### 6.3 Add Code Node to Parse JSON

1. [ ] After Gemini node, add **Code** node
2. [ ] Name: `Parse Ideas JSON`
3. [ ] Mode: Run Once for All Items
4. [ ] JavaScript code:

```javascript
// Get the Gemini response
const response = $input.all()[0].json.text || $input.all()[0].json.content;

// Try to extract JSON from the response
let extractedIdeas;

try {
  // Handle if response is already an object
  if (typeof response === "object") {
    extractedIdeas = response;
  } else {
    // Try to find JSON in the string
    const jsonMatch = response.match(/\{[\s\S]*\}/);
    if (jsonMatch) {
      extractedIdeas = JSON.parse(jsonMatch[0]);
    } else {
      throw new Error("No JSON found in response");
    }
  }
} catch (error) {
  // Fallback with empty structure
  extractedIdeas = {
    key_ideas: [],
    quotable_moments: [],
    frameworks: [],
    error: error.message,
    raw_response: response,
  };
}

// Get metadata from earlier in the workflow
const metadata = {
  video_id: $("Set Metadata").first().json.video_id,
  video_title: $("Set Metadata").first().json.video_title,
  video_url: $("Set Metadata").first().json.video_url,
  niche: $("Set Metadata").first().json.niche,
};

return [
  {
    json: {
      ...metadata,
      ideas: extractedIdeas,
    },
  },
];
```

- [ ] Code node configured

### 6.4 Add Google Sheets Node (Store Ideas)

1. [ ] After Code node, add **Google Sheets** node
2. [ ] Name: `Store Ideas`
3. [ ] Configure:
   - Operation: **Append Row**
   - Document: `Content Repurposing Engine`
   - Sheet: `Ideas_Extracted`
4. [ ] Use **Split In Batches** approach:
   - Or, store the full JSON as a single row for simplicity

**Simple approach (recommended for hackathon):**

Map columns:

- idea_id → `{{ $json.video_id }}-ideas`
- video_id → `{{ $json.video_id }}`
- idea_title → `Extracted Ideas`
- summary → `{{ JSON.stringify($json.ideas.key_ideas).slice(0, 50000) }}`
- quote → `{{ JSON.stringify($json.ideas.quotable_moments).slice(0, 50000) }}`
- idea_type → `{{ $json.ideas.frameworks ? JSON.stringify($json.ideas.frameworks) : '[]' }}`

- [ ] Google Sheets node configured

### 6.5 Add Sticky Notes

1. [ ] Add note above Gemini node: "AI: Extract key ideas, quotes, frameworks"
2. [ ] Add note above Code node: "PARSE: Clean JSON from LLM response"
3. [ ] Add note above Sheets node: "STORE: Save extracted ideas"

- [ ] Documentation added

---

## Verification: Test Idea Extraction

### 6.6 Test with Full Transcript

1. [ ] Get a sample transcript (use first few paragraphs from Liam's video)
2. [ ] Submit through the form (or use test execution)

**Sample transcript for testing:**

```
Today I'm going to show you how to automate any business with AI in just three steps.
This is what I call the Morningside Method, and it's helped us go from zero to over
$100,000 per month in revenue.

The first phase is what I call the AI Automation Agency phase. This is where you use
no-code tools like Make, Zapier, and ChatGPT to build basic automations. You don't
need to be technical. You just need to understand the client's problem.

Phase two is the AI Agency phase. Once you've made some money and proven the model,
you hire full-stack AI developers and start offering custom solutions.

Phase three is becoming an AI Transformation Partner. This is the endgame where you
do strategic consulting for enterprises and build long-term partnerships.

The key insight that most people miss: start with the problem, not the technology.
Don't ask "what AI tools should we use?" Ask "what process is costing us the most
time and money?"
```

3. [ ] Execute the workflow
4. [ ] Check each node for success:
   - [ ] Gemini returns JSON with ideas
   - [ ] Code node parses successfully
   - [ ] Ideas appear in Google Sheets

- [ ] Test execution successful

### 6.7 Verify Extracted Ideas Quality

Check the output contains:

- [ ] At least 3 key ideas identified
- [ ] Framework (Morningside Method / 3 phases) captured
- [ ] Quotable moments ("start with the problem, not the technology")
- [ ] Data stored in Ideas_Extracted sheet

---

## Current Workflow State

```
┌───────────────┐   ┌────────────┐   ┌───────────────┐   ┌──────────────┐   ┌─────────────┐   ┌─────────────┐
│ Form Trigger  │──▶│ Set        │──▶│ Store Raw     │──▶│ Extract      │──▶│ Parse Ideas │──▶│ Store Ideas │
│               │   │ Metadata   │   │ Transcript    │   │ Ideas        │   │ JSON        │   │             │
│               │   │            │   │ (Sheets)      │   │ (Gemini)     │   │ (Code)      │   │ (Sheets)    │
└───────────────┘   └────────────┘   └───────────────┘   └──────────────┘   └─────────────┘   └─────────────┘
```

---

## Troubleshooting

### Gemini returns error

- Check API key is valid
- Verify free tier limits not exceeded (15 RPM)
- Reduce transcript length if too long

### JSON parsing fails

- Check Gemini response in node output
- Gemini sometimes wraps JSON in markdown - Code node handles this
- Look for malformed JSON in response

### Ideas not specific enough

- Improve the prompt with more examples
- Add "Be specific, use actual quotes" to prompt
- Temperature of 0.7 should be good

### Rate limits

- Add **Wait** node (1-2 seconds) before Gemini if needed
- Gemini free tier: 15 requests per minute

---

## Completion Checklist

- [ ] Gemini node configured with extraction prompt
- [ ] Code node parses JSON response
- [ ] Ideas stored in Ideas_Extracted sheet
- [ ] Test run successful
- [ ] Extracted ideas are specific and useful

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 07: Twitter Generation**

---

_Your AI extraction layer is working! Now we'll generate platform content._
