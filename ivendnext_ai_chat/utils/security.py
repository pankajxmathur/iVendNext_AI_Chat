"""
Security utilities for AI Chat
"""

import frappe
from frappe import _
import bleach
from typing import Optional


def sanitize_input(text: str) -> str:
    """
    Sanitize user input to prevent XSS and injection attacks

    Args:
        text: Raw user input

    Returns:
        Sanitized text
    """
    if not text:
        return ""

    # Remove any HTML tags and escape special characters
    cleaned = bleach.clean(text, tags=[], strip=True)

    # Limit length to prevent abuse
    max_length = 10000
    if len(cleaned) > max_length:
        frappe.throw(_(f"Message too long. Maximum {max_length} characters allowed."))

    return cleaned


def validate_conversation_access(conversation_id: str, user: str):
    """
    Validate that user has access to conversation

    Args:
        conversation_id: Conversation ID
        user: User email

    Raises:
        PermissionError if user doesn't have access
    """
    if not frappe.db.exists("AI Chat Conversation", conversation_id):
        frappe.throw(_("Conversation not found"))

    conversation = frappe.get_doc("AI Chat Conversation", conversation_id)

    # Check if user owns the conversation or is System Manager
    if conversation.user != user and "System Manager" not in frappe.get_roles(user):
        frappe.throw(_("You don't have permission to access this conversation"))


def validate_api_key(api_key: str) -> bool:
    """
    Validate API key format

    Args:
        api_key: API key to validate

    Returns:
        True if valid
    """
    if not api_key or len(api_key) < 10:
        return False

    # Basic validation - should be alphanumeric with possible hyphens/underscores
    import re

    pattern = r"^[a-zA-Z0-9_\-\.]+$"
    return bool(re.match(pattern, api_key))


def encrypt_api_key(api_key: str) -> str:
    """
    Encrypt API key for storage

    Args:
        api_key: Plain API key

    Returns:
        Encrypted key
    """
    from frappe.utils.password import encrypt

    return encrypt(api_key)


def decrypt_api_key(encrypted_key: str) -> str:
    """
    Decrypt API key

    Args:
        encrypted_key: Encrypted API key

    Returns:
        Plain API key
    """
    from frappe.utils.password import decrypt

    return decrypt(encrypted_key)


def check_permission(doctype: str, name: str, permission_type: str = "read") -> bool:
    """
    Check if user has permission on document

    Args:
        doctype: DocType name
        name: Document name
        permission_type: Permission type (read, write, delete)

    Returns:
        True if user has permission
    """
    return frappe.has_permission(doctype, permission_type, name)


def audit_log(action: str, conversation_id: Optional[str] = None, details: Optional[dict] = None):
    """
    Log user actions for audit trail

    Args:
        action: Action performed
        conversation_id: Optional conversation ID
        details: Optional additional details
    """
    if not frappe.get_cached_doc("AI Chat Settings").enable_logging:
        return

    frappe.logger().info(
        f"AI Chat Audit - User: {frappe.session.user}, Action: {action}, "
        f"Conversation: {conversation_id}, Details: {details}"
    )
