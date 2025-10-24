"""
API endpoints for AI Chat
All endpoints are whitelisted for authenticated users
"""

import frappe
from frappe import _
from typing import Optional, Dict, Any
import json
from ivendnext_ai_chat.ai_chat.llm_provider import get_provider
from ivendnext_ai_chat.ai_chat.mcp_integration import get_mcp_client
from ivendnext_ai_chat.utils.rate_limiter import check_rate_limit
from ivendnext_ai_chat.utils.security import sanitize_input, validate_conversation_access


@frappe.whitelist()
def send_message(
    message: str,
    conversation_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    provider: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Send a message and get AI response

    Args:
        message: User message
        conversation_id: Optional conversation ID
        system_prompt: Optional custom system prompt
        provider: Optional provider override

    Returns:
        Response dict with message and metadata
    """
    try:
        # Validate input
        message = sanitize_input(message)
        if not message:
            frappe.throw(_("Message cannot be empty"))

        # Check rate limit
        check_rate_limit(frappe.session.user)

        # Create or get conversation
        if conversation_id:
            validate_conversation_access(conversation_id, frappe.session.user)
            conversation = frappe.get_doc("AI Chat Conversation", conversation_id)
        else:
            conversation = create_conversation()
            conversation_id = conversation.name

        # Save user message
        conversation.add_message(role="user", content=message)

        # Get MCP client and enhance prompt if enabled
        mcp_client = get_mcp_client()
        if mcp_client.is_enabled() and system_prompt:
            system_prompt = mcp_client.enhance_prompt(message, system_prompt)

        # Get LLM provider and generate response
        llm_provider = get_provider()
        response = llm_provider.generate(
            message=message,
            conversation_id=conversation_id,
            system_prompt=system_prompt,
            provider_name=provider,
            stream=False,
        )

        # Save assistant message
        conversation.add_message(
            role="assistant", content=response["content"], tokens_used=response["tokens"]["total"]
        )

        return {
            "success": True,
            "conversation_id": conversation_id,
            "message": response["content"],
            "model": response["model"],
            "tokens": response["tokens"],
        }

    except Exception as e:
        frappe.log_error(f"Chat Error: {str(e)}", "AI Chat Error")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def stream_message(
    message: str,
    conversation_id: Optional[str] = None,
    system_prompt: Optional[str] = None,
    provider: Optional[str] = None,
):
    """
    Stream message response (Server-Sent Events)

    Args:
        message: User message
        conversation_id: Optional conversation ID
        system_prompt: Optional custom system prompt
        provider: Optional provider override

    Yields:
        SSE formatted chunks
    """
    try:
        # Validate input
        message = sanitize_input(message)
        if not message:
            yield f"data: {json.dumps({'error': 'Message cannot be empty'})}\n\n"
            return

        # Check rate limit
        check_rate_limit(frappe.session.user)

        # Create or get conversation
        if conversation_id:
            validate_conversation_access(conversation_id, frappe.session.user)
            conversation = frappe.get_doc("AI Chat Conversation", conversation_id)
        else:
            conversation = create_conversation()
            conversation_id = conversation.name

        # Save user message
        conversation.add_message(role="user", content=message)

        # Send conversation ID first
        yield f"data: {json.dumps({'conversation_id': conversation_id, 'type': 'start'})}\n\n"

        # Get MCP client and enhance prompt if enabled
        mcp_client = get_mcp_client()
        if mcp_client.is_enabled() and system_prompt:
            system_prompt = mcp_client.enhance_prompt(message, system_prompt)

        # Get LLM provider and stream response
        llm_provider = get_provider()
        stream = llm_provider.generate(
            message=message,
            conversation_id=conversation_id,
            system_prompt=system_prompt,
            provider_name=provider,
            stream=True,
        )

        # Collect full response for saving
        full_response = ""

        # Stream chunks
        for chunk in stream:
            if chunk.get("done"):
                # Save complete message
                conversation.add_message(role="assistant", content=full_response)
                yield f"data: {json.dumps({'type': 'done', 'model': chunk.get('model')})}\n\n"
            else:
                content = chunk.get("content", "")
                full_response += content
                yield f"data: {json.dumps({'type': 'content', 'content': content})}\n\n"

    except Exception as e:
        frappe.log_error(f"Stream Error: {str(e)}", "AI Chat Stream Error")
        yield f"data: {json.dumps({'type': 'error', 'error': str(e)})}\n\n"


@frappe.whitelist()
def create_conversation(title: Optional[str] = None) -> Dict[str, Any]:
    """
    Create a new conversation

    Args:
        title: Optional conversation title

    Returns:
        Conversation document
    """
    conversation = frappe.get_doc(
        {
            "doctype": "AI Chat Conversation",
            "title": title or f"New Conversation",
            "user": frappe.session.user,
            "status": "Active",
        }
    )
    conversation.insert(ignore_permissions=True)
    return conversation


@frappe.whitelist()
def get_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Get conversation with messages

    Args:
        conversation_id: Conversation ID

    Returns:
        Conversation with messages
    """
    validate_conversation_access(conversation_id, frappe.session.user)

    conversation = frappe.get_doc("AI Chat Conversation", conversation_id)
    messages = conversation.get_messages()

    return {"conversation": conversation.as_dict(), "messages": messages}


@frappe.whitelist()
def get_conversations(limit: int = 20, offset: int = 0) -> Dict[str, Any]:
    """
    Get user's conversations

    Args:
        limit: Number of conversations to fetch
        offset: Offset for pagination

    Returns:
        List of conversations
    """
    conversations = frappe.get_all(
        "AI Chat Conversation",
        filters={"user": frappe.session.user, "status": "Active"},
        fields=["name", "title", "message_count", "total_tokens", "created_at", "last_message_at"],
        order_by="last_message_at desc",
        limit=limit,
        start=offset,
    )

    return {"conversations": conversations}


@frappe.whitelist()
def delete_conversation(conversation_id: str) -> Dict[str, Any]:
    """
    Delete (archive) a conversation

    Args:
        conversation_id: Conversation ID

    Returns:
        Success response
    """
    validate_conversation_access(conversation_id, frappe.session.user)

    conversation = frappe.get_doc("AI Chat Conversation", conversation_id)
    conversation.status = "Deleted"
    conversation.save(ignore_permissions=True)

    return {"success": True}


@frappe.whitelist()
def get_mcp_tools() -> Dict[str, Any]:
    """
    Get available MCP tools

    Returns:
        List of available tools
    """
    try:
        mcp_client = get_mcp_client()
        if not mcp_client.is_enabled():
            return {"tools": []}

        tools = mcp_client.sync_get_available_tools()
        return {"tools": tools}
    except Exception as e:
        frappe.log_error(f"MCP Tools Error: {str(e)}", "AI Chat MCP Error")
        return {"tools": [], "error": str(e)}


@frappe.whitelist()
def execute_mcp_tool(tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
    """
    Execute an MCP tool

    Args:
        tool_name: Tool name
        parameters: Tool parameters

    Returns:
        Tool execution result
    """
    try:
        mcp_client = get_mcp_client()
        if not mcp_client.is_enabled():
            frappe.throw("MCP is not enabled")

        result = mcp_client.sync_execute_tool(tool_name, parameters)
        return {"success": True, "result": result}
    except Exception as e:
        frappe.log_error(f"MCP Tool Execution Error: {str(e)}", "AI Chat MCP Error")
        return {"success": False, "error": str(e)}


@frappe.whitelist()
def get_settings() -> Dict[str, Any]:
    """
    Get public AI Chat settings

    Returns:
        Public settings
    """
    settings = frappe.get_cached_doc("AI Chat Settings")

    return {
        "enabled": settings.enabled,
        "enable_streaming": settings.enable_streaming,
        "enable_markdown": settings.enable_markdown,
        "enable_code_highlighting": settings.enable_code_highlighting,
        "enable_mcp": settings.enable_mcp,
        "default_provider": settings.default_provider,
        "max_tokens": settings.max_tokens,
    }
