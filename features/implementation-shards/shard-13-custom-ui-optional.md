# Shard 13: Custom UI (OPTIONAL BONUS)

## Content Repurposing Engine

**Est. Time:** 60-90 min | **Depends on:** Shard 11 (workflow working) | **Priority:** LOW - Only if time permits

---

## Overview

This shard creates a custom web UI that looks more polished than the default n8n form. It's hosted on the same VPS and calls the n8n webhook.

**Only attempt this if:**

- ✅ All core shards (01-11) complete
- ✅ Workflow fully tested and working
- ✅ At least 3-4 hours remaining before deadline
- ✅ Demo video not yet recorded (UI appears in video)

---

## Part A: Convert Form Trigger to Webhook

### 13.1 Add Webhook Node

In your n8n workflow:

1. [ ] Add **Webhook** node (keep Form Trigger as backup)
2. [ ] Name: `Custom UI Webhook`
3. [ ] HTTP Method: `POST`
4. [ ] Path: `content-engine`
5. [ ] Response Mode: `When Last Node Finishes`
6. [ ] Copy the Webhook URL:

```
Webhook URL: http://YOUR_VPS_IP:5678/webhook/content-engine
```

### 13.2 Connect Webhook to Workflow

1. [ ] Connect Webhook → Set Metadata (same as Form Trigger was)
2. [ ] Update Set Metadata expressions to use webhook data:
   - `{{ $json.body.video_title }}`
   - `{{ $json.body.transcript }}`
   - etc.
3. [ ] Test with curl:

```bash
curl -X POST http://YOUR_VPS_IP:5678/webhook/content-engine \
  -H "Content-Type: application/json" \
  -d '{"video_title":"Test","transcript":"Test content","niche":"AI/Business"}'
```

- [ ] Webhook triggers workflow successfully

---

## Part B: Create Simple Web UI

### 13.3 Create HTML File

SSH to your VPS:

```bash
mkdir -p /var/www/content-engine
nano /var/www/content-engine/index.html
```

Paste this HTML:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Content Repurposing Engine</title>
    <style>
      * {
        box-sizing: border-box;
        margin: 0;
        padding: 0;
      }
      body {
        font-family:
          -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 100%);
        min-height: 100vh;
        display: flex;
        justify-content: center;
        align-items: center;
        padding: 20px;
      }
      .container {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 24px;
        padding: 40px;
        width: 100%;
        max-width: 600px;
        box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);
      }
      h1 {
        color: #fff;
        font-size: 28px;
        margin-bottom: 8px;
        text-align: center;
      }
      .subtitle {
        color: rgba(255, 255, 255, 0.6);
        text-align: center;
        margin-bottom: 32px;
        font-size: 14px;
      }
      label {
        display: block;
        color: rgba(255, 255, 255, 0.8);
        margin-bottom: 8px;
        font-size: 14px;
        font-weight: 500;
      }
      input,
      textarea,
      select {
        width: 100%;
        padding: 14px 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        background: rgba(255, 255, 255, 0.05);
        color: #fff;
        font-size: 16px;
        margin-bottom: 20px;
        transition: border-color 0.2s;
      }
      input:focus,
      textarea:focus,
      select:focus {
        outline: none;
        border-color: #6366f1;
      }
      textarea {
        min-height: 200px;
        resize: vertical;
      }
      select option {
        background: #1a1a2e;
      }
      button {
        width: 100%;
        padding: 16px;
        background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%);
        border: none;
        border-radius: 12px;
        color: #fff;
        font-size: 16px;
        font-weight: 600;
        cursor: pointer;
        transition:
          transform 0.2s,
          box-shadow 0.2s;
      }
      button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 30px rgba(99, 102, 241, 0.4);
      }
      button:disabled {
        opacity: 0.6;
        cursor: not-allowed;
        transform: none;
      }
      .status {
        margin-top: 20px;
        padding: 16px;
        border-radius: 12px;
        text-align: center;
        display: none;
      }
      .status.loading {
        display: block;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
      }
      .status.success {
        display: block;
        background: rgba(34, 197, 94, 0.2);
        color: #86efac;
      }
      .status.error {
        display: block;
        background: rgba(239, 68, 68, 0.2);
        color: #fca5a5;
      }
      .badge {
        display: inline-block;
        background: rgba(99, 102, 241, 0.2);
        color: #a5b4fc;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        margin-bottom: 24px;
      }
    </style>
  </head>
  <body>
    <div class="container">
      <div style="text-align:center">
        <span class="badge">🚀 n8n + Gemini Powered</span>
      </div>
      <h1>Content Repurposing Engine</h1>
      <p class="subtitle">
        Transform video transcripts into platform-ready social content
      </p>

      <form id="contentForm">
        <label for="title">Video Title *</label>
        <input
          type="text"
          id="title"
          name="video_title"
          required
          placeholder="e.g., How to Build an AI Business"
        />

        <label for="url">Video URL</label>
        <input
          type="url"
          id="url"
          name="video_url"
          placeholder="https://youtube.com/..."
        />

        <label for="transcript">Transcript *</label>
        <textarea
          id="transcript"
          name="transcript"
          required
          placeholder="Paste your video transcript here..."
        ></textarea>

        <label for="niche">Target Niche</label>
        <select id="niche" name="niche">
          <option value="AI/Business">AI / Business</option>
          <option value="Entrepreneurship">Entrepreneurship</option>
          <option value="Tech">Tech</option>
          <option value="Other">Other</option>
        </select>

        <button type="submit" id="submitBtn">✨ Generate Content</button>
      </form>

      <div id="status" class="status"></div>
    </div>

    <script>
      const WEBHOOK_URL = "http://YOUR_VPS_IP:5678/webhook/content-engine";

      document
        .getElementById("contentForm")
        .addEventListener("submit", async (e) => {
          e.preventDefault();

          const btn = document.getElementById("submitBtn");
          const status = document.getElementById("status");

          btn.disabled = true;
          btn.textContent = "⏳ Processing...";
          status.className = "status loading";
          status.textContent =
            "Generating content... This may take 1-2 minutes.";

          try {
            const formData = new FormData(e.target);
            const data = Object.fromEntries(formData.entries());

            const response = await fetch(WEBHOOK_URL, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(data),
            });

            if (response.ok) {
              status.className = "status success";
              status.textContent =
                "✅ Content generated! Check Google Sheets for your posts.";
            } else {
              throw new Error("Workflow failed");
            }
          } catch (error) {
            status.className = "status error";
            status.textContent = "❌ Error: " + error.message;
          } finally {
            btn.disabled = false;
            btn.textContent = "✨ Generate Content";
          }
        });
    </script>
  </body>
</html>
```

**IMPORTANT:** Replace `YOUR_VPS_IP` in the JavaScript with your actual VPS IP.

- [ ] HTML file created

---

## Part C: Serve the UI

### 13.4 Option 1: Use Python Simple Server

Quick way to serve the HTML:

```bash
cd /var/www/content-engine
python3 -m http.server 8080 &
```

Access at: `http://YOUR_VPS_IP:8080`

- [ ] UI accessible in browser

### 13.5 Option 2: Use Nginx (More Robust)

```bash
apt install -y nginx

# Create nginx config
cat > /etc/nginx/sites-available/content-engine << 'EOF'
server {
    listen 80;
    server_name YOUR_VPS_IP;

    location / {
        root /var/www/content-engine;
        index index.html;
    }
}
EOF

ln -s /etc/nginx/sites-available/content-engine /etc/nginx/sites-enabled/
nginx -t
systemctl restart nginx
```

Access at: `http://YOUR_VPS_IP` (port 80)

- [ ] Nginx serving UI

### 13.6 Allow Port in Firewall

```bash
ufw allow 8080  # if using Python
# or port 80 already allowed for nginx
```

---

## Part D: Test Full Flow

### 13.7 End-to-End Test

1. [ ] Open `http://YOUR_VPS_IP:8080` (or `:80`)
2. [ ] Fill in form with test data
3. [ ] Click "Generate Content"
4. [ ] See "Processing..." status
5. [ ] After 1-2 min, see "Success" message
6. [ ] Check Google Sheets - content should appear

---

## Verification Checklist

- [ ] Webhook node added to workflow
- [ ] HTML file created and served
- [ ] Custom UI accessible via browser
- [ ] Form submission triggers n8n workflow
- [ ] Content appears in Google Sheets
- [ ] UI looks polished for demo video

---

## UI Preview

The custom UI features:

- 🌙 Dark glassmorphic design
- 📱 Mobile responsive
- ✨ Animated submit button
- 📊 Loading/success/error states
- 🏷️ "n8n + Gemini Powered" badge

---

## Demo Video Update

If using custom UI, update demo video shots:

| Time      | What to Show                     |
| --------- | -------------------------------- |
| 0:10-0:25 | Custom UI instead of n8n form    |
| 0:25-0:30 | Click submit, show loading state |
| ...       | Rest of demo same as before      |

---

## Fallback

If custom UI has issues:

- Keep the n8n Form Trigger connected
- Use that for the demo instead
- Don't debug UI issues close to deadline

---

_This is an OPTIONAL bonus. Only complete if core workflow is solid!_
