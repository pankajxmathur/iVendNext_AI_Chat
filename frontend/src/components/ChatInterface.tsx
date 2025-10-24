/**
 * Main Chat Interface Component
 * Uses assistant-ui components for the chat UI
 */

import React from 'react';
import {
  Thread,
  Composer,
  useThreadRuntime,
  useAssistantRuntime,
} from '@assistant-ui/react';
import { MarkdownText } from '@assistant-ui/react-markdown';

export const ChatInterface: React.FC = () => {
  return (
    <div className="ai-chat-interface">
      <ChatHeader />
      <div className="chat-thread-container">
        <Thread
          welcome={{
            message: "Hello! I'm your AI assistant. How can I help you today?",
          }}
          components={{
            Text: MarkdownText,
          }}
        />
      </div>
      <ChatComposer />
    </div>
  );
};

const ChatHeader: React.FC = () => {
  const runtime = useAssistantRuntime();

  const handleNewChat = () => {
    runtime.switchToNewThread();
  };

  return (
    <div className="chat-header">
      <div className="chat-title">
        <h3>AI Assistant</h3>
      </div>
      <div className="chat-actions">
        <button onClick={handleNewChat} className="btn-new-chat">
          New Chat
        </button>
      </div>
    </div>
  );
};

const ChatComposer: React.FC = () => {
  return (
    <div className="chat-composer-container">
      <Composer
        placeholder="Type your message..."
        className="chat-composer"
      />
    </div>
  );
};
