# Technical Requirements Specification

## Content Repurposing Engine - Hostinger x n8n Hackathon

**Version:** 1.0  
**Date:** 2025-12-09  
**Deadline:** December 14, 2025 (11:59 PM EST)  
**Status:** Ready for Implementation

---

## 1. Executive Summary

This document specifies the technical requirements for a **Content Repurposing Engine** that transforms long-form video transcripts into high-quality, platform-ready social media content. The system is designed for the Hostinger x n8n Hackathon Build #2 challenge.

### 1.1 Key Differentiator

Unlike commodity content tools, this engine produces **magazine-quality output** by:

- Embedding editorial voice DNA (Liam Ottley / Morningside AI style)
- Implementing a quality gate with second-pass LLM critique
- Enforcing Hook-Value-CTA structure across all platforms

### 1.2 Zero-Cost Stack

| Component         | Technology           | Cost                 |
| ----------------- | -------------------- | -------------------- |
| Hosting           | Hostinger VPS (KVM2) | Hackathon provided   |
| Orchestration     | n8n (self-hosted)    | FREE                 |
| LLM               | Google Gemini Flash  | FREE (1M tokens/day) |
| Storage           | Google Sheets        | FREE                 |
| Input             | n8n Form/Webhook     | FREE                 |
| **Total Ongoing** |                      | **$0**               |

---

## 2. System Architecture

### 2.1 High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        CONTENT REPURPOSING ENGINE                        │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────────┐     ┌──────────────────────────────────────────────┐  │
│  │    INPUT     │     │              n8n ORCHESTRATOR                 │  │
│  │              │     │                                               │  │
│  │  Transcript  │────▶│  ┌─────────┐  ┌─────────┐  ┌─────────────┐   │  │
│  │  + Metadata  │     │  │ Ingest  │─▶│ Extract │─▶│  Generate   │   │  │
│  │              │     │  │         │  │  Ideas  │  │  Content    │   │  │
│  └──────────────┘     │  └─────────┘  └─────────┘  └──────┬──────┘   │  │
│                       │                                    │          │  │
│                       │                           ┌────────▼────────┐ │  │
│                       │                           │  Quality Gate   │ │  │
│                       │                           │  (Critique +    │ │  │
│                       │                           │   Refine)       │ │  │
│                       │                           └────────┬────────┘ │  │
│                       └────────────────────────────────────┼──────────┘  │
│                                                            │             │
│  ┌──────────────────────────────────────────────────────────▼──────────┐ │
│  │                         GOOGLE SHEETS                                │ │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐  ┌──────────┐  │ │
│  │  │ Tweets  │  │LinkedIn │  │Newsletter│  │ Quality │  │ Raw      │  │ │
│  │  │ (5)     │  │ (3)     │  │ (1)      │  │ Scores  │  │Transcript│  │ │
│  │  └─────────┘  └─────────┘  └─────────┘  └─────────┘  └──────────┘  │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐ │
│  │                      GOOGLE GEMINI FLASH                              │ │
│  │  • Idea Extraction  • Content Generation  • Quality Critique         │ │
│  └──────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

### 2.2 Component Details

#### 2.2.1 Hostinger VPS (Infrastructure Layer)

| Specification  | Requirement                             |
| -------------- | --------------------------------------- |
| **Plan**       | KVM2 (recommended)                      |
| **OS**         | Ubuntu 24.04 LTS                        |
| **RAM**        | 4GB minimum                             |
| **Deployment** | Docker via Hostinger one-click template |
| **Access**     | HTTPS with basic auth                   |

#### 2.2.2 n8n Orchestrator (Workflow Layer)

**Primary Workflow: `Content_Repurposing_Engine`**

| Node Group             | Purpose                                   | Gemini Calls         |
| ---------------------- | ----------------------------------------- | -------------------- |
| **Ingestion**          | Receive transcript + metadata             | 0                    |
| **Idea Extraction**    | Identify key insights, quotes, frameworks | 1                    |
| **Content Generation** | Create platform-specific posts            | 3 (one per platform) |
| **Quality Gate**       | Critique and refine each post             | 9 (one per post)     |
| **Storage**            | Write to Google Sheets                    | 0                    |

**Estimated Total Gemini Calls per Run:** ~13

#### 2.2.3 Google Gemini Flash (Intelligence Layer)

| Setting             | Value                             |
| ------------------- | --------------------------------- |
| **Model**           | gemini-1.5-flash                  |
| **Temperature**     | 0.7 (for content generation)      |
| **Temperature**     | 0.3 (for critique)                |
| **Max Tokens**      | 2048 (generation), 512 (critique) |
| **Free Tier Limit** | 15 RPM, 1M tokens/day             |

#### 2.2.4 Google Sheets (Storage Layer)

**Workbook Structure:**

```
📊 Content_Repurposing_Engine
├── 📋 Raw_Transcripts
│   └── video_id, title, transcript, metadata, created_at
├── 📋 Ideas_Extracted
│   └── video_id, idea_title, summary, quote, idea_type
├── 📋 Generated_Content
│   └── id, video_id, platform, content_type, hook, body, cta, quality_score, status
└── 📋 Quality_Logs
    └── id, content_id, scores_json, feedback, refined, timestamp
```

---

## 3. Data Flow Specification

### 3.1 Input Schema

```json
{
  "transcript": "string (required) - Full video transcript text",
  "video_title": "string (required) - Title of source video",
  "video_url": "string (optional) - YouTube URL",
  "niche": "string (default: 'AI/Business') - Content niche",
  "target_audience": "string (default: 'Entrepreneurs') - Who this is for",
  "tone": "string (default: 'practical') - Voice modifier"
}
```

### 3.2 Processing Pipeline

```
STAGE 1: INGESTION
├── Input: Raw transcript + metadata
├── Process: Validate, clean, store
└── Output: Stored transcript record with video_id

STAGE 2: IDEA EXTRACTION
├── Input: Transcript text
├── Process: Gemini extracts key ideas, quotes, frameworks
└── Output: Structured list of 5-7 content nuggets

STAGE 3: CONTENT GENERATION (per platform)
├── Input: Content nuggets + platform template
├── Process: Gemini generates platform-specific posts
└── Output: Raw posts (5 tweets, 3 LinkedIn, 1 newsletter)

STAGE 4: QUALITY GATE (per post)
├── Input: Generated post + quality rubric
├── Process: Gemini scores and critiques
├── Decision: If score < 18/25, trigger refinement
└── Output: Final posts with quality scores

STAGE 5: STORAGE
├── Input: All generated content
├── Process: Write to Google Sheets
└── Output: Populated spreadsheet with content library
```

### 3.3 Output Schema

**Generated Content Record:**

```json
{
  "id": "uuid",
  "video_id": "string",
  "platform": "twitter | linkedin | newsletter",
  "content_type": "tweet | post | summary",
  "hook": "string - Opening line(s)",
  "body": "string - Main content",
  "cta": "string - Call to action",
  "quality_score": "number (1-25)",
  "quality_breakdown": {
    "hook_clarity": "number (1-5)",
    "specificity": "number (1-5)",
    "voice_authenticity": "number (1-5)",
    "value_density": "number (1-5)",
    "cta_naturalness": "number (1-5)"
  },
  "status": "draft | refined | approved",
  "created_at": "timestamp",
  "refined_at": "timestamp | null"
}
```

---

## 4. Voice DNA Specification

### 4.1 Target Voice Profile: Liam Ottley / Morningside AI

| Attribute          | Specification                                              |
| ------------------ | ---------------------------------------------------------- |
| **Energy Level**   | High - urgent, action-oriented                             |
| **Tone**           | Direct, practical, transparently ambitious                 |
| **Language**       | Accessible, no jargon gatekeeping                          |
| **Evidence Style** | Numbers-forward ($100k, 60+ team, 1M views)                |
| **Learning Frame** | "Mistake-first" - "I screwed this up so you don't have to" |
| **CTAs**           | Action-oriented - "Build your first AI agent this weekend" |

### 4.2 Editorial Principles (from NYT/Economist research)

1. **Clarity Before Cleverness** - Simple, precise language
2. **Evidence-Grounded** - Every claim backed by specifics
3. **Impartial Gravitas** - Show, don't sell
4. **The Lingering Question** - End with reflection
5. **Rhythm & Cadence** - Vary sentence lengths deliberately

### 4.3 Platform-Specific Voice Adaptations

| Platform       | Voice Modification                                     |
| -------------- | ------------------------------------------------------ |
| **X/Twitter**  | Maximum punch, one idea per tweet, thread-aware        |
| **LinkedIn**   | Professional depth, white space, conversation-starters |
| **Newsletter** | Comprehensive summary, actionable takeaways, warmth    |

---

## 5. Quality Gate Specification

### 5.1 Scoring Rubric

| Criterion              | Weight | 1 (Fail)          | 3 (Acceptable)              | 5 (Excellent)                |
| ---------------------- | ------ | ----------------- | --------------------------- | ---------------------------- |
| **Hook Clarity**       | 20%    | Generic/clickbait | Interesting but predictable | Genuine cognitive dissonance |
| **Specificity**        | 20%    | All abstract      | Some examples               | Names, numbers, moments      |
| **Voice Authenticity** | 20%    | AI slop           | Professional but bland      | Distinct, identifiable voice |
| **Value Density**      | 20%    | Filler/platitudes | Some value                  | Every sentence earns place   |
| **CTA Naturalness**    | 20%    | "SMASH LIKE"      | Clear but transactional     | Genuine invitation           |

### 5.2 Quality Thresholds

| Platform   | Pass Threshold | Auto-Refine? | Max Attempts |
| ---------- | -------------- | ------------ | ------------ |
| X/Twitter  | 16/25          | Yes          | 2            |
| LinkedIn   | 18/25          | Yes          | 2            |
| Newsletter | 20/25          | Yes          | 3            |

### 5.3 Refinement Loop

```
IF quality_score < threshold:
    1. Extract specific feedback from critique
    2. Re-prompt Gemini with original + feedback
    3. Generate refined version
    4. Re-score refined version
    5. IF still below threshold AND attempts < max:
         Repeat from step 1
       ELSE:
         Accept current version, flag for human review
```

---

## 6. n8n Workflow Specification

### 6.1 Node Structure

```
[Form Trigger] ─────────────────────────────────────────────────────┐
       │                                                             │
       ▼                                                             │
[Set Metadata] ── video_id, timestamp, defaults                     │
       │                                                             │
       ▼                                                             │
[Store Raw] ── Google Sheets: Raw_Transcripts                       │
       │                                                             │
       ▼                                                             │
[Extract Ideas] ── Gemini: Idea Extraction Prompt                   │
       │                                                             │
       ▼                                                             │
[Store Ideas] ── Google Sheets: Ideas_Extracted                     │
       │                                                             │
       ▼                                                             │
[Split Platforms] ── Branch for each platform                       │
       │                                                             │
       ├──▶ [Generate Tweets] ── Gemini: Twitter Prompt (x5)        │
       │          │                                                  │
       │          ▼                                                  │
       │    [Quality Gate Tweets] ── Gemini: Critique (x5)          │
       │          │                                                  │
       │          ▼                                                  │
       │    [Refine Loop] ── Conditional refinement                 │
       │          │                                                  │
       │          ▼                                                  │
       │    [Store Tweets] ── Google Sheets                         │
       │                                                             │
       ├──▶ [Generate LinkedIn] ── Gemini: LinkedIn Prompt (x3)     │
       │          │                                                  │
       │          ▼                                                  │
       │    [Quality Gate LinkedIn] ── Gemini: Critique (x3)        │
       │          │                                                  │
       │          ▼                                                  │
       │    [Refine Loop] ── Conditional refinement                 │
       │          │                                                  │
       │          ▼                                                  │
       │    [Store LinkedIn] ── Google Sheets                       │
       │                                                             │
       └──▶ [Generate Newsletter] ── Gemini: Newsletter Prompt (x1) │
                  │                                                  │
                  ▼                                                  │
            [Quality Gate Newsletter] ── Gemini: Critique (x1)      │
                  │                                                  │
                  ▼                                                  │
            [Refine Loop] ── Conditional refinement                 │
                  │                                                  │
                  ▼                                                  │
            [Store Newsletter] ── Google Sheets                     │
                  │                                                  │
                  ▼                                                  │
            [Merge Results] ◀────────────────────────────────────────┘
                  │
                  ▼
            [Summary Response] ── Return counts + preview
```

### 6.2 Credential Requirements

| Credential        | Type    | Notes                        |
| ----------------- | ------- | ---------------------------- |
| **Google Gemini** | API Key | From Google AI Studio (free) |
| **Google Sheets** | OAuth2  | n8n native Google connection |

---

## 7. Demonstration Requirements

### 7.1 Demo Video (1-2 minutes)

**Required Shots:**

1. **Trigger** (10s) - Show form with transcript input
2. **Workflow Execution** (20s) - n8n canvas with nodes executing
3. **LLM Processing** (10s) - Show Gemini calls in action
4. **Quality Gate** (15s) - Show scoring and refinement
5. **Output** (30s) - Google Sheets with generated content
6. **Content Preview** (15s) - Read a sample LinkedIn post

### 7.2 Written Submission (100-300 words)

**Template:**

```
# Content Repurposing Engine

Transforms long-form video transcripts into platform-ready social
content for X/Twitter, LinkedIn, and newsletters.

## How It Works

1. **Input** a video transcript via n8n form
2. **Extract** 5-7 key insights using Gemini Flash
3. **Generate** 9 pieces of content (5 tweets, 3 LinkedIn, 1 newsletter)
4. **Validate** with quality gate scoring (Hook/Value/CTA structure)
5. **Store** in Google Sheets for review

## What Makes It Different

- Voice DNA calibrated to premium editorial standards
- Second-pass quality critique prevents "AI slop"
- Zero ongoing costs (Gemini free tier + Google Sheets)

## Tech Stack

- Hostinger VPS with self-hosted n8n
- Google Gemini Flash for LLM
- Google Sheets for storage

Built for creators who want to multiply their content without
sacrificing quality.
```

---

## 8. Success Criteria

### 8.1 Functional Requirements

| Requirement               | Acceptance Criteria                                 |
| ------------------------- | --------------------------------------------------- |
| Accept transcript input   | Form successfully ingests 10,000+ tokens            |
| Generate platform content | Produces exactly 5 tweets, 3 LinkedIn, 1 newsletter |
| Quality gate functions    | All posts scored, <18 posts trigger refinement      |
| Store outputs             | Google Sheets populated with all fields             |
| Complete under 3 minutes  | Full workflow execution time                        |

### 8.2 Quality Requirements

| Metric                 | Target                           |
| ---------------------- | -------------------------------- |
| Average quality score  | ≥ 18/25                          |
| Hook clarity score     | ≥ 3.5/5 average                  |
| Zero "AI slop" markers | No generic filler phrases        |
| Voice consistency      | Matches Liam Ottley energy/style |

---

## 9. Risk Mitigation

| Risk                | Likelihood | Impact | Mitigation                                |
| ------------------- | ---------- | ------ | ----------------------------------------- |
| Gemini rate limits  | Medium     | High   | Batch calls, add delays between requests  |
| Low quality output  | Medium     | High   | Quality gate with refinement loop         |
| VPS setup issues    | Low        | High   | Use Hostinger one-click template          |
| Transcript too long | Low        | Medium | Chunk into segments, process sequentially |

---

## 10. Appendices

### A. Demo Transcript Source

**Video:** "How to Automate Any Business With AI in 3 Steps (Beginner's Guide)"  
**Creator:** Liam Ottley  
**URL:** https://youtu.be/kQFW3bUrOu4

### B. Reference Links

- [Hostinger VPS](https://www.hostinger.com/vps-hosting)
- [n8n Documentation](https://docs.n8n.io/)
- [Google AI Studio](https://aistudio.google.com/)
- [Google Sheets API](https://developers.google.com/sheets/api)

### C. Prompt Templates

See separate document: `voice-dna-framework.md`

### D. Implementation Shards

See separate directory: `implementation-shards/`

---

_Document prepared by the BMAD Team for Tony - Hostinger x n8n Hackathon 2025_
