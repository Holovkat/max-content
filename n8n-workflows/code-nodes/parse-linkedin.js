/**
 * Parse LinkedIn JSON
 * 
 * Parses LinkedIn post output from either GLM-4.6 or Kimi-K2.
 */

const httpOutput = $input.all()[0].json;
const generatorName = $input.all()[0].json._generator || 'unknown';

const response = httpOutput.choices?.[0]?.message?.content 
  || httpOutput.text 
  || httpOutput.content 
  || '';

const metadata = $('Parse Ideas').first().json;

let posts;
try {
  let cleanedResponse = response
    .replace(/```json\n?/gi, '')
    .replace(/```\n?/gi, '')
    .trim();
  
  const jsonMatch = cleanedResponse.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    posts = parsed.posts || [];
  } else {
    throw new Error('No valid JSON found');
  }
} catch (error) {
  posts = [];
  console.log('Parse error:', error.message);
}

return posts.map((post, index) => ({
  json: {
    content_id: `${metadata.video_id}-linkedin-${generatorName}-${index + 1}`,
    video_id: metadata.video_id,
    platform: 'linkedin',
    generator: generatorName,
    content_type: post.type || 'post',
    hook: post.hook,
    body: post.body,
    cta: post.closing_question || '',
    char_count: post.body?.length || 0,
    source_idea: post.source_idea,
    status: 'draft',
    created_at: new Date().toISOString()
  }
}));
