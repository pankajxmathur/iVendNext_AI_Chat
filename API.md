# API Documentation

Complete API reference for iVendNext AI Chat.

## Authentication

All API endpoints require authentication. Use Frappe's session-based authentication or API key/secret.

```javascript
// Using session (in Frappe frontend)
frappe.call({
  method: 'ivendnext_ai_chat.api.send_message',
  args: { message: 'Hello' },
  callback: (r) => console.log(r.message)
});

// Using API key (external)
fetch('/api/method/ivendnext_ai_chat.api.send_message', {
  method: 'POST',
  headers: {
    'Authorization': 'token api_key:api_secret',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ message: 'Hello' })
});
```

## Endpoints

### Send Message

Send a message and get AI response.

**Endpoint:** `ivendnext_ai_chat.api.send_message`

**Method:** POST

**Parameters:**
- `message` (string, required): User message
- `conversation_id` (string, optional): Conversation ID to continue
- `system_prompt` (string, optional): Custom system prompt
- `provider` (string, optional): Provider override

**Response:**
```json
{
  "success": true,
  "conversation_id": "CONV-0001",
  "message": "AI response here",
  "model": "gpt-4",
  "tokens": {
    "prompt": 50,
    "completion": 100,
    "total": 150
  }
}
```

**Example:**
```python
import frappe

response = frappe.call(
    'ivendnext_ai_chat.api.send_message',
    message="What is Frappe Framework?",
    conversation_id="CONV-0001"
)
```

---

### Stream Message

Stream AI response in real-time (Server-Sent Events).

**Endpoint:** `ivendnext_ai_chat.api.stream_message`

**Method:** POST

**Parameters:**
- `message` (string, required): User message
- `conversation_id` (string, optional): Conversation ID
- `system_prompt` (string, optional): Custom system prompt
- `provider` (string, optional): Provider override

**Response:** SSE stream

```
data: {"conversation_id": "CONV-0001", "type": "start"}

data: {"type": "content", "content": "Hello"}

data: {"type": "content", "content": " there"}

data: {"type": "done", "model": "gpt-4"}
```

**Example:**
```javascript
const eventSource = new EventSource('/api/method/ivendnext_ai_chat.api.stream_message?message=Hello');

eventSource.onmessage = (event) => {
  const data = JSON.parse(event.data);
  if (data.type === 'content') {
    console.log(data.content);
  }
};
```

---

### Create Conversation

Create a new conversation.

**Endpoint:** `ivendnext_ai_chat.api.create_conversation`

**Method:** POST

**Parameters:**
- `title` (string, optional): Conversation title

**Response:**
```json
{
  "name": "CONV-0001",
  "title": "New Conversation",
  "user": "user@example.com",
  "status": "Active"
}
```

---

### Get Conversation

Get conversation with all messages.

**Endpoint:** `ivendnext_ai_chat.api.get_conversation`

**Method:** GET/POST

**Parameters:**
- `conversation_id` (string, required): Conversation ID

**Response:**
```json
{
  "conversation": {
    "name": "CONV-0001",
    "title": "My Chat",
    "message_count": 10,
    "total_tokens": 1500
  },
  "messages": [
    {
      "role": "user",
      "content": "Hello",
      "creation": "2025-01-24 10:00:00"
    },
    {
      "role": "assistant",
      "content": "Hi there!",
      "creation": "2025-01-24 10:00:05"
    }
  ]
}
```

---

### Get Conversations

Get user's conversations with pagination.

**Endpoint:** `ivendnext_ai_chat.api.get_conversations`

**Method:** GET/POST

**Parameters:**
- `limit` (int, optional): Number of conversations (default: 20)
- `offset` (int, optional): Offset for pagination (default: 0)

**Response:**
```json
{
  "conversations": [
    {
      "name": "CONV-0001",
      "title": "My Chat",
      "message_count": 10,
      "total_tokens": 1500,
      "created_at": "2025-01-24 10:00:00",
      "last_message_at": "2025-01-24 10:30:00"
    }
  ]
}
```

---

### Delete Conversation

Delete (archive) a conversation.

**Endpoint:** `ivendnext_ai_chat.api.delete_conversation`

**Method:** POST

**Parameters:**
- `conversation_id` (string, required): Conversation ID

**Response:**
```json
{
  "success": true
}
```

---

### Get MCP Tools

Get available MCP tools.

**Endpoint:** `ivendnext_ai_chat.api.get_mcp_tools`

**Method:** GET/POST

**Response:**
```json
{
  "tools": [
    {
      "name": "get_document",
      "description": "Fetch a Frappe document",
      "parameters": {
        "doctype": "string",
        "name": "string"
      }
    }
  ]
}
```

---

### Execute MCP Tool

Execute an MCP tool.

**Endpoint:** `ivendnext_ai_chat.api.execute_mcp_tool`

**Method:** POST

**Parameters:**
- `tool_name` (string, required): Tool name
- `parameters` (dict, required): Tool parameters

**Response:**
```json
{
  "success": true,
  "result": {
    "data": "Tool result here"
  }
}
```

---

### Get Settings

Get public AI Chat settings.

**Endpoint:** `ivendnext_ai_chat.api.get_settings`

**Method:** GET/POST

**Response:**
```json
{
  "enabled": true,
  "enable_streaming": true,
  "enable_markdown": true,
  "enable_code_highlighting": true,
  "enable_mcp": false,
  "default_provider": "OpenAI",
  "max_tokens": 2000
}
```

---

## Python API

Use the Python API directly in your Frappe apps:

```python
import frappe
from ivendnext_ai_chat.ai_chat.llm_provider import get_provider
from ivendnext_ai_chat.ai_chat.mcp_integration import get_mcp_client

# Send a message
provider = get_provider()
response = provider.generate(
    message="What is Frappe?",
    conversation_id="CONV-0001",
    stream=False
)

print(response['content'])

# Use MCP
mcp = get_mcp_client()
if mcp.is_enabled():
    context = mcp.sync_get_context("sales orders")
    print(context)

# Execute MCP tool
result = mcp.sync_execute_tool(
    "get_document",
    {"doctype": "Customer", "name": "CUST-0001"}
)
print(result)
```

---

## Rate Limiting

API endpoints are rate limited based on settings:

**Headers:**
```
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

**Error Response:**
```json
{
  "success": false,
  "error": "Rate limit exceeded. Maximum 100 requests per hour allowed."
}
```

---

## Error Handling

All endpoints return consistent error responses:

```json
{
  "success": false,
  "error": "Error message here"
}
```

**Common Errors:**
- `401`: Unauthorized (not logged in)
- `403`: Forbidden (no permission)
- `429`: Rate limit exceeded
- `500`: Internal server error

---

## Webhooks (Future)

Webhook support is planned for future releases to notify external systems of events.

---

## SDK (Future)

Official SDKs for popular languages are planned:
- Python SDK
- JavaScript/TypeScript SDK
- PHP SDK

---

## Examples

See the `examples/` directory for complete examples:
- Basic chat integration
- Streaming responses
- MCP tool usage
- Custom providers
- Conversation management
