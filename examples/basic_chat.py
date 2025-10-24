"""
Basic Chat Example
Demonstrates how to use the AI Chat API
"""

import frappe


def basic_chat_example():
    """Simple chat example"""

    # Send a single message
    response = frappe.call(
        'ivendnext_ai_chat.api.send_message',
        message="What is Frappe Framework?"
    )

    print(f"Response: {response['message']}")
    print(f"Conversation ID: {response['conversation_id']}")
    print(f"Tokens used: {response['tokens']['total']}")


def conversation_example():
    """Multi-turn conversation example"""

    # Create a conversation
    conversation = frappe.call(
        'ivendnext_ai_chat.api.create_conversation',
        title="Learning about Frappe"
    )

    conversation_id = conversation.name

    # Ask multiple questions
    questions = [
        "What is Frappe Framework?",
        "How do I create a DocType?",
        "Can you explain hooks.py?"
    ]

    for question in questions:
        response = frappe.call(
            'ivendnext_ai_chat.api.send_message',
            message=question,
            conversation_id=conversation_id
        )

        print(f"\nQ: {question}")
        print(f"A: {response['message']}")


def custom_prompt_example():
    """Example with custom system prompt"""

    system_prompt = """You are a helpful assistant specializing in ERP systems.
    You provide detailed, technical answers about business processes."""

    response = frappe.call(
        'ivendnext_ai_chat.api.send_message',
        message="How should I manage inventory?",
        system_prompt=system_prompt
    )

    print(f"Response: {response['message']}")


def provider_override_example():
    """Example with specific provider"""

    # Use Claude instead of default provider
    response = frappe.call(
        'ivendnext_ai_chat.api.send_message',
        message="Explain Docker in simple terms",
        provider="Anthropic"
    )

    print(f"Response: {response['message']}")
    print(f"Model used: {response['model']}")


# Run examples
if __name__ == "__main__":
    basic_chat_example()
    conversation_example()
    custom_prompt_example()
    provider_override_example()
