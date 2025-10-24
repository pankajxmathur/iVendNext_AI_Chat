# Installation Guide - iVendNext AI Chat

Complete installation and setup guide for the AI Chat application.

## Prerequisites

- Frappe Framework (v14 or higher)
- Node.js (v18 or higher)
- Python (v3.10 or higher)
- npm or yarn

## Step 1: Install the App

### From Git Repository

```bash
# Get the app
bench get-app https://github.com/yourusername/iVendNext_AI_Chat

# Install on your site
bench --site your-site.local install-app ivendnext_ai_chat
```

### Local Development

```bash
# Clone the repository
cd frappe-bench/apps
git clone https://github.com/yourusername/iVendNext_AI_Chat

# Install app
bench --site your-site.local install-app ivendnext_ai_chat
```

## Step 2: Install Dependencies

### Python Dependencies

```bash
cd frappe-bench/apps/iVendNext_AI_Chat
pip install -r requirements.txt
```

### Frontend Dependencies

```bash
cd frappe-bench/apps/iVendNext_AI_Chat
npm install

# Build frontend
npm run build
```

## Step 3: Configure AI Chat Settings

1. Login to your Frappe site
2. Go to **AI Chat Settings**
3. Enable the AI Chat
4. Configure your LLM provider:

### OpenAI Configuration

```
Provider Name: OpenAI
Model Name: gpt-4
API Key: sk-your-api-key-here
```

### Anthropic (Claude) Configuration

```
Provider Name: Anthropic
Model Name: claude-3-sonnet-20240229
API Key: sk-ant-your-api-key-here
```

### Google (Gemini) Configuration

```
Provider Name: Google
Model Name: gemini-pro
API Key: your-google-api-key
```

### Azure OpenAI Configuration

```
Provider Name: Azure OpenAI
Model Name: your-deployment-name
API Key: your-azure-api-key
API Base URL: https://your-resource.openai.azure.com
```

### Ollama (Local) Configuration

```
Provider Name: Ollama
Model Name: llama2
API Base URL: http://localhost:11434
```

## Step 4: MCP Integration (Optional)

If you want to integrate with Frappe Assistant Core MCP Server:

### Install MCP Server

```bash
# Install Frappe Assistant Core
npm install -g @buildswithpaul/frappe-assistant-core

# Or clone and run locally
git clone https://github.com/buildswithpaul/Frappe_Assistant_Core
cd Frappe_Assistant_Core
npm install
npm start
```

### Configure in AI Chat Settings

1. Enable MCP in AI Chat Settings
2. Set MCP Server URL: `http://localhost:3000` (or your MCP server URL)
3. Set timeout (default: 30 seconds)

## Step 5: Build and Deploy

```bash
# Build assets
bench build --app ivendnext_ai_chat

# Clear cache
bench --site your-site.local clear-cache

# Restart bench
bench restart
```

## Step 6: Verify Installation

1. Login to your site
2. You should see an "AI Chat" button in the toolbar
3. Click to open the chat interface
4. Send a test message

## Configuration Options

### System Prompt

Customize the system prompt to change the AI's behavior:

```
AI Chat Settings > System Prompt
```

Example prompts:
- "You are a helpful assistant specializing in ERP systems."
- "You are a technical support expert for Frappe Framework."
- "You help users with their business questions."

### Rate Limiting

Prevent abuse by setting rate limits:

```
AI Chat Settings > Rate Limit Per User
Default: 100 messages per hour
```

### Model Parameters

Fine-tune the AI responses:

```
Temperature: 0.7 (0.0 = deterministic, 1.0 = creative)
Max Tokens: 2000 (maximum response length)
Max Conversation Length: 50 (number of previous messages to include)
```

### Features

Enable/disable features:

- **Enable Streaming**: Real-time response streaming
- **Enable Markdown**: Render markdown in responses
- **Enable Code Highlighting**: Syntax highlighting for code blocks
- **Enable Conversation History**: Store conversation history

## Troubleshooting

### API Key Issues

If you get authentication errors:

1. Verify your API key is correct
2. Check the provider is enabled
3. Ensure you have sufficient API credits

### MCP Connection Issues

If MCP integration fails:

1. Verify MCP server is running
2. Check the MCP server URL is correct
3. Check firewall settings
4. Review MCP server logs

### Frontend Build Issues

If frontend doesn't load:

```bash
# Rebuild frontend
cd frappe-bench/apps/iVendNext_AI_Chat
npm run build

# Clear cache
bench --site your-site.local clear-cache

# Restart
bench restart
```

### Rate Limit Issues

If users are hitting rate limits:

1. Increase rate limit in AI Chat Settings
2. Or reset for specific user:
   ```python
   frappe.call('ivendnext_ai_chat.utils.rate_limiter.reset_rate_limit', {user: 'user@example.com'})
   ```

## Security Best Practices

1. **API Keys**: Store API keys securely, never commit to git
2. **Rate Limiting**: Set appropriate rate limits
3. **Permissions**: Configure DocType permissions appropriately
4. **Logging**: Enable logging for audit trails
5. **HTTPS**: Always use HTTPS in production

## Updating the App

```bash
# Pull latest changes
cd frappe-bench/apps/iVendNext_AI_Chat
git pull

# Update dependencies
pip install -r requirements.txt
npm install

# Rebuild
npm run build
bench build --app ivendnext_ai_chat

# Migrate
bench --site your-site.local migrate

# Clear cache and restart
bench --site your-site.local clear-cache
bench restart
```

## Support

For issues and support:
- GitHub Issues: https://github.com/yourusername/iVendNext_AI_Chat/issues
- Documentation: See README.md

## Next Steps

- Customize the system prompt for your use case
- Configure MCP integration for enhanced Frappe context
- Set up rate limits based on your usage
- Train users on how to use the AI assistant
- Monitor usage and costs
