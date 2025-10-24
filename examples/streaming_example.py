"""
Streaming Example
Demonstrates how to use streaming responses
"""

import frappe
import json


def streaming_example():
    """Example of streaming response"""

    # Note: This example shows the concept
    # In practice, streaming is used via SSE in frontend

    from ivendnext_ai_chat.ai_chat.llm_provider import get_provider

    provider = get_provider()

    print("Streaming response:")
    print("-" * 50)

    # Stream response
    stream = provider.generate(
        message="Write a short poem about programming",
        stream=True
    )

    full_response = ""
    for chunk in stream:
        if chunk.get("done"):
            print(f"\n\n[Done - Model: {chunk.get('model')}]")
        else:
            content = chunk.get("content", "")
            print(content, end="", flush=True)
            full_response += content

    print("\n" + "-" * 50)
    return full_response


def sse_streaming_example():
    """
    Example of using Server-Sent Events for streaming
    This would be used in frontend JavaScript
    """

    javascript_code = """
    // Frontend JavaScript example

    async function streamChat(message) {
        const response = await fetch('/api/method/ivendnext_ai_chat.api.stream_message', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-Frappe-CSRF-Token': frappe.csrf_token
            },
            body: JSON.stringify({ message: message })
        });

        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        let conversationId = null;
        let fullResponse = '';

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const chunk = decoder.decode(value, { stream: true });
            const lines = chunk.split('\\n');

            for (const line of lines) {
                if (line.startsWith('data: ')) {
                    const data = JSON.parse(line.slice(6));

                    if (data.type === 'start') {
                        conversationId = data.conversation_id;
                        console.log('Conversation ID:', conversationId);
                    } else if (data.type === 'content') {
                        fullResponse += data.content;
                        console.log(data.content); // Display chunk
                    } else if (data.type === 'done') {
                        console.log('Streaming complete');
                        console.log('Model:', data.model);
                    } else if (data.type === 'error') {
                        console.error('Error:', data.error);
                    }
                }
            }
        }

        return { conversationId, response: fullResponse };
    }

    // Usage
    streamChat('Tell me about Frappe Framework').then(result => {
        console.log('Full response:', result.response);
        console.log('Conversation ID:', result.conversationId);
    });
    """

    print("Frontend JavaScript example:")
    print(javascript_code)


if __name__ == "__main__":
    streaming_example()
    print("\n" * 2)
    sse_streaming_example()
