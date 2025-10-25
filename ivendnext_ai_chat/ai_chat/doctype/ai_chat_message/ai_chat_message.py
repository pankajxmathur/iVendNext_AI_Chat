import frappe
from frappe.model.document import Document


class AIChatMessage(Document):
    def after_insert(self):
        """Update conversation after message insert"""
        if self.conversation:
            # Use direct database update to avoid version conflicts
            frappe.db.set_value(
                "AI Chat Conversation",
                self.conversation,
                "last_message_at",
                self.creation,
                update_modified=False,
            )
