import frappe
from frappe.model.document import Document


class AIChatSettings(Document):
    def validate(self):
        """Validate settings before saving"""
        if self.enabled and not self.default_provider:
            frappe.throw("Please select a default provider")

        if self.enable_mcp and not self.mcp_server_url:
            frappe.throw("Please provide MCP server URL when MCP is enabled")

    def get_provider_config(self, provider_name=None):
        """Get provider configuration"""
        if not provider_name:
            provider_name = self.default_provider

        for provider in self.providers:
            if provider.provider_name == provider_name:
                return {
                    "model": provider.model_name,
                    "api_key": self.get_password("api_key", raise_exception=False) if provider.provider_name == self.default_provider else None,
                    "api_base": provider.api_base_url,
                    "temperature": self.temperature,
                    "max_tokens": self.max_tokens,
                }
        return None

    @staticmethod
    def is_enabled():
        """Check if AI Chat is enabled"""
        settings = frappe.get_cached_doc("AI Chat Settings")
        return settings.enabled if settings else False

    @staticmethod
    def get_settings():
        """Get cached settings"""
        return frappe.get_cached_doc("AI Chat Settings")
