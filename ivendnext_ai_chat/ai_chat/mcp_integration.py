"""
MCP (Model Context Protocol) Integration
Connects with Frappe Assistant Core MCP Server
"""

import frappe
import httpx
from typing import Dict, List, Optional, Any
import json


class MCPClient:
    """Client for MCP server integration"""

    def __init__(self):
        self.settings = frappe.get_cached_doc("AI Chat Settings")
        self.enabled = self.settings.enable_mcp
        self.server_url = self.settings.mcp_server_url
        self.timeout = self.settings.mcp_timeout or 30

        if self.enabled and not self.server_url:
            frappe.throw("MCP is enabled but server URL is not configured")

    def is_enabled(self) -> bool:
        """Check if MCP is enabled"""
        return self.enabled and bool(self.server_url)

    async def get_context(self, query: str, user: Optional[str] = None) -> Dict[str, Any]:
        """
        Get context from MCP server

        Args:
            query: User query
            user: Optional user for permission filtering

        Returns:
            Context dict with relevant information
        """
        if not self.is_enabled():
            return {}

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.server_url}/get-context",
                    json={"query": query, "user": user or frappe.session.user},
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            frappe.log_error(f"MCP Error: {str(e)}", "AI Chat MCP Error")
            return {}

    async def execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute a tool via MCP server

        Args:
            tool_name: Name of tool to execute
            parameters: Tool parameters

        Returns:
            Tool execution result
        """
        if not self.is_enabled():
            frappe.throw("MCP is not enabled")

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.server_url}/execute-tool",
                    json={"tool": tool_name, "parameters": parameters, "user": frappe.session.user},
                )
                response.raise_for_status()
                return response.json()
        except Exception as e:
            frappe.log_error(f"MCP Tool Error: {str(e)}", "AI Chat MCP Tool Error")
            raise

    async def get_available_tools(self) -> List[Dict[str, Any]]:
        """
        Get list of available tools from MCP server

        Returns:
            List of available tools with their schemas
        """
        if not self.is_enabled():
            return []

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.get(
                    f"{self.server_url}/tools", params={"user": frappe.session.user}
                )
                response.raise_for_status()
                return response.json().get("tools", [])
        except Exception as e:
            frappe.log_error(f"MCP Tools List Error: {str(e)}", "AI Chat MCP Error")
            return []

    def sync_get_context(self, query: str, user: Optional[str] = None) -> Dict[str, Any]:
        """Synchronous wrapper for get_context"""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.get_context(query, user))

    def sync_execute_tool(self, tool_name: str, parameters: Dict[str, Any]) -> Dict[str, Any]:
        """Synchronous wrapper for execute_tool"""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.execute_tool(tool_name, parameters))

    def sync_get_available_tools(self) -> List[Dict[str, Any]]:
        """Synchronous wrapper for get_available_tools"""
        import asyncio

        try:
            loop = asyncio.get_event_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)

        return loop.run_until_complete(self.get_available_tools())

    def enhance_prompt(self, user_message: str, system_prompt: str) -> str:
        """
        Enhance system prompt with MCP context

        Args:
            user_message: User's message
            system_prompt: Original system prompt

        Returns:
            Enhanced system prompt with context
        """
        if not self.is_enabled():
            return system_prompt

        try:
            context = self.sync_get_context(user_message)

            if context and context.get("data"):
                context_str = json.dumps(context.get("data"), indent=2)
                enhanced = f"""{system_prompt}

## Frappe Context
You have access to the following context from the Frappe system:

{context_str}

Use this context to provide more accurate and relevant responses.
"""
                return enhanced
        except Exception as e:
            frappe.log_error(f"Error enhancing prompt: {str(e)}", "AI Chat MCP Error")

        return system_prompt


def get_mcp_client() -> MCPClient:
    """Get MCP client instance"""
    return MCPClient()
