# Shard 11: Testing & Refinement

## Content Repurposing Engine

**Est. Time:** 60-90 min | **Depends on:** Shard 10 | **Outcome:** Fully working, tested workflow

---

## Tasks

### 11.1 Get Full Transcript for Testing

1. [ ] Go to Liam Ottley's video: https://youtu.be/kQFW3bUrOu4
2. [ ] Get transcript (YouTube → ... → Show Transcript → Copy)
3. [ ] Or use a transcript tool like Otter.ai or YouTube transcript extractor
4. [ ] Save transcript to a local file for testing

### 11.2 Full Integration Test

1. [ ] Open the form URL in browser
2. [ ] Submit with:
   - Video Title: `How to Automate Any Business With AI in 3 Steps`
   - Video URL: `https://youtu.be/kQFW3bUrOu4`
   - Transcript: (paste full transcript)
   - Niche: `AI/Business`
3. [ ] Watch workflow execute in n8n
4. [ ] Time the execution (should be under 3 minutes)

### 11.3 Verify All Outputs

Check Google Sheets:

**Raw_Transcripts:**

- [ ] New row with transcript stored
- [ ] video_id generated correctly

**Ideas_Extracted:**

- [ ] Ideas JSON stored
- [ ] Contains key_ideas, quotable_moments, frameworks

**Generated_Content:**

- [ ] 5 tweets (platform = twitter)
- [ ] 3 LinkedIn posts (platform = linkedin)
- [ ] 1 newsletter (platform = newsletter)
- [ ] All have quality_score filled in

**Quality_Logs:**

- [ ] 9 entries (one per content piece)
- [ ] Scores between 15-25
- [ ] pass/fail recorded

### 11.4 Quality Spot Check

Manually review 3 pieces of content:

**Tweet Review:**

- [ ] Under 280 characters
- [ ] Has specific insight (not generic)
- [ ] Sounds like Liam's voice

**LinkedIn Review:**

- [ ] Uses white space properly
- [ ] Hook is compelling
- [ ] Ends with genuine question

**Newsletter Review:**

- [ ] Has clear structure
- [ ] Includes actionable takeaways
- [ ] CTA feels natural

### 11.5 Prompt Tuning (if needed)

If content quality is poor:

1. [ ] Identify which prompt needs improvement
2. [ ] Add more specific instructions
3. [ ] Include examples of good output
4. [ ] Re-test with same transcript
5. [ ] Iterate until quality is acceptable

### 11.6 Error Handling Check

Test edge cases:

- [ ] Empty transcript → Should show error
- [ ] Very short transcript → Should still work
- [ ] Special characters → Should handle properly

### 11.7 Performance Optimization

If workflow is slow:

- [ ] Add Wait nodes (1s) between Gemini calls if hitting rate limits
- [ ] Check for unnecessary nodes
- [ ] Consider parallel vs sequential execution

---

## Final Verification Checklist

- [ ] Form accepts input correctly
- [ ] All Gemini calls succeed
- [ ] Ideas extracted are specific and useful
- [ ] 9 content pieces generated (5+3+1)
- [ ] Quality scores populated
- [ ] Content quality is acceptable for demo
- [ ] Execution time under 3 minutes
- [ ] No errors in workflow execution

---

## Troubleshooting Quick Reference

| Issue              | Solution                                     |
| ------------------ | -------------------------------------------- |
| Gemini rate limit  | Add 2s Wait nodes between calls              |
| JSON parse errors  | Check Gemini response format in node output  |
| Empty outputs      | Verify expressions reference correct nodes   |
| Low quality scores | Tune prompts with more specific instructions |
| Sheets write fails | Check column mapping and permissions         |

---

**→ Next: Shard 12: Demo Assets Creation**
