"""
LLM Provider implementation using LiteLLM
Supports 100+ LLM providers with unified interface
"""

import frappe
from typing import Dict, List, Optional, Any, Generator
import json


class LLMProvider:
    """Unified LLM provider interface using LiteLLM"""

    def __init__(self):
        self.settings = frappe.get_cached_doc("AI Chat Settings")
        self._validate_settings()

    def _validate_settings(self):
        """Validate settings before use"""
        if not self.settings.enabled:
            frappe.throw("AI Chat is not enabled")

        if not self.settings.default_provider:
            frappe.throw("No default provider configured")

    def _get_litellm_config(self, provider_name: Optional[str] = None) -> Dict[str, Any]:
        """Get LiteLLM configuration for the provider"""
        provider_name = provider_name or self.settings.default_provider

        # Find provider in settings
        provider = None
        for p in self.settings.providers:
            if p.provider_name == provider_name and p.enabled:
                provider = p
                break

        if not provider:
            frappe.throw(f"Provider {provider_name} not found or disabled")

        # Build model string for LiteLLM
        model_string = self._build_model_string(provider)

        config = {
            "model": model_string,
            "temperature": self.settings.temperature,
            "max_tokens": self.settings.max_tokens,
        }

        # Add API key if available
        if provider.api_key:
            api_key = provider.get_password("api_key")
            if api_key:
                config["api_key"] = api_key

        # Add custom API base if specified
        if provider.api_base_url:
            config["api_base"] = provider.api_base_url

        return config

    def _build_model_string(self, provider) -> str:
        """Build LiteLLM model string based on provider"""
        provider_name = provider.provider_name.lower().replace(" ", "_")
        model_name = provider.model_name

        # LiteLLM model string format: provider/model
        if provider_name == "openai":
            return model_name  # OpenAI is default, no prefix needed
        elif provider_name == "anthropic":
            return f"claude/{model_name}" if not model_name.startswith("claude/") else model_name
        elif provider_name == "google":
            return f"gemini/{model_name}" if not model_name.startswith("gemini/") else model_name
        elif provider_name == "azure_openai":
            return f"azure/{model_name}" if not model_name.startswith("azure/") else model_name
        elif provider_name == "ollama":
            return f"ollama/{model_name}" if not model_name.startswith("ollama/") else model_name
        else:
            # For custom providers, use as-is
            return model_name

    def _build_messages(
        self, user_message: str, conversation_id: Optional[str] = None, system_prompt: Optional[str] = None
    ) -> List[Dict[str, str]]:
        """Build messages array for LLM"""
        messages = []

        # Add system prompt
        system = system_prompt or self.settings.system_prompt
        if system:
            messages.append({"role": "system", "content": system})

        # Add conversation history if enabled and conversation_id provided
        if self.settings.enable_conversation_history and conversation_id:
            history = self._get_conversation_history(conversation_id)
            messages.extend(history)

        # Add current user message
        messages.append({"role": "user", "content": user_message})

        return messages

    def _get_conversation_history(self, conversation_id: str) -> List[Dict[str, str]]:
        """Get conversation history from database"""
        if not frappe.db.exists("AI Chat Conversation", conversation_id):
            return []

        messages = frappe.get_all(
            "AI Chat Message",
            filters={"conversation": conversation_id},
            fields=["role", "content"],
            order_by="creation asc",
            limit=self.settings.max_conversation_length,
        )

        return [{"role": msg.role, "content": msg.content} for msg in messages]

    def generate(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        system_prompt: Optional[str] = None,
        provider_name: Optional[str] = None,
        stream: bool = False,
    ) -> Any:
        """
        Generate response from LLM

        Args:
            message: User message
            conversation_id: Optional conversation ID for history
            system_prompt: Optional custom system prompt
            provider_name: Optional provider override
            stream: Whether to stream response

        Returns:
            Response string or generator for streaming
        """
        try:
            # Lazy import to avoid dependency issues
            import litellm

            # Build configuration
            config = self._get_litellm_config(provider_name)
            messages = self._build_messages(message, conversation_id, system_prompt)

            # Log request if enabled
            if self.settings.enable_logging:
                self._log_request(messages, config)

            # Make LLM call
            if stream and self.settings.enable_streaming:
                return self._stream_response(litellm, config, messages)
            else:
                return self._complete_response(litellm, config, messages)

        except Exception as e:
            frappe.log_error(f"LLM Error: {str(e)}", "AI Chat LLM Error")
            raise

    def _complete_response(self, litellm, config: Dict, messages: List[Dict]) -> Dict[str, Any]:
        """Get complete response from LLM"""
        response = litellm.completion(messages=messages, stream=False, **config)

        result = {
            "content": response.choices[0].message.content,
            "model": response.model,
            "tokens": {
                "prompt": response.usage.prompt_tokens,
                "completion": response.usage.completion_tokens,
                "total": response.usage.total_tokens,
            },
            "finish_reason": response.choices[0].finish_reason,
        }

        # Log response if enabled
        if self.settings.enable_logging:
            self._log_response(result)

        return result

    def _stream_response(self, litellm, config: Dict, messages: List[Dict]) -> Generator:
        """Stream response from LLM"""
        response = litellm.completion(messages=messages, stream=True, **config)

        for chunk in response:
            if chunk.choices[0].delta.content:
                yield {
                    "content": chunk.choices[0].delta.content,
                    "model": chunk.model,
                    "done": False,
                }

        # Final chunk
        yield {"content": "", "done": True}

    def _log_request(self, messages: List[Dict], config: Dict):
        """Log LLM request"""
        frappe.logger().info(f"LLM Request - Model: {config.get('model')}, Messages: {len(messages)}")

    def _log_response(self, result: Dict):
        """Log LLM response"""
        frappe.logger().info(
            f"LLM Response - Model: {result.get('model')}, Tokens: {result.get('tokens', {}).get('total', 0)}"
        )


def get_provider() -> LLMProvider:
    """Get LLM provider instance"""
    return LLMProvider()
