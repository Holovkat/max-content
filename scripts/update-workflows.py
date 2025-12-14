#!/usr/bin/env python3
"""
Update n8n workflow files to send raw LLM output instead of formatted payload.
This avoids JSON encoding issues with control characters.
"""

import json
import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GENERATOR_PATH = os.path.join(BASE_DIR, 'n8n-workflows', 'content-generator.json')
APPROVAL_PATH = os.path.join(BASE_DIR, 'n8n-workflows', 'content-approval.json')

# New Build Preview Response code for content-generator.json
# Key change: Send raw LLM text + metadata instead of parsed/formatted content
BUILD_PREVIEW_CODE = '''// Parse the LLM response and build preview HTML
const llmOutput = $('Generate Content').first().json;
const input = $('Prepare Input').first().json;

// Get the raw LLM response text (we'll send this to approval)
const rawLlmText = llmOutput.text || llmOutput.response || JSON.stringify(llmOutput);

// Parse for preview display only
let output = {};
try {
  let responseText = rawLlmText.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim();
  output = JSON.parse(responseText);
} catch (e) {
  output = {
    key_ideas: ['Error parsing AI response'],
    tweets: [],
    linkedin: { hook: '', body: 'Error: ' + e.message, question: '' },
    newsletter: { subject: '', intro: '', points: [], cta: '' },
    instagram: [],
    skool: { title: '', intro: '', takeaways: [], discussion: '' },
    summary: 'Parse error'
  };
}

// Get newsletter settings from input
const newsletterSettings = input.newsletter || {};
const recipients = newsletterSettings.recipients || [];
const senderName = newsletterSettings.senderName || 'Newsletter';

// Create a simple payload with raw LLM text (no nested JSON objects)
// The approval workflow will parse the rawLlmText
const simplePayload = {
  s: input.sessionId,
  p: input.platforms,
  r: recipients.join(','),
  n: senderName,
  t: rawLlmText.replace(/```json\\n?/g, '').replace(/```\\n?/g, '').trim()
};

// Encode as simple pipe-delimited string to avoid JSON issues
const payloadStr = [
  simplePayload.s,
  simplePayload.p.x ? '1' : '0',
  simplePayload.p.linkedin ? '1' : '0', 
  simplePayload.p.newsletter ? '1' : '0',
  simplePayload.p.instagram ? '1' : '0',
  simplePayload.p.skool ? '1' : '0',
  simplePayload.r,
  simplePayload.n,
  Buffer.from(simplePayload.t).toString('base64')
].join('|');

const approvalWebhookPath = 'content-approval-confirm';
const encodedContent = Buffer.from(payloadStr).toString('base64');
const showApprovalButton = input.platforms.x || input.platforms.linkedin || (input.platforms.newsletter && recipients.length > 0);

// Icons
const xIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg>';
const linkedinIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#0077b5"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433c-1.144 0-2.063-.926-2.063-2.065 0-1.138.92-2.063 2.063-2.063 1.14 0 2.064.925 2.064 2.063 0 1.139-.925 2.065-2.064 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>';
const listIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M3 4h18v2H3V4zm0 7h18v2H3v-2zm0 7h18v2H3v-2z"/></svg>';
const emailIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor"><path d="M20 4H4c-1.1 0-2 .9-2 2v12c0 1.1.9 2 2 2h16c1.1 0 2-.9 2-2V6c0-1.1-.9-2-2-2zm0 4l-8 5-8-5V6l8 5 8-5v2z"/></svg>';
const instaIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#E4405F"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zm0-2.163c-3.259 0-3.667.014-4.947.072-4.358.2-6.78 2.618-6.98 6.98-.059 1.281-.073 1.689-.073 4.948 0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98 1.281.058 1.689.072 4.948.072 3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98-1.281-.059-1.69-.073-4.949-.073zm0 5.838c-3.403 0-6.162 2.759-6.162 6.162s2.759 6.163 6.162 6.163 6.162-2.759 6.162-6.163c0-3.403-2.759-6.162-6.162-6.162zm0 10.162c-2.209 0-4-1.79-4-4 0-2.209 1.791-4 4-4s4 1.791 4 4c0 2.21-1.791 4-4 4zm6.406-11.845c-.796 0-1.441.645-1.441 1.44s.645 1.44 1.441 1.44c.795 0 1.439-.645 1.439-1.44s-.644-1.44-1.439-1.44z"/></svg>';
const skoolIcon = '<svg width="20" height="20" viewBox="0 0 24 24" fill="#5865F2"><path d="M12 3L1 9l11 6 9-4.91V17h2V9L12 3zM5 13.18v4L12 21l7-3.82v-4L12 17l-7-3.82z"/></svg>';

const tweets = output.tweets || [];
const linkedin = output.linkedin || {};
const newsletter = output.newsletter || {};
const instagram = output.instagram || [];
const skool = output.skool || {};

const css = '<style>body{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,sans-serif;background:linear-gradient(135deg,#1a1a2e 0%,#16213e 100%);min-height:100vh;padding:40px 20px;margin:0}.container{max-width:900px;margin:0 auto}.card{background:#fff;border-radius:16px;padding:24px;margin-bottom:20px;box-shadow:0 10px 40px rgba(0,0,0,0.3)}.header{text-align:center;color:#fff;margin-bottom:30px}.header h1{font-size:2.5em;margin:0}.header p{opacity:0.8;margin-top:8px}.preview-badge{display:inline-block;background:#fbbf24;color:#78350f;padding:8px 20px;border-radius:20px;font-weight:600;margin-top:16px}.section-title{display:flex;align-items:center;gap:10px;font-size:1.3em;font-weight:600;color:#333;margin-bottom:16px;padding-bottom:8px;border-bottom:2px solid #667eea}.section-icon{display:flex;align-items:center;color:#667eea}.platform-status{display:inline-block;padding:4px 10px;border-radius:12px;font-size:0.8em;font-weight:500;margin-left:12px}.platform-on{background:#d1fae5;color:#065f46}.platform-warn{background:#fef3c7;color:#92400e}.platform-copy{background:#e0e7ff;color:#3730a3}.idea-list{list-style:none;padding:0;margin:0}.idea-list li{padding:12px 16px;background:#f8f9ff;border-radius:8px;margin-bottom:8px;border-left:4px solid #667eea;color:#1a1a2e}.tweet-card{background:#f8f9ff;border-radius:12px;padding:20px;margin-bottom:16px;border:1px solid #e0e7ff}.tweet-header{display:flex;align-items:center;gap:12px;margin-bottom:12px}.tweet-number{display:inline-flex;align-items:center;justify-content:center;background:#000;color:#fff;width:32px;height:32px;border-radius:50%;font-weight:600}.tweet-type{background:#fef3c7;color:#92400e;padding:4px 12px;border-radius:12px;font-size:0.8em}.tweet-content{font-size:1.1em;line-height:1.6;color:#1a1a2e;margin:0}.linkedin-section{background:#f0f4ff;padding:20px;border-radius:12px}.linkedin-hook{font-size:1.2em;font-weight:600;color:#0077b5;margin-bottom:12px}.linkedin-body{line-height:1.7;color:#333;white-space:pre-line;margin-bottom:16px}.linkedin-question{font-style:italic;color:#555;padding:12px;background:#fff;border-radius:8px;border-left:4px solid #0077b5}.newsletter-section{background:#fef3c7;padding:20px;border-radius:12px}.newsletter-subject{font-size:1.2em;font-weight:600;color:#92400e;margin-bottom:12px}.newsletter-intro{line-height:1.6;color:#333;margin-bottom:16px}.newsletter-points{list-style:none;padding:0;margin:0 0 16px}.newsletter-points li{padding:8px 12px;background:#fff;border-radius:6px;margin-bottom:6px;border-left:3px solid #f59e0b}.newsletter-cta{font-weight:600;color:#b45309}.newsletter-recipients{background:#fff;border-radius:8px;padding:12px;margin-top:16px;border:1px solid #fcd34d}.instagram-section{background:linear-gradient(135deg,#f8f0ff 0%,#fff0f5 100%);padding:20px;border-radius:12px;margin-bottom:16px}.instagram-hook{font-size:1.1em;font-weight:600;color:#E4405F;margin-bottom:10px}.instagram-body{line-height:1.6;color:#333;white-space:pre-line;margin-bottom:12px}.instagram-cta{font-weight:500;color:#833AB4;padding:10px;background:#fff;border-radius:8px;border-left:3px solid #E4405F}.skool-section{background:#f0f4ff;padding:20px;border-radius:12px}.skool-title{font-size:1.3em;font-weight:700;color:#5865F2;margin-bottom:12px}.skool-intro{line-height:1.6;color:#333;margin-bottom:16px}.skool-takeaways{list-style:none;padding:0;margin:0 0 16px}.skool-takeaways li{padding:10px 14px;background:#fff;border-radius:8px;margin-bottom:8px;border-left:3px solid #5865F2}.skool-discussion{font-style:italic;color:#4338ca;padding:14px;background:#e0e7ff;border-radius:8px}.approval-section{background:linear-gradient(135deg,#667eea 0%,#764ba2 100%);padding:30px;border-radius:16px;text-align:center;color:#fff;margin-top:20px}.approval-section h2{margin:0 0 16px}.approval-section p{opacity:0.9;margin-bottom:24px}.approval-btn{display:inline-block;background:#fff;color:#667eea;padding:16px 40px;border-radius:12px;font-size:1.2em;font-weight:600;text-decoration:none;box-shadow:0 4px 15px rgba(0,0,0,0.2);cursor:pointer}.approval-btn:hover{transform:translateY(-2px)}.platform-summary{display:flex;gap:12px;justify-content:center;margin-top:16px;flex-wrap:wrap}.platform-chip{background:rgba(255,255,255,0.2);padding:8px 16px;border-radius:20px;font-size:0.9em}.platform-chip.active{background:rgba(255,255,255,0.9);color:#667eea}</style>';

var html = css;
html += '<div class="container">';
html += '<div class="header"><h1>Content Preview</h1><p>Review your generated content</p>';
html += showApprovalButton ? '<span class="preview-badge">Ready for Approval</span>' : '<span class="preview-badge">Preview Only</span>';
html += '</div>';

// Platform summary
var selectedPlatforms = [];
if (input.platforms.x) selectedPlatforms.push('X/Twitter');
if (input.platforms.linkedin) selectedPlatforms.push('LinkedIn');
if (input.platforms.instagram) selectedPlatforms.push('Instagram');
if (input.platforms.skool) selectedPlatforms.push('Skool');
if (input.platforms.newsletter && recipients.length > 0) selectedPlatforms.push('Newsletter (' + recipients.length + ')');

html += '<div class="card"><div class="section-title">Platforms</div>';
html += '<div style="display:flex;gap:12px;flex-wrap:wrap;">';
if (selectedPlatforms.length > 0) {
  for (var p = 0; p < selectedPlatforms.length; p++) {
    html += '<span class="platform-status platform-on">' + selectedPlatforms[p] + '</span>';
  }
} else {
  html += '<span class="platform-status" style="background:#fee2e2;color:#991b1b;">No platforms selected</span>';
}
html += '</div></div>';

// Key Ideas
html += '<div class="card"><div class="section-title"><span class="section-icon">' + listIcon + '</span> Key Ideas</div><ul class="idea-list">';
var keyIdeas = output.key_ideas || [];
for (var i = 0; i < keyIdeas.length; i++) {
  html += '<li>' + keyIdeas[i] + '</li>';
}
html += '</ul></div>';

// Tweets
if (input.platforms.x && tweets.length > 0) {
  html += '<div class="card"><div class="section-title"><span class="section-icon">' + xIcon + '</span> Tweets (' + tweets.length + ')<span class="platform-status platform-on">Will Post</span></div>';
  for (var j = 0; j < tweets.length; j++) {
    var t = tweets[j];
    html += '<div class="tweet-card"><div class="tweet-header">';
    html += '<span class="tweet-number">' + (j+1) + '</span><span class="tweet-type">' + (t.type || 'tweet') + '</span>';
    html += '</div>';
    html += '<p class="tweet-content">' + (t.content || '') + '</p>';
    html += '</div>';
  }
  html += '</div>';
}

// LinkedIn
if (input.platforms.linkedin && linkedin.hook) {
  html += '<div class="card"><div class="section-title"><span class="section-icon">' + linkedinIcon + '</span> LinkedIn<span class="platform-status platform-on">Will Post</span></div><div class="linkedin-section">';
  html += '<div class="linkedin-hook">' + (linkedin.hook || '') + '</div>';
  html += '<div class="linkedin-body">' + (linkedin.body || '') + '</div>';
  html += '<div class="linkedin-question">' + (linkedin.question || '') + '</div>';
  html += '</div></div>';
}

// Instagram
if (input.platforms.instagram && instagram.length > 0) {
  html += '<div class="card"><div class="section-title"><span class="section-icon">' + instaIcon + '</span> Instagram (' + instagram.length + ')<span class="platform-status platform-copy">Copy to Post</span></div>';
  for (var ig = 0; ig < instagram.length; ig++) {
    var insta = instagram[ig];
    html += '<div class="instagram-section">';
    html += '<div class="instagram-hook">' + (insta.hook || '') + '</div>';
    html += '<div class="instagram-body">' + (insta.body || '') + '</div>';
    html += '<div class="instagram-cta">' + (insta.cta || '') + '</div>';
    html += '</div>';
  }
  html += '</div>';
}

// Skool
if (input.platforms.skool && skool.title) {
  html += '<div class="card"><div class="section-title"><span class="section-icon">' + skoolIcon + '</span> Skool Community<span class="platform-status platform-copy">Copy to Post</span></div><div class="skool-section">';
  html += '<div class="skool-title">' + (skool.title || '') + '</div>';
  html += '<div class="skool-intro">' + (skool.intro || '') + '</div>';
  var takeaways = skool.takeaways || [];
  if (takeaways.length > 0) {
    html += '<ul class="skool-takeaways">';
    for (var tk = 0; tk < takeaways.length; tk++) {
      html += '<li>' + takeaways[tk] + '</li>';
    }
    html += '</ul>';
  }
  html += '<div class="skool-discussion">' + (skool.discussion || '') + '</div>';
  html += '</div></div>';
}

// Newsletter
if (input.platforms.newsletter && newsletter.subject) {
  var recipientStatus = recipients.length > 0 ? 'Will Send to ' + recipients.length : 'No Recipients';
  var statusClass = recipients.length > 0 ? 'platform-on' : 'platform-warn';
  html += '<div class="card"><div class="section-title"><span class="section-icon">' + emailIcon + '</span> Newsletter<span class="platform-status ' + statusClass + '">' + recipientStatus + '</span></div><div class="newsletter-section">';
  html += '<div class="newsletter-subject">Subject: ' + (newsletter.subject || '') + '</div>';
  html += '<div class="newsletter-intro">' + (newsletter.intro || '') + '</div>';
  var points = newsletter.points || [];
  if (points.length > 0) {
    html += '<ul class="newsletter-points">';
    for (var k = 0; k < points.length; k++) {
      html += '<li>' + points[k] + '</li>';
    }
    html += '</ul>';
  }
  html += '<div class="newsletter-cta">CTA: ' + (newsletter.cta || '') + '</div>';
  if (recipients.length > 0) {
    html += '<div class="newsletter-recipients"><strong>From:</strong> ' + senderName + '<br><strong>Recipients:</strong> ' + recipients.slice(0, 5).join(', ') + (recipients.length > 5 ? '... +' + (recipients.length - 5) : '') + '</div>';
  }
  html += '</div></div>';
}

// Approval Button
if (showApprovalButton) {
  var approvalUrl = '/webhook/' + approvalWebhookPath + '?data=' + encodedContent;
  html += '<div class="approval-section">';
  html += '<h2>Ready to Publish?</h2>';
  html += '<p>Review above. X, LinkedIn, Newsletter will auto-post. Instagram/Skool are copy-only.</p>';
  html += '<div class="platform-summary">';
  if (input.platforms.x) html += '<span class="platform-chip active">X Twitter</span>';
  if (input.platforms.linkedin) html += '<span class="platform-chip active">LinkedIn</span>';
  if (input.platforms.newsletter && recipients.length > 0) html += '<span class="platform-chip active">Email</span>';
  html += '</div>';
  html += '<br><br><a class="approval-btn" href="' + approvalUrl + '">Approve and Post</a>';
  html += '</div>';
} else if (input.platforms.instagram || input.platforms.skool) {
  html += '<div class="card" style="text-align:center;padding:30px;background:#f0f4ff;"><h3>Copy-Only Platforms</h3><p>Instagram and Skool content is generated for you to copy and post manually.</p></div>';
} else {
  html += '<div class="card" style="text-align:center;padding:30px;"><h3>Preview Only</h3><p>Select platforms to generate content.</p></div>';
}

html += '</div>';

return [{ json: { html: html } }];'''

# New Decode Payload code for content-approval.json
# Key change: Parse the pipe-delimited format and decode LLM text
DECODE_PAYLOAD_CODE = '''// Decode the simple payload from the approval URL
const query = $json.query || {};
const encodedData = query.data || '';

if (!encodedData) {
  return [{
    json: {
      success: false,
      error: 'No content data provided',
      html: '<html><body><h1>Error</h1><p>No content data found. Please go back and try again.</p></body></html>'
    }
  }];
}

try {
  // Decode the outer base64
  const payloadStr = Buffer.from(encodedData, 'base64').toString('utf-8');
  
  // Parse pipe-delimited format: sessionId|x|linkedin|newsletter|instagram|skool|recipients|senderName|base64LlmText
  const parts = payloadStr.split('|');
  if (parts.length < 9) {
    throw new Error('Invalid payload format');
  }
  
  const sessionId = parts[0];
  const platforms = {
    x: parts[1] === '1',
    linkedin: parts[2] === '1',
    newsletter: parts[3] === '1',
    instagram: parts[4] === '1',
    skool: parts[5] === '1'
  };
  const recipients = parts[6] ? parts[6].split(',').filter(e => e.includes('@')) : [];
  const senderName = parts[7] || 'Newsletter';
  
  // Decode the LLM text from base64
  const llmTextBase64 = parts[8];
  const llmText = Buffer.from(llmTextBase64, 'base64').toString('utf-8');
  
  // Now parse the LLM JSON output
  let content = {};
  try {
    content = JSON.parse(llmText);
  } catch (parseErr) {
    content = {
      key_ideas: ['Error parsing LLM output'],
      tweets: [],
      linkedin: { hook: '', body: '', question: '' },
      newsletter: { subject: '', intro: '', points: [], cta: '' },
      instagram: [],
      skool: { title: '', intro: '', takeaways: [], discussion: '' }
    };
  }
  
  return [{
    json: {
      success: true,
      sessionId: sessionId,
      platforms: platforms,
      content: content,
      newsletter: {
        recipients: recipients,
        senderName: senderName
      },
      createdAt: new Date().toISOString()
    }
  }];
} catch (error) {
  return [{
    json: {
      success: false,
      error: 'Failed to decode content: ' + error.message,
      html: '<html><body><h1>Error</h1><p>Failed to decode content. Please go back and try again.</p></body></html>'
    }
  }];
}'''


def update_generator():
    """Update content-generator.json with new Build Preview Response code"""
    print(f"Reading {GENERATOR_PATH}...")
    with open(GENERATOR_PATH, 'r') as f:
        workflow = json.load(f)
    
    # Find and update the Build Preview Response node
    for node in workflow['nodes']:
        if node.get('name') == 'Build Preview Response':
            node['parameters']['jsCode'] = BUILD_PREVIEW_CODE
            print("Updated Build Preview Response node")
            break
    
    with open(GENERATOR_PATH, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"Saved {GENERATOR_PATH}")


def update_approval():
    """Update content-approval.json with new Decode Payload code"""
    print(f"Reading {APPROVAL_PATH}...")
    with open(APPROVAL_PATH, 'r') as f:
        workflow = json.load(f)
    
    # Find and update the Decode Payload node
    for node in workflow['nodes']:
        if node.get('name') == 'Decode Payload':
            node['parameters']['jsCode'] = DECODE_PAYLOAD_CODE
            print("Updated Decode Payload node")
            break
    
    with open(APPROVAL_PATH, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"Saved {APPROVAL_PATH}")


def validate_json():
    """Validate both JSON files are valid"""
    print("Validating JSON files...")
    with open(GENERATOR_PATH, 'r') as f:
        json.load(f)
    print(f"  {GENERATOR_PATH} is valid")
    
    with open(APPROVAL_PATH, 'r') as f:
        json.load(f)
    print(f"  {APPROVAL_PATH} is valid")


if __name__ == '__main__':
    print("=" * 60)
    print("Updating n8n workflows to use raw LLM output format")
    print("=" * 60)
    
    update_generator()
    update_approval()
    validate_json()
    
    print("\n✅ All workflows updated successfully!")
    print("\nRe-import both workflows in n8n:")
    print("  1. content-generator.json")
    print("  2. content-approval.json")
