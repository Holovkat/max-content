/**
 * Parse Newsletter JSON
 * 
 * Parses newsletter output from either GLM-4.6 or Kimi-K2.
 */

const httpOutput = $input.all()[0].json;
const generatorName = $input.all()[0].json._generator || 'unknown';

const response = httpOutput.choices?.[0]?.message?.content 
  || httpOutput.text 
  || httpOutput.content 
  || '';

const metadata = $('Parse Ideas').first().json;

let newsletter;
try {
  let cleanedResponse = response
    .replace(/```json\n?/gi, '')
    .replace(/```\n?/gi, '')
    .trim();
  
  const jsonMatch = cleanedResponse.match(/\{[\s\S]*\}/);
  if (jsonMatch) {
    const parsed = JSON.parse(jsonMatch[0]);
    newsletter = parsed.newsletter || parsed;
  } else {
    throw new Error('No valid JSON found');
  }
} catch (error) {
  newsletter = {};
  console.log('Parse error:', error.message);
}

// Compose full newsletter body
const takeawaysText = (newsletter.takeaways || [])
  .map(t => `→ ${t}`)
  .join('\n');

const frameworkText = newsletter.framework?.name 
  ? `\n\n**${newsletter.framework.name}**\n${(newsletter.framework.steps || []).map((s, i) => `${i + 1}. ${s}`).join('\n')}`
  : '';

const fullBody = `${newsletter.opening || ''}\n\n${newsletter.key_insight || ''}\n\n**Key Takeaways:**\n${takeawaysText}${frameworkText}\n\n${newsletter.closing || ''}\n\n${newsletter.video_reference || ''}`;

return [{
  json: {
    content_id: `${metadata.video_id}-newsletter-${generatorName}-1`,
    video_id: metadata.video_id,
    platform: 'newsletter',
    generator: generatorName,
    content_type: 'summary',
    hook: newsletter.subject_line || '',
    preview_text: newsletter.preview_text || '',
    body: fullBody.trim(),
    cta: newsletter.closing || '',
    source_idea: 'all',
    status: 'draft',
    created_at: new Date().toISOString()
  }
}];
