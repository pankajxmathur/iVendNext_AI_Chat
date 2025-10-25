# Fresh Installation Guide

Complete guide for installing iVendNext AI Chat on a fresh Frappe instance.

## Prerequisites

- Frappe Framework v14 or higher
- Python 3.10+
- Node.js 18+
- Valid LLM provider API key (OpenAI/Anthropic) OR Ollama installed locally

## Installation Steps

### 1. Install the App

```bash
cd ~/frappe-bench

# Get the app
bench get-app https://github.com/pankajxmathur/iVendNext_AI_Chat

# Install on your site
bench --site your-site.local install-app ivendnext_ai_chat --force

# Restart
bench restart
```

**Expected Output:**
```
Installing ivendnext_ai_chat...
Setting up iVendNext AI Chat...
✓ Created default AI Chat Settings
✓ Created AI Chat button script
iVendNext AI Chat setup complete!

============================================================
Next Steps:
1. Go to AI Chat Settings
2. Enable the app
3. Add your LLM provider (OpenAI/Anthropic/Ollama)
4. Save and start chatting!
============================================================
```

### 2. Configure Your LLM Provider

Login to your Frappe site and configure one of these options:

#### Option A: OpenAI (Recommended for Production)

1. Get API key from https://platform.openai.com/api-keys
2. Add billing at https://platform.openai.com/settings/organization/billing
3. In Frappe, search for **"AI Chat Settings"**
4. Configure:
   ```
   ✓ Enabled
   Default Provider: OpenAI

   Provider Configuration (Add Row):
   - Provider Name: OpenAI
   - Model Name: gpt-3.5-turbo (or gpt-4)
   - API Key: sk-your-api-key-here
   - Enabled: ✓

   Save
   ```

#### Option B: Anthropic Claude

1. Get API key from https://console.anthropic.com/
2. In **AI Chat Settings**:
   ```
   ✓ Enabled
   Default Provider: Anthropic

   Provider Configuration (Add Row):
   - Provider Name: Anthropic
   - Model Name: claude-3-sonnet-20240229
   - API Key: sk-ant-your-api-key-here
   - Enabled: ✓

   Save
   ```

#### Option C: Ollama (FREE - Local)

1. Install Ollama:
   ```bash
   curl -fsSL https://ollama.com/install.sh | sh
   ollama pull llama2
   ```

2. In **AI Chat Settings**:
   ```
   ✓ Enabled
   Default Provider: Ollama

   Provider Configuration (Add Row):
   - Provider Name: Ollama
   - Model Name: llama2
   - API Base URL: http://localhost:11434
   - Enabled: ✓

   Save
   ```

### 3. Verify Installation

1. **Refresh browser** (Ctrl+Shift+R)
2. Look for **"AI Chat"** button in the top toolbar
3. Click it and type a test message
4. You should get a response!

## Troubleshooting

### Chat button not visible

**Solution 1: Hard refresh**
```
Ctrl + Shift + R (Windows/Linux)
Cmd + Shift + R (Mac)
```

**Solution 2: Check Client Script**
1. Go to **Client Script** list
2. Find "AI Chat Button"
3. Make sure it's **Enabled**
4. Refresh browser

**Solution 3: Recreate manually**
```bash
bench --site your-site.local console
```

Then:
```python
from ivendnext_ai_chat.install import add_chat_button_script
add_chat_button_script()
exit()
```

### "AI Chat is not enabled" error

**Solution:**
1. Go to **AI Chat Settings**
2. Check the **Enabled** checkbox
3. Make sure **Default Provider** is set
4. Save

### "No default provider configured" error

**Solution:**
1. Go to **AI Chat Settings**
2. Add at least one provider in **Provider Configuration**
3. Set **Default Provider** to match
4. Save

### API authentication errors

**OpenAI:**
- Verify API key is correct
- Check you have credits: https://platform.openai.com/usage
- Check billing: https://platform.openai.com/settings/organization/billing

**Anthropic:**
- Verify API key format: `sk-ant-...`
- Check quota at: https://console.anthropic.com/

**Ollama:**
- Verify Ollama is running: `ollama list`
- Check URL: `http://localhost:11434`
- Verify model is pulled: `ollama pull llama2`

### Rate limit exceeded

**Solution:**
```python
# Reset rate limit for a user
bench --site your-site.local console
```

```python
from ivendnext_ai_chat.utils.rate_limiter import RateLimiter
limiter = RateLimiter()
limiter.reset('user@example.com')
exit()
```

Or increase in **AI Chat Settings** > **Rate Limit Per User**

### Build errors during installation

**If you get build errors**, they can be safely ignored. The app works without frontend build:

```bash
# Skip build errors and continue
bench --site your-site.local install-app ivendnext_ai_chat --force
```

The chat button is added via Client Script, not the build system.

## Post-Installation Configuration

### Customize System Prompt

In **AI Chat Settings**, edit **System Prompt**:

```
You are an expert assistant for [YOUR COMPANY].
You help users with [SPECIFIC TASKS].
You have knowledge of [YOUR DOMAIN].
```

### Adjust Model Parameters

- **Temperature** (0.0-1.0): Lower = more focused, Higher = more creative
- **Max Tokens**: Maximum response length
- **Max Conversation Length**: How many previous messages to remember

### Enable MCP (Optional)

For Frappe-context-aware responses:

```bash
npm install -g @buildswithpaul/frappe-assistant-core
```

Then in **AI Chat Settings**:
- Enable MCP: ✓
- MCP Server URL: http://localhost:3000

## Verification Checklist

- [ ] App installed without errors
- [ ] AI Chat Settings created
- [ ] Provider configured with API key
- [ ] Chat button appears in toolbar
- [ ] Can send a test message
- [ ] Receive AI response
- [ ] Conversation saved in database

## Next Steps

- Monitor token usage in **AI Chat Conversation**
- Review conversation history
- Customize system prompt for your use case
- Set appropriate rate limits
- Train users on features

## Support

- GitHub Issues: https://github.com/pankajxmathur/iVendNext_AI_Chat/issues
- Documentation: See README.md and API.md
- Examples: Check examples/ directory

---

**Congratulations!** Your AI Chat is ready to use! 🎉
