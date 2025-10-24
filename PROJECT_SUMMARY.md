# iVendNext AI Chat - Project Summary

## Overview

iVendNext AI Chat is a **production-ready AI chatbot application** for Frappe Framework that provides:
- Multi-provider LLM support (100+ providers via LiteLLM)
- Modern React UI with assistant-ui components
- MCP (Model Context Protocol) integration with Frappe Assistant Core
- Real-time streaming responses
- Comprehensive security and rate limiting
- Full conversation history management

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                          │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  React + TypeScript + assistant-ui                   │   │
│  │  - ChatInterface Component                           │   │
│  │  - Frappe Runtime Adapter                            │   │
│  │  - Streaming Support                                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕ HTTP/SSE
┌─────────────────────────────────────────────────────────────┐
│                    Frappe API Layer                         │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Whitelisted API Endpoints (api.py)                  │   │
│  │  - send_message, stream_message                      │   │
│  │  - conversation management                           │   │
│  │  - MCP tool execution                                │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Security & Rate Limiting                            │   │
│  │  - Input sanitization                                │   │
│  │  - Permission checks                                 │   │
│  │  - Rate limiter (per-user, per-hour)                 │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                   Business Logic Layer                      │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  LLM Provider (llm_provider.py)                      │   │
│  │  - LiteLLM integration                               │   │
│  │  - Multi-provider support                            │   │
│  │  - Streaming & completion                            │   │
│  │  - Token counting                                    │   │
│  └──────────────────────────────────────────────────────┘   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  MCP Integration (mcp_integration.py)                │   │
│  │  - Frappe Assistant Core client                     │   │
│  │  - Context enhancement                               │   │
│  │  - Tool execution                                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    Data Persistence Layer                   │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Frappe DocTypes                                     │   │
│  │  - AI Chat Settings (single)                         │   │
│  │  - AI Chat Conversation                              │   │
│  │  - AI Chat Message                                   │   │
│  │  - AI Chat Provider (child table)                    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            ↕
┌─────────────────────────────────────────────────────────────┐
│                    External Services                        │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │  LLM Providers   │  │  MCP Server                  │    │
│  │  - OpenAI        │  │  (Frappe Assistant Core)     │    │
│  │  - Anthropic     │  │  - Context provision         │    │
│  │  - Google        │  │  - Tool execution            │    │
│  │  - Azure         │  │  - Frappe integration        │    │
│  │  - Ollama        │  └──────────────────────────────┘    │
│  │  - 100+ more     │                                       │
│  └──────────────────┘                                       │
└─────────────────────────────────────────────────────────────┘
```

## Key Components

### Backend (Python)

1. **LLM Provider** (`llm_provider.py`)
   - Unified interface to 100+ LLM providers via LiteLLM
   - Support for streaming and completion modes
   - Conversation history management
   - Token counting and usage tracking

2. **MCP Integration** (`mcp_integration.py`)
   - Client for Frappe Assistant Core MCP Server
   - Context enhancement for better responses
   - Tool execution capabilities
   - Async/sync adapters

3. **API Layer** (`api.py`)
   - RESTful API endpoints
   - Server-Sent Events for streaming
   - Conversation management
   - Settings access

4. **Security** (`utils/security.py`)
   - Input sanitization (XSS prevention)
   - Permission validation
   - API key management
   - Audit logging

5. **Rate Limiting** (`utils/rate_limiter.py`)
   - Per-user rate limits
   - Hourly windows
   - Configurable limits
   - System Manager bypass

### Frontend (React + TypeScript)

1. **Chat Interface** (`ChatInterface.tsx`)
   - Modern chat UI using assistant-ui
   - Markdown rendering
   - Code highlighting
   - Responsive design

2. **Frappe Runtime** (`frappeRuntime.ts`)
   - Adapter for assistant-ui
   - Frappe API integration
   - Streaming support
   - Session management

3. **Classic UI** (`ai_chat.bundle.js`)
   - jQuery-based fallback
   - Frappe dialog integration
   - Toolbar button
   - Basic chat functionality

### DocTypes

1. **AI Chat Settings** (Single)
   - Global configuration
   - Provider settings
   - Feature flags
   - Rate limits
   - MCP configuration

2. **AI Chat Conversation**
   - User conversations
   - Metadata (tokens, count)
   - Status tracking
   - Timestamps

3. **AI Chat Message**
   - Individual messages
   - Role (user/assistant/system)
   - Content
   - Token usage

4. **AI Chat Provider** (Child Table)
   - Provider configuration
   - API credentials
   - Model settings
   - Enable/disable

## Features

### ✅ Implemented

- [x] Multi-provider LLM support (OpenAI, Claude, Gemini, etc.)
- [x] Real-time streaming responses
- [x] Conversation history persistence
- [x] MCP integration for Frappe context
- [x] Rate limiting and security
- [x] Markdown and code highlighting
- [x] React frontend with assistant-ui
- [x] RESTful API
- [x] Configuration UI
- [x] Audit logging
- [x] Token tracking
- [x] Permission management
- [x] Error handling
- [x] Documentation

### 🚧 Planned (Future Releases)

- [ ] Tool calling (function calling)
- [ ] File upload support
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Conversation export/import
- [ ] Analytics dashboard
- [ ] Mobile app
- [ ] RAG (Retrieval Augmented Generation)
- [ ] Fine-tuning support
- [ ] Team collaboration
- [ ] Prompt templates

## Technology Stack

### Backend
- **Framework**: Frappe (Python)
- **LLM Library**: LiteLLM (100+ provider support)
- **HTTP Client**: httpx (async)
- **Validation**: Pydantic
- **Sanitization**: bleach

### Frontend
- **UI Library**: React 18
- **Language**: TypeScript
- **Chat UI**: assistant-ui
- **Markdown**: marked
- **Code Highlighting**: highlight.js
- **Build Tool**: Vite

### Infrastructure
- **Database**: MariaDB (via Frappe)
- **Cache**: Redis (via Frappe)
- **Web Server**: Nginx/Apache (via Frappe)
- **Process Manager**: Supervisor (via Frappe)

## File Structure

```
iVendNext_AI_Chat/
├── ivendnext_ai_chat/           # Main app directory
│   ├── ai_chat/                 # AI Chat module
│   │   ├── doctype/            # DocTypes
│   │   │   ├── ai_chat_settings/
│   │   │   ├── ai_chat_conversation/
│   │   │   ├── ai_chat_message/
│   │   │   └── ai_chat_provider/
│   │   ├── llm_provider.py     # LLM integration
│   │   └── mcp_integration.py  # MCP integration
│   ├── config/                  # App configuration
│   │   ├── desktop.py
│   │   └── docs.py
│   ├── public/                  # Static assets
│   │   ├── css/
│   │   ├── js/
│   │   └── dist/               # Built frontend
│   ├── utils/                   # Utilities
│   │   ├── security.py
│   │   └── rate_limiter.py
│   ├── www/                     # Web pages
│   ├── api.py                   # API endpoints
│   ├── hooks.py                 # Frappe hooks
│   └── __init__.py
├── frontend/                    # React frontend
│   ├── src/
│   │   ├── components/
│   │   │   └── ChatInterface.tsx
│   │   ├── lib/
│   │   │   └── frappeRuntime.ts
│   │   ├── styles/
│   │   └── main.tsx
│   ├── vite.config.ts
│   └── tsconfig.json
├── examples/                    # Code examples
│   ├── basic_chat.py
│   ├── streaming_example.py
│   └── mcp_integration_example.py
├── setup.py                     # Python setup
├── requirements.txt             # Python dependencies
├── package.json                 # Node dependencies
├── README.md                    # Main documentation
├── INSTALLATION.md              # Installation guide
├── API.md                       # API documentation
├── CONTRIBUTING.md              # Contribution guide
├── CHANGELOG.md                 # Version history
└── LICENSE                      # MIT License
```

## Security Features

1. **Input Validation**
   - XSS prevention via bleach
   - SQL injection prevention (Frappe ORM)
   - Length limits
   - Type validation

2. **Rate Limiting**
   - Per-user limits
   - Configurable thresholds
   - Redis-backed tracking
   - Bypass for System Managers

3. **Access Control**
   - Frappe permissions
   - Conversation ownership validation
   - API key encryption
   - Session management

4. **Audit Trail**
   - All interactions logged
   - Configurable log levels
   - Error tracking
   - Token usage monitoring

## Performance

- **Streaming**: Real-time SSE for immediate feedback
- **Caching**: Redis cache for settings and frequent queries
- **Async**: httpx for non-blocking I/O
- **Pagination**: Efficient conversation loading
- **Token Limits**: Configurable to prevent abuse

## Deployment

### Development
```bash
bench get-app https://github.com/yourusername/iVendNext_AI_Chat
bench --site dev.local install-app ivendnext_ai_chat
npm install && npm run build
bench build --app ivendnext_ai_chat
```

### Production
```bash
# Same as development, plus:
bench --site prod.local migrate
bench restart
# Configure reverse proxy (Nginx)
# Set up SSL certificates
# Configure firewall
```

## Configuration

Minimal required configuration:

1. **LLM Provider**: Add at least one provider with API key
2. **Enable**: Turn on AI Chat in settings
3. **System Prompt**: Customize for your use case
4. **Rate Limits**: Set appropriate limits

Optional:
- MCP integration for Frappe context
- Custom providers
- Multiple models
- Advanced features

## Monitoring

Track these metrics:

- **Usage**: Messages per hour/day
- **Tokens**: Token consumption per user/model
- **Errors**: Failed requests
- **Latency**: Response times
- **Costs**: API costs per provider

## Support & Community

- **Issues**: GitHub Issues
- **Discussions**: GitHub Discussions
- **Documentation**: README, INSTALLATION, API docs
- **Examples**: Complete code examples

## License

MIT License - Free for commercial and personal use

## Credits

- **Frappe Framework**: ERPNext team
- **LiteLLM**: BerriAI team
- **assistant-ui**: assistant-ui team
- **MCP**: Frappe Assistant Core by buildswithpaul

## Conclusion

iVendNext AI Chat is a **production-ready**, **extensible**, and **secure** AI chatbot solution for Frappe Framework. It provides enterprise-grade features while remaining simple to configure and use.

Perfect for:
- Customer support automation
- Internal knowledge bases
- ERP assistance
- Business process automation
- Developer tools
