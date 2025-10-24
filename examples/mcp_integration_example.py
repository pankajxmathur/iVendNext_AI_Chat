"""
MCP Integration Example
Demonstrates how to use MCP (Model Context Protocol) features
"""

import frappe
import json


def get_mcp_tools_example():
    """Get available MCP tools"""

    response = frappe.call('ivendnext_ai_chat.api.get_mcp_tools')

    print("Available MCP Tools:")
    print("-" * 50)

    for tool in response.get('tools', []):
        print(f"\nTool: {tool['name']}")
        print(f"Description: {tool['description']}")
        print(f"Parameters: {json.dumps(tool.get('parameters', {}), indent=2)}")


def execute_mcp_tool_example():
    """Execute an MCP tool"""

    # Example: Get a Frappe document
    result = frappe.call(
        'ivendnext_ai_chat.api.execute_mcp_tool',
        tool_name='get_document',
        parameters={
            'doctype': 'Customer',
            'name': 'CUST-0001'
        }
    )

    if result['success']:
        print("Tool execution result:")
        print(json.dumps(result['result'], indent=2))
    else:
        print(f"Error: {result['error']}")


def chat_with_mcp_context_example():
    """Chat with MCP context enhancement"""

    # When MCP is enabled, the system automatically
    # enhances prompts with Frappe context

    response = frappe.call(
        'ivendnext_ai_chat.api.send_message',
        message="What are my open sales orders?"
    )

    # The AI will have context about your sales orders
    # thanks to MCP integration
    print(f"Response: {response['message']}")


def direct_mcp_usage_example():
    """Use MCP client directly"""

    from ivendnext_ai_chat.ai_chat.mcp_integration import get_mcp_client

    mcp = get_mcp_client()

    if not mcp.is_enabled():
        print("MCP is not enabled in settings")
        return

    # Get context for a query
    context = mcp.sync_get_context("sales orders")
    print("\nMCP Context:")
    print(json.dumps(context, indent=2))

    # Get available tools
    tools = mcp.sync_get_available_tools()
    print(f"\n{len(tools)} tools available")

    # Execute a tool
    if tools:
        result = mcp.sync_execute_tool(
            tools[0]['name'],
            tools[0].get('example_parameters', {})
        )
        print("\nTool result:")
        print(json.dumps(result, indent=2))


def enhanced_prompt_example():
    """Example of how MCP enhances prompts"""

    from ivendnext_ai_chat.ai_chat.mcp_integration import get_mcp_client

    mcp = get_mcp_client()

    if not mcp.is_enabled():
        print("MCP is not enabled")
        return

    system_prompt = "You are a helpful assistant."
    user_message = "What customers do I have?"

    # Enhance prompt with MCP context
    enhanced = mcp.enhance_prompt(user_message, system_prompt)

    print("Original prompt:")
    print(system_prompt)
    print("\nEnhanced prompt:")
    print(enhanced)


if __name__ == "__main__":
    print("MCP Integration Examples")
    print("=" * 50)

    get_mcp_tools_example()
    print("\n" * 2)

    chat_with_mcp_context_example()
    print("\n" * 2)

    direct_mcp_usage_example()
    print("\n" * 2)

    enhanced_prompt_example()
