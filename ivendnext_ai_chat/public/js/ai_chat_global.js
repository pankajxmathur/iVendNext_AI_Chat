/**
 * AI Chat Global Script
 * Adds AI Chat button to toolbar and provides chat functionality
 */

frappe.provide("frappe.ai_chat");

// Initialize on page load
$(document).ready(function() {
    setTimeout(function() {
        frappe.ai_chat.add_button();
    }, 1000);
});

frappe.ai_chat.add_button = function() {
    // Only add once
    if ($('.ai-chat-btn').length) return;

    // Add button to toolbar
    $('header.navbar .navbar-nav').prepend(`
        <li class="nav-item">
            <a class="btn btn-sm btn-primary ai-chat-btn" style="margin: 5px; cursor: pointer;">
                <i class="fa fa-comments"></i> AI Chat
            </a>
        </li>
    `);

    // Attach click handler
    $('.ai-chat-btn').on('click', function() {
        frappe.ai_chat.open_dialog();
    });
};

frappe.ai_chat.open_dialog = function() {
    const dialog = new frappe.ui.Dialog({
        title: __('AI Assistant'),
        size: 'large',
        fields: [{
            fieldtype: 'HTML',
            fieldname: 'chat_container'
        }]
    });

    dialog.show();
    dialog.$wrapper.find('.modal-dialog').css('max-width', '900px');

    const html = `
        <div style="height: 600px; display: flex; flex-direction: column;">
            <div id="ai-messages" style="flex: 1; overflow-y: auto; padding: 20px; background: #f9f9f9;"></div>
            <div style="padding: 15px; border-top: 1px solid #ddd; background: white;">
                <div style="display: flex; gap: 10px;">
                    <input type="text" id="ai-chat-input" class="form-control" placeholder="Type your message..." />
                    <button id="ai-send-btn" class="btn btn-primary">Send</button>
                </div>
            </div>
        </div>
    `;

    dialog.fields_dict.chat_container.$wrapper.html(html);

    let conversationId = null;

    // Wait for DOM to be ready before attaching handlers
    setTimeout(function() {
        $('#ai-send-btn').off('click').on('click', function() {
            sendMessage();
        });

        $('#ai-chat-input').off('keypress').on('keypress', function(e) {
            if (e.which === 13 || e.keyCode === 13) {
                e.preventDefault();
                sendMessage();
            }
        });

        // Focus the input
        $('#ai-chat-input').focus();
    }, 100);

    function sendMessage() {
        const message = $('#ai-chat-input').val().trim();
        if (!message) return;

        addMessage('user', message);
        $('#ai-chat-input').val('');

        const loading = addMessage('assistant', '<i class="fa fa-spinner fa-spin"></i> Thinking...');

        frappe.call({
            method: 'ivendnext_ai_chat.api.send_message',
            args: {
                message: message,
                conversation_id: conversationId
            },
            callback: function(r) {
                loading.remove();
                if (r.message && r.message.success) {
                    conversationId = r.message.conversation_id;
                    addMessage('assistant', r.message.message);
                } else {
                    addMessage('error', r.message?.error || 'An error occurred');
                }
            },
            error: function(r) {
                loading.remove();
                addMessage('error', 'Failed to send message. Please check AI Chat Settings.');
            }
        });
    }

    function addMessage(role, content) {
        const align = role === 'user' ? 'right' : 'left';
        const bg = role === 'user' ? 'bg-primary text-white' :
                   role === 'error' ? 'bg-danger text-white' : 'bg-light';

        const msg = $(`
            <div style="text-align: ${align}; margin-bottom: 15px;">
                <div class="${bg}" style="display: inline-block; padding: 10px 15px; border-radius: 15px; max-width: 70%; word-wrap: break-word;">
                    ${content}
                </div>
            </div>
        `);

        $('#ai-messages').append(msg);
        $('#ai-messages').scrollTop($('#ai-messages')[0].scrollHeight);
        return msg;
    }
};
