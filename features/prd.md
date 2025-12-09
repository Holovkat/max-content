# PRD: Content Repurposing Engine  
**Hostinger x n8n Hackathon – Content Management Build**

---

## 1. Context & Hackathon Constraints

### 1.1 Event Overview
- **Hackathon:** Hostinger x n8n (N8N) Hackathon  
- **Build Option Chosen:** Content Repurposing Engine (Build #2)  
- **Platform Requirements:**
  - Core automation built with **n8n**.
  - Workflow **self-hosted on Hostinger VPS** (e.g., KVM2 plan).
- **Submission Deadline:**  
  - **December 14, 11:59 PM EST**.

### 1.2 Hackathon Judging Criteria (for this build)

The system must:

1. **Input**
   - Accept a **video transcript** (preferably long-form) as input.

2. **Output**
   - Produce **high-quality content** for multiple platforms:
     - Examples: X/Twitter, LinkedIn, Instagram, Skool posts, newsletters, etc.
   - Each piece of content must have:
     - A **clear hook**
     - Strong **value** (insight, how-to, or transformation)
     - A natural, **organic call to action** (CTA)

3. **Content Quality**
   - Avoid “AI slop” / generic filler.
   - Sound like something a serious creator would actually post.
   - Be aligned with a chosen **niche** (does not have to be AI).

4. **System Requirements (Hackathon-Specific)**
   - Hosted on **Hostinger** (self-hosted, not n8n cloud).
   - Demonstrated in:
     - **1–2 minute demo video** walkthrough.
     - **100–300 word write-up** explaining the workflow.

---

## 2. Product Vision

### 2.1 Product Summary

> Build a **Content Repurposing Engine** that takes a single long-form video transcript and automatically generates **platform-ready posts** tailored to X/Twitter, LinkedIn, Instagram, Skool, and/or newsletters, while maintaining **high-quality hooks, strong value, and natural CTAs**, all orchestrated via **n8n** and hosted on a **Hostinger VPS**.

### 2.2 Goals

- **Primary Goal:**  
  Convert one long-form piece of content (video transcript) into a **library of ready-to-use posts** for multiple platforms.

- **Secondary Goals:**
  - Provide **consistent structure** (hook–value–CTA) across platforms.
  - Provide **centralised storage** (e.g., Airtable/Notion/Google Sheets) for easy human review & scheduling.
  - Demonstrate a **clear, understandable architecture** that judges can follow easily.

### 2.3 Non-Goals

- Not required to:
  - Auto-post content to social platforms.
  - Handle advanced scheduling, analytics, or A/B testing.
  - Provide full front-end UI (optional bonus, not mandatory).

---

## 3. User Personas & Use Cases

### 3.1 Primary Persona – Content Creator / Educator

- Has **long-form videos** (YouTube, webinars, podcasts, live calls).
- Wants to:
  - Extract high-signal **nuggets** and **insights**.
  - Quickly generate **social content** across platforms.
  - Maintain **brand voice** and **quality** without writing everything manually.

### 3.2 Key Use Cases

1. **Repurpose YouTube Video into Cross-Platform Posts**
   - Input: Video transcript (copied from YouTube or a transcription tool).
   - Output:
     - 3–5 LinkedIn posts.
     - 3–10 X/Twitter posts.
     - 2–4 Instagram captions.
     - 1 newsletter summary.

2. **Create Community/Skool Posts From a Training Call**
   - Input: Transcript of a community workshop.
   - Output:
     - Skool thread posts with:
       - Summary of key idea.
       - Structured bullet points.
       - CTA to re-watch the replay.

---

## 4. Functional Requirements

### 4.1 Inputs

- **Required Input:**
  - Video transcript text (UTF-8, plain text).
- **Optional Inputs:**
  - **Metadata:** video title, description, target niche, target audience.
  - **Preferred platforms:** e.g., `[LinkedIn, X, Instagram, Newsletter]`.
  - **Tone/Style:** e.g., “educational”, “controversial”, “inspirational”.

### 4.2 Processing Steps (High-Level)

1. **Transcript Ingestion**
   - Receive transcript via:
     - Manual paste into a form (or)
     - n8n webhook node (text payload).
   - Store raw transcript + metadata in a table.

2. **Segmentation & Idea Extraction**
   - Chunk transcript into logical sections (e.g., by topic/time).
   - Identify:
     - Key ideas.
     - Stories/examples.
     - Strong quotes / one-liners.
   - Output: A structured list of **content nuggets**.

3. **Platform-Specific Content Generation**
   - For each chosen platform:
     - Map content nuggets into platform-specific formats:
       - X/Twitter: short punchy posts, threads, single-sentence hooks.
       - LinkedIn: 150–300+ words, structured with line breaks.
       - Instagram: caption with emotional hook and CTA.
       - Skool/community: informative posts with questions to drive engagement.
       - Newsletter: 1–2 section summary + CTA.
   - Enforce **Hook–Value–CTA** structure.

4. **Quality Layer**
   - Optionally perform a second LLM pass to:
     - Score or critique posts based on:
       - Clarity of hook.
       - Specificity of value.
       - Naturalness & relevance of CTA.
     - Refine any posts that fail a quality threshold.

5. **Storage & Output**
   - Save generated content to a persistent store:
     - e.g., Airtable, Notion, PostgreSQL, Google Sheets.
   - Provide:
     - Clear columns/fields (platform, post_type, hook, body, CTA, tags, status).
   - Optionally notify user:
     - Email summary or message containing a link to the content sheet.

### 4.3 Outputs

- A structured collection of posts, e.g.:

  | Platform | Type       | Hook                         | Body / Content | CTA                           | Status |
  |----------|------------|------------------------------|----------------|--------------------------------|--------|
  | LinkedIn | Single post| “Most people misunderstand…” | (full text)    | “Reply ‘guide’ for the PDF…”  | Draft  |
  | X        | Tweet      | “AI won’t take your job…”    | (same or short)| “RT if this resonates.”       | Draft  |
  | Skool    | Post       | “Today’s lesson: …”          | (longer body)  | “Comment your biggest insight”| Draft  |

---

## 5. Non-Functional Requirements

- **Performance:**
  - Must handle transcripts up to **~10,000–20,000 tokens**.
  - Total generation time should be acceptable for human use (e.g., under a few minutes).

- **Reliability:**
  - Workflow should fail gracefully:
    - Clear error messages in n8n.
    - No silent failures.

- **Maintainability:**
  - Workflow nodes must be:
    - Clearly labelled.
    - Grouped logically.
    - Easy to modify (e.g. add/remove platforms).

- **Explainability (for judges):**
  - Architecture and workflows must be:
    - Easy to explain in a **1–2 minute video**.
    - Easy to summarise in **100–300 words**.

---

## 6. Technical Components for AI Agent (High-Level Spec)

This section is formatted so an AI agent can easily parse the design.

### 6.1 Architecture Overview

**Components:**

1. **Hostinger VPS**
   - OS: Ubuntu 24.04 (default from Hostinger).
   - n8n running via Docker container (Hostinger one-click template or custom Compose).

2. **n8n Orchestrator**
   - Main workflow:
     - Ingest transcript.
     - Call LLM(s).
     - Transform & store outputs.
   - Optional: separate workflows for:
     - Transcript ingestion.
     - Quality review.
     - Notification.

3. **LLM Provider**
   - One primary LLM for generation/refinement (e.g., OpenAI, Gemini, Anthropic, etc.).
   - All calls coordinated via:
     - HTTP Request node, or
     - Native n8n LLM integration if available.

4. **Data Storage Layer**
   - One of:
     - Airtable base with “Posts” table.
     - Notion database.
     - Google Sheet.
     - Postgres DB (if comfortable).
   - Required Fields:
     - `id`, `video_id`, `platform`, `post_type`, `hook`, `body`, `cta`, `topic`, `created_at`.

5. **Optional Input UI**
   - Simple web front-end (optional):
     - Host on same Hostinger VPS or static hosting.
     - Form with transcript + metadata → n8n webhook.

---

### 6.2 Infrastructure Requirements

- **Hostinger VPS:**
  - Plan: **KVM2** (recommended).
  - Self-hosted n8n instance:
    - Deployed via Hostinger one-click template or Docker Compose.
  - Docker Manager used for:
    - Container updates.
    - Viewing logs/env variables.

- **Security & Access:**
  - n8n editor URL:
    - Protected with basic auth and/or n8n credentials.
  - API keys:
    - Stored in n8n credentials.
    - Not hardcoded into workflow.

---

### 6.3 Core Workflows (for AI Agent)

#### Workflow A: `Transcript_Ingestion`

**Trigger:**

- Manual run, or
- Webhook (e.g., POST with transcript JSON), or
- “Execute workflow” node from a helper.

**Steps:**

1. **Receive Transcript & Metadata**
   - Fields: `transcript`, `video_title`, `niche`, `audience`, `platforms[]`.

2. **Store Raw Transcript**
   - Save into data storage (e.g., Airtable/Sheet row: `video_id`, `transcript`, `metadata`).

3. **Call Workflow B: `Content_Generation`**
   - Pass transcript + metadata as input.

---

#### Workflow B: `Content_Generation`

**Steps:**

1. **Chunk & Extract Ideas**
   - LLM call: “Summarise this transcript into X–Y key ideas.”
   - Output: structured list (`ideas[]` with `title`, `summary`, `quote`, `timestamp` if provided).

2. **Platform Mapping**
   - For each platform in `platforms[]`, run a sub-workflow:
     - `Generate_LinkedIn_Posts`
     - `Generate_Twitter_Posts`
     - `Generate_Instagram_Captions`
     - `Generate_Skool_Posts`
     - `Generate_Newsletter_Section`

3. **Hook–Value–CTA Enforcement**
   - Prompt template explicitly enforces:
     - **Hook**: 1–2 sentences.
     - **Value**: detailed main content.
     - **CTA**: natural, platform-appropriate.

4. **Quality Review (Optional but Recommended)**
   - Second LLM call per post:
     - “Critique this post for clarity, specificity, and value. Suggest improvements if needed.”
   - If score < threshold (via simple rubric), regenerate or refine.

5. **Persist Outputs**
   - Upsert data into storage:
     - Row per post with all required fields.

6. **Return Summary**
   - Output count of posts per platform.
   - Provide preview of a few posts for the demo.

---

### 6.4 Outcomes & Deliverables (for AI Agent)

1. **Technical Deliverables**
   - Deployed n8n workflows on Hostinger VPS.
   - External storage (Airtable/Sheet/Notion) populated with sample output.
   - (Optional) Lightweight web form or endpoint for input.

2. **Demonstration Artifacts**
   - Short **screen recording**:
     - Show trigger → workflow execution → final outputs in storage.
   - **100–300 word description** explaining:
     - What the workflow does.
     - How it’s structured.
     - Why it’s useful for creators.

3. **Architecture Description**
   - A simple diagram (textual or image) explaining:
     - Input → n8n → LLM → Storage → Human review.

---

## 7. Implementation Plan (High-Level)

1. **Phase 1 – Environment Setup**
   - Provision Hostinger VPS (KVM2).
   - Install n8n via Hostinger one-click template.
   - Ensure HTTPS, login, and access work.

2. **Phase 2 – Minimal Viable Workflow**
   - Create `Transcript_Ingestion` workflow:
     - Manual trigger node with example transcript.
   - Create `Content_Generation` workflow:
     - For one platform only (e.g., LinkedIn).
   - Confirm end-to-end: transcript → 2–3 LinkedIn posts → store into a Google Sheet/Airtable.

3. **Phase 3 – Multi-Platform Expansion**
   - Add X/Twitter, Instagram, Skool, Newsletter variants.
   - Create sub-workflow or function per platform.
   - Tune prompts for each platform’s style.

4. **Phase 4 – Quality Layer**
   - Add second-pass LLM review/refinement.
   - Ensure prompts discourage AI slop and emphasize:
     - Specific examples.
     - Niche relevance.
     - Clear, simple language.

5. **Phase 5 – Polish & Observability**
   - Clean up node labels, groups, and comments.
   - Add simple error handling & logging nodes.
   - Ensure the workflow is understandable at a glance.

6. **Phase 6 – Demo & Submission Assets**
   - Record 1–2 minute demo video.
   - Write 100–300 word summary.
   - Capture necessary screenshots of Hostinger VPS & n8n.
   - Complete submission form on Skool.

