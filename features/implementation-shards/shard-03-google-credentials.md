# Shard 03: Google Credentials Setup

## Content Repurposing Engine

**Estimated Time:** 30-45 minutes  
**Dependencies:** Shard 02 (n8n running)  
**Outcome:** Gemini API + Google Sheets credentials in n8n

---

## Prerequisites

- [ ] Shard 02 complete (n8n accessible in browser)
- [ ] Google account available
- [ ] n8n dashboard open

---

## Part A: Google Gemini API Key

### 3.1 Access Google AI Studio

- [ ] Navigate to: https://aistudio.google.com/
- [ ] Sign in with your Google account
- [ ] Accept terms if prompted

### 3.2 Create API Key

- [ ] Click **"Get API Key"** in the left sidebar
- [ ] Click **"Create API Key"**
- [ ] Select an existing Google Cloud project OR create new
- [ ] Copy the API key that appears

**IMPORTANT:** Save this key securely - you can't view it again!

```
Gemini API Key: ________________________________________________
```

- [ ] API key copied and saved

### 3.3 Verify API Key

Test in terminal (optional):

```bash
curl "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key=YOUR_API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{"contents":[{"parts":[{"text":"Say hello"}]}]}'
```

- [ ] Response contains generated text (or skip this step)

### 3.4 Add Gemini Credential to n8n

1. [ ] Open n8n in browser
2. [ ] Go to **Settings** (gear icon) → **Credentials**
3. [ ] Click **Add Credential**
4. [ ] Search for "**Google Gemini**" or "**Google PaLM**"
   - If not found, search for "**HTTP Header Auth**" (we'll use HTTP Request node)
5. [ ] For **Google Gemini Chat Model**:
   - Name: `Gemini API`
   - API Key: (paste your key)
6. [ ] Click **Save**

- [ ] Gemini credential created in n8n

---

## Part B: Google Sheets OAuth Connection

### 3.5 Enable Google Sheets API

1. [ ] Go to: https://console.cloud.google.com/
2. [ ] Select or create a project (same as Gemini, or new)
3. [ ] Navigate to **APIs & Services** → **Library**
4. [ ] Search for "**Google Sheets API**"
5. [ ] Click **Enable**
6. [ ] Also enable "**Google Drive API**" (for file access)

- [ ] Both APIs enabled

### 3.6 Create OAuth Credentials

1. [ ] Go to **APIs & Services** → **Credentials**
2. [ ] Click **Create Credentials** → **OAuth client ID**
3. [ ] If prompted, configure OAuth consent screen:
   - User Type: **External**
   - App name: `Content Repurposing Engine`
   - User support email: (your email)
   - Developer contact: (your email)
   - Scopes: Skip for now
   - Test users: Add your Google email
   - Save and continue
4. [ ] Back to Credentials → **Create Credentials** → **OAuth client ID**
5. [ ] Application type: **Web application**
6. [ ] Name: `n8n Sheets Integration`
7. [ ] Authorized redirect URIs: Add:
   ```
   http://YOUR_VPS_IP:5678/rest/oauth2-credential/callback
   ```
8. [ ] Click **Create**
9. [ ] Copy **Client ID** and **Client Secret**

```
OAuth Client ID: ________________________________________________
OAuth Client Secret: ____________________________________________
```

- [ ] OAuth credentials created

### 3.7 Add Google Sheets Credential to n8n

1. [ ] Open n8n → **Settings** → **Credentials**
2. [ ] Click **Add Credential**
3. [ ] Search for "**Google Sheets**"
4. [ ] Select **Google Sheets OAuth2 API**
5. [ ] Fill in:
   - Credential Name: `Google Sheets`
   - Client ID: (paste)
   - Client Secret: (paste)
6. [ ] Click **Sign in with Google** button
7. [ ] Authorize n8n to access your Google account
8. [ ] Grant permissions for Sheets and Drive

- [ ] Google Sheets credential connected (shows green checkmark)

---

## Part C: Verify Credentials

### 3.8 Test Gemini Connection

1. [ ] Create new workflow in n8n
2. [ ] Add **Google Gemini Chat Model** node
3. [ ] Select your Gemini credential
4. [ ] Model: `gemini-1.5-flash`
5. [ ] Add a simple message: "Say hello"
6. [ ] Execute node
7. [ ] Verify response appears

- [ ] Gemini test successful

### 3.9 Test Google Sheets Connection

1. [ ] In same test workflow, add **Google Sheets** node
2. [ ] Credential: Select your Google Sheets credential
3. [ ] Operation: **Read Rows**
4. [ ] Try to browse your Google Drive
5. [ ] Should see your files/folders

- [ ] Google Sheets connection working

### 3.10 Clean Up Test Workflow

- [ ] Delete the test workflow (or save as "Credentials Test")

---

## Verification Checklist

| Check             | Method                      | Expected Result         |
| ----------------- | --------------------------- | ----------------------- |
| Gemini API        | Test node execution         | Returns text response   |
| Sheets OAuth      | Browse Drive in Sheets node | Shows your files        |
| Credentials saved | Settings → Credentials      | Both credentials listed |

---

## Troubleshooting

### Gemini API returns error

- Verify API key is correct (no extra spaces)
- Check free tier limits at https://aistudio.google.com/
- Ensure API is enabled in Google Cloud Console

### Google Sheets OAuth fails

- Verify redirect URI exactly matches (including http vs https)
- Check that both Sheets API and Drive API are enabled
- Ensure your email is added as test user in OAuth consent screen

### OAuth consent screen in "Testing" mode

- This is fine for hackathon
- Only your added test users can connect
- For production: publish the app

### "Access blocked" error

- Add your email to test users in OAuth consent screen
- Wait a few minutes for propagation

---

## Completion Checklist

- [ ] Gemini API key created and saved in n8n
- [ ] Google Cloud project set up
- [ ] Sheets API and Drive API enabled
- [ ] OAuth credentials created
- [ ] n8n connected to Google Sheets
- [ ] Both credentials tested and working

---

## Credentials Summary

```
Gemini API Key: ________________ (stored in n8n)
OAuth Client ID: _______________ (stored in n8n)
Google Account: ________________ (connected)
```

---

## Next Shard

Once all items checked, proceed to:
**→ Shard 04: Google Sheets Structure**

---

_Your LLM and storage connections are now ready!_
