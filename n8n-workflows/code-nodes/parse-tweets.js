/**
 * Parse Tweets JSON
 * 
 * Parses tweet output from either GLM-4.6 or Kimi-K2.
 * Handles OpenAI-compatible response format.
 */

const httpOutput = $input.all()[0].json;
const generatorName = $input.all()[0].json._generator || 'unknown';

// Extract content from OpenAI-compatible format
const response = httpOutput.choices?.[0]?.message?.content 
  || httpOutput.text 
  || httpOutput.content 
  || '';

// Get metadata from earlier node
const metadata = $('Parse Ideas').first().json;

let tweets;
try {
  // Clean and parse JSON
  let cleanedResponse = response
    .replace(/```json\n?/gi, '')
    .replace(/```\n?/gi, '')
    .trim();
  
  const jsonMatch = cleanedResponse.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    tweets = parsed.tweets || [];
  } else {
    throw new Error('No valid JSON found');
  }
} catch (error) {
  tweets = [];
  console.log('Parse error:', error.message);
}

// Return formatted tweets with metadata
return tweets.map((tweet, index) => ({
  json: {
    content_id: `${metadata.video_id}-twitter-${generatorName}-${index + 1}`,
    video_id: metadata.video_id,
    platform: 'twitter',
    generator: generatorName,
    content_type: tweet.type || 'tweet',
    hook: tweet.hook || tweet.content?.substring(0, 50),
    body: tweet.content,
    cta: '',
    char_count: tweet.content?.length || 0,
    source_idea: tweet.source_idea,
    status: 'draft',
    created_at: new Date().toISOString()
  }
}));
