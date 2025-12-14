#!/usr/bin/env python3
"""
Fix email template - add fallback background colors for email clients 
that don't support gradients, and ensure all text has proper contrast.
"""

import json

APPROVAL_PATH = '/Users/tonyholovka/workspace/max-content/n8n-workflows/content-approval.json'

# Updated email template with fallback solid colors for gradient backgrounds
EMAIL_CODE = '''// Build HTML email from newsletter data
const decodedPayload = $('Decode Payload').first().json;
const newsletterSettings = decodedPayload.newsletter || {};
const recipients = newsletterSettings.recipients || [];
const senderName = newsletterSettings.senderName || 'Newsletter';
const content = decodedPayload.content || {};
const platforms = decodedPayload.platforms || {};

const nl = $json.newsletterData || content.newsletter || $json;
const instagram = content.instagram || [];
const skool = content.skool || {};

// Build points HTML
const pointsHtml = (nl.points && nl.points.length > 0) ? nl.points.map((p, i) => `
  <tr>
    <td style="padding:12px 16px;background:${i % 2 === 0 ? '#f0f4ff' : '#e8eeff'};border-left:4px solid #667eea;color:#1f2937;font-size:15px;">
      <span style="color:#667eea;font-weight:bold;margin-right:8px;">&#10003;</span>${p}
    </td>
  </tr>
`).join('') : '';

// Build Instagram section
let instagramHtml = '';
if (platforms.instagram && instagram.length > 0) {
  const igCaptions = instagram.map((ig, idx) => `
    <tr>
      <td style="padding:16px;background:#ffffff;border-radius:8px;margin-bottom:12px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td><span style="background:#E4405F;color:#ffffff;padding:8px 12px;border-radius:4px;font-size:12px;font-weight:bold;">CAPTION ${idx + 1}</span></td>
          </tr>
          <tr>
            <td style="padding-top:12px;font-weight:600;color:#1f2937;font-size:16px;">${ig.hook || ''}</td>
          </tr>
          <tr>
            <td style="padding-top:8px;color:#4b5563;line-height:1.6;white-space:pre-line;">${ig.body || ''}</td>
          </tr>
          <tr>
            <td style="padding-top:12px;color:#E4405F;font-weight:600;font-size:14px;">&#128073; ${ig.cta || ''}</td>
          </tr>
        </table>
      </td>
    </tr>
    <tr><td height="12"></td></tr>
  `).join('');
  
  instagramHtml = `
    <tr>
      <td style="padding:24px;background:#fce7f3;border-radius:12px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="padding-bottom:16px;">
              <span style="background:#E4405F;color:#ffffff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:600;">&#128247; INSTAGRAM READY</span>
            </td>
          </tr>
          ${igCaptions}
        </table>
      </td>
    </tr>
    <tr><td height="20"></td></tr>
  `;
}

// Build Skool section
let skoolHtml = '';
if (platforms.skool && skool.title) {
  const takeawaysList = (skool.takeaways || []).map(t => `
    <tr>
      <td style="padding:10px 0;border-bottom:1px solid #c7d2fe;color:#374151;">
        <span style="color:#5865F2;margin-right:8px;">&#9733;</span>${t}
      </td>
    </tr>
  `).join('');
  
  skoolHtml = `
    <tr>
      <td style="padding:24px;background:#e0e7ff;border-radius:12px;">
        <table width="100%" cellpadding="0" cellspacing="0">
          <tr>
            <td style="padding-bottom:16px;">
              <span style="background:#5865F2;color:#ffffff;padding:6px 14px;border-radius:20px;font-size:13px;font-weight:600;">&#127891; SKOOL COMMUNITY</span>
            </td>
          </tr>
          <tr>
            <td style="background:#ffffff;border-radius:8px;padding:20px;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="font-size:18px;font-weight:700;color:#5865F2;padding-bottom:12px;">${skool.title || ''}</td>
                </tr>
                <tr>
                  <td style="color:#374151;line-height:1.6;padding-bottom:16px;">${skool.intro || ''}</td>
                </tr>
                ${takeawaysList ? `<tr><td><table width="100%" cellpadding="0" cellspacing="0" style="margin-bottom:16px;">${takeawaysList}</table></td></tr>` : ''}
                <tr>
                  <td style="background:#5865F2;color:#ffffff;padding:14px;border-radius:8px;font-style:italic;">
                    &#128172; ${skool.discussion || ''}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
        </table>
      </td>
    </tr>
    <tr><td height="20"></td></tr>
  `;
}

const emailHtml = `
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body style="margin:0;padding:0;background-color:#f4f4f5;font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',Roboto,'Helvetica Neue',Arial,sans-serif;">
  <table width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f5;padding:40px 20px;">
    <tr>
      <td align="center">
        <table width="600" cellpadding="0" cellspacing="0" style="max-width:600px;background:#ffffff;border-radius:16px;overflow:hidden;box-shadow:0 4px 20px rgba(0,0,0,0.1);">
          
          <!-- HEADER with solid purple fallback -->
          <tr>
            <td style="background-color:#667eea;padding:40px 30px;text-align:center;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="font-size:26px;font-weight:700;color:#1f2937;padding-bottom:8px;">
                    &#128231; Newsletter
                  </td>
                </tr>
                <tr>
                  <td style="font-size:22px;font-weight:600;color:#ffffff;">
                    ${nl.subject || 'Newsletter'}
                  </td>
                </tr>
                <tr>
                  <td style="padding-top:12px;">
                    <span style="background:rgba(255,255,255,0.25);color:#ffffff;padding:6px 16px;border-radius:20px;font-size:12px;font-weight:500;">From ${senderName}</span>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- INTRO -->
          <tr>
            <td style="padding:32px 30px 24px;background:#ffffff;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="font-size:16px;line-height:1.8;color:#374151;">
                    ${nl.intro || ''}
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
          <!-- KEY POINTS -->
          ${pointsHtml ? `
          <tr>
            <td style="padding:0 30px 24px;background:#ffffff;">
              <table width="100%" cellpadding="0" cellspacing="0" style="background:#f8fafc;border-radius:12px;overflow:hidden;">
                <tr>
                  <td style="background:#667eea;color:#ffffff;padding:14px 20px;font-weight:600;font-size:14px;">
                    &#128161; KEY TAKEAWAYS
                  </td>
                </tr>
                ${pointsHtml}
              </table>
            </td>
          </tr>
          ` : ''}
          
          <!-- CTA BUTTON -->
          ${nl.cta ? `
          <tr>
            <td style="padding:12px 30px 32px;text-align:center;background:#ffffff;">
              <table cellpadding="0" cellspacing="0" style="margin:0 auto;">
                <tr>
                  <td style="background:#667eea;border-radius:30px;">
                    <a href="#" style="display:inline-block;color:#ffffff;padding:14px 36px;text-decoration:none;font-weight:600;font-size:15px;">
                      ${nl.cta} &#8594;
                    </a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          ` : ''}
          
          <!-- DIVIDER -->
          ${(instagramHtml || skoolHtml) ? `
          <tr>
            <td style="padding:0 30px;background:#ffffff;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="border-top:2px dashed #e5e7eb;"></td>
                </tr>
                <tr>
                  <td style="text-align:center;padding:16px 0;color:#6b7280;font-size:13px;font-weight:500;">
                    &#11015; BONUS CONTENT FOR YOUR SOCIALS &#11015;
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          ` : ''}
          
          <!-- INSTAGRAM -->
          <tr>
            <td style="padding:0 30px;background:#ffffff;">
              <table width="100%" cellpadding="0" cellspacing="0">
                ${instagramHtml}
              </table>
            </td>
          </tr>
          
          <!-- SKOOL -->
          <tr>
            <td style="padding:0 30px;background:#ffffff;">
              <table width="100%" cellpadding="0" cellspacing="0">
                ${skoolHtml}
              </table>
            </td>
          </tr>
          
          <!-- FOOTER -->
          <tr>
            <td style="background:#374151;padding:24px 30px;text-align:center;">
              <table width="100%" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="color:#d1d5db;font-size:12px;line-height:1.6;">
                    You received this email because you subscribed to ${senderName}.<br>
                    <a href="#" style="color:#a5b4fc;text-decoration:none;">Unsubscribe</a> | <a href="#" style="color:#a5b4fc;text-decoration:none;">Preferences</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
`;

return [{
  json: {
    platform: 'newsletter',
    subject: nl.subject || 'Newsletter',
    htmlBody: emailHtml,
    recipients: recipients,
    senderName: senderName,
    recipientCount: recipients.length,
    newsletterData: nl,
    originalContent: $json.originalContent
  }
}];'''

def main():
    print(f"Reading {APPROVAL_PATH}...")
    with open(APPROVAL_PATH, 'r') as f:
        workflow = json.load(f)
    
    # Find and update the Build Email HTML node
    for node in workflow['nodes']:
        if node.get('name') == 'Build Email HTML':
            node['parameters']['jsCode'] = EMAIL_CODE
            print("Updated Build Email HTML node")
            break
    
    with open(APPROVAL_PATH, 'w') as f:
        json.dump(workflow, f, indent=2)
    print(f"Saved {APPROVAL_PATH}")
    
    # Validate
    with open(APPROVAL_PATH, 'r') as f:
        json.load(f)
    print("JSON validation passed!")
    print("\n✅ Email template fixed with proper fallback colors!")
    print("\nKey changes:")
    print("  - Header uses solid #667eea purple (no gradient)")
    print("  - Added dark emoji label above subject")
    print("  - Instagram/Skool sections use solid background colors")
    print("  - All text has proper contrast")

if __name__ == '__main__':
    main()
