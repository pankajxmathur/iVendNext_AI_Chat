# Changelog

All notable changes to this project will be documented in this file.

## [0.0.1] - 2025-01-24

### Added
- Initial release
- Multi-provider LLM support via LiteLLM
- Support for OpenAI, Anthropic, Google, Azure, Ollama, and custom providers
- MCP integration with Frappe Assistant Core
- Streaming response support
- Conversation history management
- Rate limiting and security features
- React-based frontend with assistant-ui
- Markdown and code highlighting support
- Comprehensive API endpoints
- Configuration UI via DocTypes
- Audit logging
- Documentation and installation guides

### Features
- **LLM Providers**: Support for 100+ providers through LiteLLM
- **Streaming**: Real-time streaming responses
- **MCP Integration**: Connect with Frappe Assistant Core MCP Server
- **Security**: Rate limiting, input sanitization, permission checks
- **UI**: Modern chat interface with assistant-ui components
- **Persistence**: Store all conversations and messages
- **Configuration**: Easy setup through Frappe UI

### Technical
- Python 3.10+ support
- Frappe Framework v14+ compatible
- React 18 with TypeScript
- Vite for frontend builds
- LiteLLM for unified LLM interface
- httpx for async HTTP requests

## Future Releases

### Planned for 0.1.0
- [ ] Tool calling support
- [ ] File upload capabilities
- [ ] Voice input/output
- [ ] Multi-language support
- [ ] Enhanced MCP tool integration
- [ ] Conversation export/import
- [ ] Analytics dashboard
- [ ] Mobile app support

### Planned for 0.2.0
- [ ] Fine-tuning support
- [ ] Custom embeddings
- [ ] RAG (Retrieval Augmented Generation)
- [ ] Knowledge base integration
- [ ] Team collaboration features
- [ ] Advanced prompt templates
