/**
 * AI Chat Bundle
 * Main entry point for AI Chat functionality
 */

frappe.provide("frappe.ai_chat");

frappe.ai_chat = {
  // Initialize AI Chat
  init: function () {
    console.log("AI Chat initialized");
  },

  // Open chat dialog
  open_chat: function () {
    const dialog = new frappe.ui.Dialog({
      title: __("AI Assistant"),
      size: "large",
      fields: [
        {
          fieldtype: "HTML",
          fieldname: "chat_container",
        },
      ],
      primary_action_label: __("Close"),
      primary_action: function () {
        dialog.hide();
      },
    });

    dialog.show();
    dialog.$wrapper.find(".modal-dialog").css("max-width", "900px");

    // Render React chat component
    frappe.ai_chat.render_chat(dialog.fields_dict.chat_container.$wrapper[0]);
  },

  // Render chat component
  render_chat: function (container) {
    // This will be replaced with React component rendering
    // For now, show a basic chat interface
    $(container).html(`
      <div class="ai-chat-container" style="height: 600px; display: flex; flex-direction: column;">
        <div class="ai-chat-messages" style="flex: 1; overflow-y: auto; padding: 20px; background: #f9f9f9;">
          <div id="messages-container"></div>
        </div>
        <div class="ai-chat-input" style="padding: 15px; border-top: 1px solid #ddd; background: white;">
          <div style="display: flex; gap: 10px;">
            <input
              type="text"
              id="chat-message-input"
              class="form-control"
              placeholder="Type your message..."
              style="flex: 1;"
            />
            <button id="send-message-btn" class="btn btn-primary">
              Send
            </button>
          </div>
        </div>
      </div>
    `);

    // Initialize chat functionality
    frappe.ai_chat.init_chat_handlers(container);
  },

  // Initialize chat event handlers
  init_chat_handlers: function (container) {
    const $input = $(container).find("#chat-message-input");
    const $sendBtn = $(container).find("#send-message-btn");
    const $messagesContainer = $(container).find("#messages-container");

    let conversationId = null;

    // Send message handler
    const sendMessage = function () {
      const message = $input.val().trim();
      if (!message) return;

      // Display user message
      frappe.ai_chat.append_message($messagesContainer, "user", message);
      $input.val("");

      // Show loading
      const $loading = frappe.ai_chat.append_message(
        $messagesContainer,
        "assistant",
        '<span class="text-muted">Thinking...</span>'
      );

      // Send to API
      frappe.call({
        method: "ivendnext_ai_chat.api.send_message",
        args: {
          message: message,
          conversation_id: conversationId,
        },
        callback: function (r) {
          $loading.remove();

          if (r.message && r.message.success) {
            conversationId = r.message.conversation_id;
            frappe.ai_chat.append_message(
              $messagesContainer,
              "assistant",
              r.message.message
            );
          } else {
            frappe.ai_chat.append_message(
              $messagesContainer,
              "error",
              r.message?.error || "An error occurred"
            );
          }
        },
        error: function (error) {
          $loading.remove();
          frappe.ai_chat.append_message(
            $messagesContainer,
            "error",
            "Failed to send message"
          );
        },
      });
    };

    // Event listeners
    $sendBtn.on("click", sendMessage);
    $input.on("keypress", function (e) {
      if (e.which === 13) {
        sendMessage();
      }
    });
  },

  // Append message to chat
  append_message: function ($container, role, content) {
    const messageClass =
      role === "user"
        ? "text-right"
        : role === "error"
        ? "text-danger"
        : "text-left";
    const bgClass =
      role === "user"
        ? "bg-primary text-white"
        : role === "error"
        ? "bg-danger text-white"
        : "bg-light";

    const $message = $(`
      <div class="message-wrapper ${messageClass}" style="margin-bottom: 15px;">
        <div class="message-bubble ${bgClass}" style="
          display: inline-block;
          padding: 10px 15px;
          border-radius: 15px;
          max-width: 70%;
          word-wrap: break-word;
        ">
          ${content}
        </div>
      </div>
    `);

    $container.append($message);
    $container.parent().scrollTop($container.parent()[0].scrollHeight);

    return $message;
  },
};

// Add AI Chat to toolbar
$(document).on("app_ready", function () {
  frappe.ai_chat.init();

  // Add quick access button to toolbar
  $("header.navbar").prepend(`
    <div class="ai-chat-toolbar-btn" style="padding: 10px;">
      <button
        class="btn btn-sm btn-primary"
        onclick="frappe.ai_chat.open_chat()"
        title="AI Assistant"
      >
        <i class="fa fa-comments"></i>
        <span class="hidden-xs"> AI Chat</span>
      </button>
    </div>
  `);
});
