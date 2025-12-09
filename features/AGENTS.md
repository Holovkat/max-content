# AGENTS.md — Features Documentation

> **Reference documentation for the Content Repurposing Engine project**

---

## Package Identity

This directory contains all project documentation for the Hostinger x n8n Hackathon Content Repurposing Engine. It includes requirements, specifications, and step-by-step implementation guides.

---

## Documentation Structure

### Core Documents

| File                             | Purpose                                 | When to Use                            |
| -------------------------------- | --------------------------------------- | -------------------------------------- |
| `prd.md`                         | Product Requirements Document           | Understanding project scope & goals    |
| `technical-requirements-spec.md` | Technical architecture & specifications | Implementation decisions, architecture |
| `voice-dna-framework.md`         | LLM prompts & voice calibration         | Writing prompts, content quality       |
| `submission-requirements.md`     | Hackathon submission checklist          | Pre-submission verification            |

### Implementation Shards

**Location:** `implementation-shards/`

These shards should be executed **sequentially**. Each shard is self-contained and builds on the previous.

| Shard | Purpose                   | Dependencies |
| ----- | ------------------------- | ------------ |
| 00    | Overview & execution plan | None         |
| 01    | Hostinger VPS Setup       | None         |
| 02    | n8n Installation          | Shard 01     |
| 03    | Google Credentials Setup  | Shard 02     |
| 04    | Google Sheets Structure   | Shard 03     |
| 05    | Core Workflow - Ingestion | Shard 04     |
| 06    | Idea Extraction Node      | Shard 05     |
| 07    | Twitter Generation        | Shard 06     |
| 08    | LinkedIn Generation       | Shard 06     |
| 09    | Newsletter Generation     | Shard 06     |
| 10    | Quality Gate              | Shards 07-09 |
| 11    | Testing & Refinement      | Shard 10     |
| 12    | Demo Assets Creation      | Shard 11     |

---

## Patterns & Conventions

### ✅ DO

- Start with `shard-00-overview.md` to understand the execution plan
- Execute shards in order (dependencies matter)
- Check off tasks as you complete them within each shard
- Run verification steps before moving to next shard
- Reference `voice-dna-framework.md` for all LLM prompt work

### ❌ DON'T

- Skip shards or execute out of order
- Modify prompt templates without understanding voice DNA principles
- Proceed to next shard if verification steps fail
- Ignore quality gate thresholds (defined in technical spec)

---

## Key Reference Patterns

### Voice DNA Profile

```yaml
voice_profile:
  name: "Liam Ottley"
  brand: "Morningside AI"
  energy: "High-drive, urgent, building-while-speaking"
  tone: "Direct, practical, transparently ambitious"
  evidence_style: "Numbers-forward ($100k, 60+ team)"
```

### Quality Gate Scoring

| Criterion          | Weight | Pass Threshold (Twitter/LinkedIn/Newsletter) |
| ------------------ | ------ | -------------------------------------------- |
| Hook Clarity       | 20%    | 16/25, 18/25, 20/25                          |
| Specificity        | 20%    |                                              |
| Voice Authenticity | 20%    |                                              |
| Value Density      | 20%    |                                              |
| CTA Naturalness    | 20%    |                                              |

### Content Output Targets

- **5 Tweets** (max 280 chars each)
- **3 LinkedIn posts** (1200-1800 chars optimal)
- **1 Newsletter section** (400-600 words)

---

## JIT Index Hints

```bash
# Find specific section in technical spec
rg -n "PATTERN" features/technical-requirements-spec.md

# Find prompt template in voice DNA
rg -n "PROMPT" features/voice-dna-framework.md

# List all implementation shards
ls features/implementation-shards/shard-*.md

# Find quality gate info
rg -n "quality" features/technical-requirements-spec.md

# Find anti-patterns (AI slop markers)
rg -n "banned_phrases" features/voice-dna-framework.md
```

---

## Common Gotchas

1. **Prompt template variables**: Use `{{variable_name}}` format in prompts (see voice-dna-framework.md)
2. **Quality thresholds differ by platform**: Twitter 16/25, LinkedIn 18/25, Newsletter 20/25
3. **Gemini Flash settings**: Temperature 0.7 for generation, 0.3 for critique
4. **Shard dependencies**: Shards 07-09 all depend on Shard 06 (can be done in parallel)

---

## Pre-PR Checks

Before any documentation changes:

```bash
# Verify all markdown files are valid
find features/ -name "*.md" -exec echo "Checking: {}" \;

# Check for broken internal links
rg -n "]\(features/" . | grep -v ".md:"

# Verify shard sequence is complete
ls features/implementation-shards/shard-*.md | wc -l
# Should be 13 (shard-00 through shard-12)
```

---

## Related Files

- **Root AGENTS.md**: [`../AGENTS.md`](../AGENTS.md) - Project-wide guidelines
- **README**: [`../README.md`](../README.md) - Project overview
