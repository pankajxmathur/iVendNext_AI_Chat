import frappe
from frappe.model.document import Document


class AIChatConversation(Document):
    def before_insert(self):
        """Set defaults before insert"""
        if not self.title:
            self.title = f"Conversation {frappe.utils.now()}"

    def get_messages(self):
        """Get all messages in this conversation"""
        return frappe.get_all(
            "AI Chat Message",
            filters={"conversation": self.name},
            fields=["name", "role", "content", "creation", "tokens_used"],
            order_by="creation asc",
        )

    def add_message(self, role, content, tokens_used=0):
        """Add a message to this conversation"""
        message = frappe.get_doc(
            {
                "doctype": "AI Chat Message",
                "conversation": self.name,
                "role": role,
                "content": content,
                "tokens_used": tokens_used,
            }
        )
        message.insert(ignore_permissions=True)

        # Update conversation stats using database update to avoid version conflicts
        frappe.db.set_value(
            "AI Chat Conversation",
            self.name,
            {
                "message_count": (self.message_count or 0) + 1,
                "total_tokens": (self.total_tokens or 0) + tokens_used,
                "last_message_at": frappe.utils.now(),
            },
            update_modified=True,
        )

        # Reload to get updated values
        self.reload()

        return message
