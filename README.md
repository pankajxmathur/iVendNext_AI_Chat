# iVendNext AI Chat

A production-ready AI Chatbot application for Frappe Framework with multi-provider LLM support and MCP integration.

## Features

- **Multi-Provider LLM Support**: Supports 100+ LLM providers through LiteLLM (OpenAI, Anthropic, Google, Azure, etc.)
- **Modern UI**: Built with assistant-ui React components for a seamless chat experience
- **MCP Integration**: Integrates with Frappe Assistant Core MCP Server for enhanced context
- **Streaming Support**: Real-time streaming responses for better UX
- **Conversation History**: Persistent storage of all conversations
- **Rate Limiting**: Built-in rate limiting and security features
- **Configurable**: Easy configuration through Frappe UI
- **Production Ready**: Error handling, logging, and monitoring

## Quick Installation

```bash
# 1. Get the app
bench get-app https://github.com/pankajxmathur/iVendNext_AI_Chat

# 2. Install on your site
bench --site your-site.local install-app ivendnext_ai_chat --force

# 3. Restart
bench restart

# 4. Configure in UI (see below)
```

**For complete installation instructions, see [FRESH_INSTALL.md](FRESH_INSTALL.md)**

## Configuration

After installation, configure your LLM provider:

1. Login to your Frappe site
2. Search for **"AI Chat Settings"**
3. Check **Enabled**
4. Add a provider (OpenAI, Anthropic, or Ollama)
5. Save and start chatting!

## Configuration

### LLM Providers

Configure your preferred LLM provider in **AI Chat Settings**:

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Google (Gemini)
- Azure OpenAI
- And 100+ more providers

### MCP Server Integration

To integrate with Frappe Assistant Core MCP Server:

1. Install the MCP server:
```bash
npm install -g @buildswithpaul/frappe-assistant-core
```

2. Configure the MCP endpoint in AI Chat Settings

## Usage

### For End Users

1. Navigate to the AI Chat page
2. Start typing your questions
3. Get intelligent responses with Frappe context

### For Developers

```python
import frappe
from ivendnext_ai_chat.api import generate_response

response = generate_response(
    message="What are my open sales orders?",
    user=frappe.session.user,
    conversation_id="conv-123"
)
```

## Architecture

```
Frontend (React + assistant-ui)
    ↓
Frappe API Layer
    ↓
LiteLLM Provider Layer
    ↓
Multiple LLM Providers (OpenAI, Claude, etc.)
    ↓
MCP Server (Frappe Assistant Core)
```

## Security

- API key encryption in database
- Rate limiting per user
- Permission-based access control
- Audit logging of all conversations

## License

MIT
