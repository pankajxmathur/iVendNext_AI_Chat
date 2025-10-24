import frappe
from frappe.model.document import Document


class AIChatMessage(Document):
    def after_insert(self):
        """Update conversation after message insert"""
        if self.conversation:
            conv = frappe.get_doc("AI Chat Conversation", self.conversation)
            conv.last_message_at = self.creation
            conv.save(ignore_permissions=True)
