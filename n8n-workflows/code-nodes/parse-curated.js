/**
 * Parse Curated Content
 * 
 * Parses Gemini's curation output and extracts the final selected content.
 */

const geminiOutput = $input.all()[0].json;

const response = geminiOutput.text 
  || geminiOutput.content 
  || geminiOutput.message?.content 
  || '';

const metadata = $('Parse Ideas').first().json;

let curationResult;
try {
  let cleanedResponse = response
    .replace(/```json\n?/gi, '')
    .replace(/```\n?/gi, '')
    .trim();
  
  const jsonMatch = cleanedResponse.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    curationResult = JSON.parse(jsonMatch[0]);
  } else {
    throw new Error('No valid JSON found');
  }
} catch (error) {
  curationResult = { curated_content: [], curation_summary: {} };
  console.log('Parse error:', error.message);
}

// Return curated content pieces
return (curationResult.curated_content || []).map((item, index) => ({
  json: {
    content_id: `${metadata.video_id}-curated-${index + 1}`,
    video_id: metadata.video_id,
    platform: item.platform || 'unknown',
    generator: item.source,
    content_type: 'curated',
    hook: item.final_content?.hook || '',
    body: item.final_content?.body || '',
    cta: item.final_content?.cta || '',
    
    // Curation metadata
    selection_reason: item.selection_reason,
    improvements_made: item.improvements_made,
    web_references: item.web_references,
    scores: item.original_scores,
    
    status: 'curated',
    created_at: new Date().toISOString(),
    
    // Summary for logging
    _curation_summary: curationResult.curation_summary
  }
}));
