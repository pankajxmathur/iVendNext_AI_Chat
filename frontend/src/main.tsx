/**
 * Main entry point for AI Chat React application
 * Uses assistant-ui for the chat interface
 */

import React from 'react';
import ReactDOM from 'react-dom/client';
import { AssistantRuntimeProvider } from '@assistant-ui/react';
import { ChatInterface } from './components/ChatInterface';
import { createFrappeRuntime } from './lib/frappeRuntime';
import './styles/index.css';

// Create the runtime that connects to Frappe backend
const runtime = createFrappeRuntime();

const App = () => {
  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <ChatInterface />
    </AssistantRuntimeProvider>
  );
};

// Mount to DOM
const rootElement = document.getElementById('ai-chat-root');
if (rootElement) {
  ReactDOM.createRoot(rootElement).render(
    <React.StrictMode>
      <App />
    </React.StrictMode>
  );
}

// Export for use in Frappe dialogs
export { App };
