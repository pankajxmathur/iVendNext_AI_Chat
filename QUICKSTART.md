# Quick Start Guide

Get started with iVendNext AI Chat in 5 minutes!

## Installation

### Step 1: Get the App

```bash
cd ~/frappe-bench
bench get-app https://github.com/pankajxmathur/iVendNext_AI_Chat
```

### Step 2: Install on Your Site

```bash
bench --site your-site.local install-app ivendnext_ai_chat
```

### Step 3: Install Python Dependencies

```bash
cd apps/iVendNext_AI_Chat
pip install -r requirements.txt
```

### Step 4: Build Assets

```bash
bench build --app ivendnext_ai_chat
bench clear-cache
bench restart
```

## Configuration

### Step 5: Configure AI Chat Settings

1. Login to your site
2. Search for "AI Chat Settings" in the search bar
3. Check "Enabled"
4. Configure your LLM provider:

#### For OpenAI (Recommended for beginners):

```
Provider Configuration:
- Add Row
- Provider Name: OpenAI
- Model Name: gpt-4
- API Key: sk-your-openai-api-key
- Enabled: ✓

Default Provider: OpenAI
Temperature: 0.7
Max Tokens: 2000
```

#### For Anthropic (Claude):

```
Provider Configuration:
- Add Row
- Provider Name: Anthropic
- Model Name: claude-3-sonnet-20240229
- API Key: sk-ant-your-api-key
- Enabled: ✓

Default Provider: Anthropic
```

#### For Local/Ollama (No API key needed):

```bash
# First install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull llama2
```

Then configure:
```
Provider Configuration:
- Add Row
- Provider Name: Ollama
- Model Name: llama2
- API Base URL: http://localhost:11434
- Enabled: ✓

Default Provider: Ollama
```

5. Click "Save"

## Usage

### Step 6: Start Chatting!

1. You'll see an "AI Chat" button in the top toolbar
2. Click it to open the chat dialog
3. Type your message and press Enter or click Send
4. Wait for the AI response

### Example Queries:

- "What is Frappe Framework?"
- "How do I create a new DocType?"
- "Explain the hooks.py file"
- "What are the best practices for Frappe development?"

## Troubleshooting

### Issue: "AI Chat is not enabled"
**Solution:** Go to AI Chat Settings and check the "Enabled" checkbox

### Issue: "No default provider configured"
**Solution:** Add at least one provider in AI Chat Settings and set it as Default Provider

### Issue: Rate limit exceeded
**Solution:** Wait an hour or increase the rate limit in AI Chat Settings (System Manager only)

### Issue: API authentication error
**Solution:**
- Check your API key is correct
- Make sure you have credits/quota with your provider
- For OpenAI: Check at https://platform.openai.com/api-keys
- For Anthropic: Check at https://console.anthropic.com/

### Issue: Chat button not appearing
**Solution:**
```bash
bench build --app ivendnext_ai_chat
bench clear-cache
bench restart
# Clear browser cache and hard refresh (Ctrl+Shift+R)
```

## Advanced Features

### MCP Integration (Optional)

For enhanced Frappe context, install the MCP server:

```bash
npm install -g @buildswithpaul/frappe-assistant-core
```

Then in AI Chat Settings:
- Enable MCP: ✓
- MCP Server URL: http://localhost:3000

### Streaming Responses

Streaming is enabled by default for real-time responses. To disable:
- Go to AI Chat Settings
- Uncheck "Enable Streaming"

### Conversation History

All conversations are automatically saved. View them:
1. Go to "AI Chat Conversation" doctype
2. See all your past conversations
3. Click to view details

## API Usage

Use the Python API in your custom scripts:

```python
import frappe

# Send a message
response = frappe.call(
    'ivendnext_ai_chat.api.send_message',
    message="What is Frappe?"
)

print(response['message'])
```

## Next Steps

- Read the [full documentation](README.md)
- Check out [API documentation](API.md)
- Review [code examples](examples/)
- Customize the system prompt for your use case
- Set up MCP for Frappe context awareness

## Support

- GitHub Issues: https://github.com/pankajxmathur/iVendNext_AI_Chat/issues
- Frappe Forum: https://discuss.frappe.io/

## Tips

1. **Start with OpenAI GPT-3.5** - It's faster and cheaper for testing
2. **Use Ollama for development** - Free, runs locally, no API costs
3. **Set rate limits** - Prevent unexpected API costs
4. **Monitor token usage** - Check AI Chat Conversation for token counts
5. **Customize system prompt** - Tailor the AI to your specific needs

---

**That's it! You're ready to use AI Chat in your Frappe site!** 🚀
