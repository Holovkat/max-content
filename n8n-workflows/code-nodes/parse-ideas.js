/**
 * Parse Ideas JSON
 * 
 * This code node parses the GLM-4 response and extracts the structured ideas.
 * It handles various response formats and provides fallback for parsing errors.
 * 
 * Input: GLM-4 HTTP response with JSON containing key_ideas, quotable_moments, frameworks, stories
 * Output: Structured object with parsed ideas and metadata from earlier nodes
 */

// Get the GLM-4 response - handle OpenAI-compatible format
const httpOutput = $input.all()[0].json;

// GLM-4 uses OpenAI-compatible format: choices[0].message.content
const response = httpOutput.choices?.[0]?.message?.content 
  || httpOutput.text 
  || httpOutput.content 
  || '';

// Get metadata from earlier in the workflow (Set Metadata node)
const metadata = $('Set Metadata').first().json;

let extractedIdeas;

try {
  // Handle if response is already an object
  if (typeof response === 'object' && response !== null) {
    extractedIdeas = response;
  } else if (typeof response === 'string') {
    // Try to find JSON in the string (Gemini sometimes wraps in markdown)
    // Remove markdown code blocks if present
    let cleanedResponse = response
      .replace(/```json\n?/gi, '')
      .replace(/```\n?/gi, '')
      .trim();
    
    // Find the JSON object
    const jsonMatch = cleanedResponse.match(/\{[\s\S]*\}/);
    
    if (jsonMatch) {
      extractedIdeas = JSON.parse(jsonMatch[0]);
    } else {
      throw new Error('No valid JSON object found in response');
    }
  } else {
    throw new Error('Unexpected response type: ' + typeof response);
  }
  
  // Validate the structure
  if (!extractedIdeas.key_ideas) {
    extractedIdeas.key_ideas = [];
  }
  if (!extractedIdeas.quotable_moments) {
    extractedIdeas.quotable_moments = [];
  }
  if (!extractedIdeas.frameworks) {
    extractedIdeas.frameworks = [];
  }
  if (!extractedIdeas.stories) {
    extractedIdeas.stories = [];
  }
  
} catch (error) {
  // Fallback with empty structure and error info
  extractedIdeas = {
    key_ideas: [],
    quotable_moments: [],
    frameworks: [],
    stories: [],
    _parse_error: error.message,
    _raw_response: typeof response === 'string' ? response.substring(0, 500) : 'Non-string response'
  };
}

// Count extracted items for logging
const counts = {
  key_ideas: extractedIdeas.key_ideas?.length || 0,
  quotable_moments: extractedIdeas.quotable_moments?.length || 0,
  frameworks: extractedIdeas.frameworks?.length || 0,
  stories: extractedIdeas.stories?.length || 0
};

// Return combined output
return [{
  json: {
    // Metadata from ingestion
    video_id: metadata.video_id,
    video_title: metadata.video_title,
    video_url: metadata.video_url,
    niche: metadata.niche,
    target_audience: metadata.target_audience,
    tone: metadata.tone,
    tweet_count: metadata.tweet_count,
    linkedin_count: metadata.linkedin_count,
    transcript: metadata.transcript,
    
    // Extracted ideas
    ideas: extractedIdeas,
    
    // Counts for logging/debugging
    extraction_counts: counts,
    
    // Timestamp
    extracted_at: new Date().toISOString()
  }
}];
