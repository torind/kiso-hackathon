$(document).ready(function() {
    
    var datasets = [{
        'id' : 1,
        'name' : 'Sales Demand Forecast.ipynb'
    }]; // To store datasets
    var currentDatasetId = null;
    var rules = []; // To store rules for the current dataset
    var data = {};
    var data_classes = {};
    var data_annotations = {};
    var selectedText = null;
    var displayedRuleId = null;

    // Add chat history array
    let chatHistory = [];

    // Add initial system message
    const initialMessage = "Hi, how can I help you understand this notebook?";
    appendMessage('ai', initialMessage);
    chatHistory.push({ role: 'assistant', content: initialMessage });

    function loadDatasets(datasetId = null) {
        var selector = $('#dataset-selector');
        $.each(datasets, function(index, dataset) {
                        selector.append($('<option>', {
                        value: dataset.id,
                        text: dataset.name
                        }));
                    });
        // For simulation, we'll hardcode some datasets
        // showLoader();
        // $.ajax({
        //     url: '/datasets',
        //     type: 'GET',
        //     success: function(data) {
        //         datasets = data['datasets'];
        //         var selector = $('#dataset-selector');
        //         selector.empty();
        //         $.each(datasets, function(index, dataset) {
        //             selector.append($('<option>', {
        //             value: dataset.id,
        //             text: dataset.name
        //             }));
        //         });

        //         if (Object.keys(datasets).length > 0) {
        //             currentDatasetId = datasetId || Object.keys(datasets)[0];
        //             selector.val(currentDatasetId);
        //             loadRules();
        //             loadDataPreview();
        //         }
        //     },
        //     error: function(response) {
        //         alert("Error loading datasets: " + response.responseText);
        //     },
        //     complete: function() {
        //         clearLoader();
        //     }
        // });
    }

    var dp_toggle = false;
    $(document).on('click', '#data-preview-panel-heading', function() {
        if (dp_toggle) {
            res = $('#data-preview-panel-body').collapse('hide')
            $('#data-preview-panel-heading i').removeClass('fa-chevron-down').addClass('fa-chevron-right');
            dp_toggle = false;  
        }
        else {
            if ($('#data-preview-panel-body').text().trim() === 'Loading...') {
                load_summary();
            }
            res = $('#data-preview-panel-body').collapse('show')
            $('#data-preview-panel-heading i').removeClass('fa-chevron-right').addClass('fa-chevron-down');
            dp_toggle = true;
        }
    });

    let load_summary = function() {
        showLoader();
        $.ajax({
            url: '/api/summary',
            type: 'GET',
            success: function(data) {
                // Render the content as markdown
                $('#data-preview-panel-body').html(marked.parse(data));
            },
            error: function(response) {
                alert("Error loading summary: " + response.responseText);
            },
            complete: function() {
                clearLoader();
            }
        });
    };

    let load_notebook = function() {
        showLoader();
        $.ajax({
            url: '/notebook-content',
            type: 'GET',
            success: function(data) {
                // First render the markdown
                const renderedContent = marked.parse(data);
                $('#notebook-viewer').html(renderedContent);
                
                // Add line numbers to code blocks
                $('pre code').each(function() {
                    const code = $(this);
                    const lines = code.text().split('\n').length;
                    const lineNumbers = $('<div>', {
                        class: 'line-numbers',
                        text: Array.from({length: lines}, (_, i) => i + 1).join('\n')
                    });
                    
                    code.parent().addClass('code-block').prepend(lineNumbers);
                });
            },
            error: function(response) {
                alert("Error loading notebook: " + response.responseText);
            },
            complete: function() {
                clearLoader();
            }
        });
    }

    function showLoader() {
        console.log("Showing loader");
        $('#loader').show();
    }

    function clearLoader() {
        $('#loader').hide();
    }
    
    loadDatasets();
    load_notebook();

    // Add custom context menu
    const contextMenu = $('<div>', {
        class: 'context-menu',
        css: {
            display: 'none',
            position: 'fixed',
            background: 'white',
            border: '1px solid #ccc',
            borderRadius: '4px',
            padding: '5px',
            zIndex: 1000
        }
    }).appendTo('body');

    // Add menu items
    const menuItems = [
        { text: 'Add context', action: 'contextualize' },
        { text: 'Ask about this', action: 'ask' },
        { text: 'Explain this', action: 'explain' },
    ];

    menuItems.forEach(item => {
        contextMenu.append($('<div>', {
            class: 'context-menu-item',
            text: item.text,
            css: {
                padding: '5px 10px',
                cursor: 'pointer',
                hover: 'background-color: #f0f0f0'
            }
        }));
    });

    // Handle text selection in notebook viewer
    $('#notebook-viewer').on('mouseup', function(e) {
        const selection = window.getSelection();
        selectedText = selection.toString().trim();
        
        if (e.button === 2) { // Right click
            e.preventDefault();
            
            // Position the context menu
            contextMenu.css({
                display: 'block',
                left: e.pageX,
                top: e.pageY
            });
        }
    });

    // Handle context menu item clicks
    contextMenu.on('click', '.context-menu-item', function() {
        const action = $(this).text();
        
        // Format the message based on the action
        let message = '';
        switch(action) {
            case 'Ask about this':
                message = `Answer the following question: \n\nAbout this code:\n"${selectedText}"`;
                $('#chat-input').focus();
                $('#chat-input').val(message);
                $('#chat-input').get(0).setSelectionRange(31, 31);
                break;
            case 'Explain this':
                message = `Explain what this does: "${selectedText}"`;
                $('#chat-input').val(message);
                $('#chat-input').focus();
                break;
            case 'Add context':
                // Load existing context and show modal
                showLoader();
                $.ajax({
                    url: '/api/get_context',
                    type: 'GET',
                    success: function(response) {
                        $('#contextText').val(response);
                        $('#contextModal').modal('show');
                    },
                    error: function(response) {
                        alert("Error loading context: " + response.responseText);
                    },
                    complete: function() {
                        clearLoader();
                    }
                });
                break;
        }
        
        // Hide the context menu
        contextMenu.hide();
    });

    // Handle context modal close
    $('#contextModal').on('hidden.bs.modal', function () {
        const context = $('#contextText').val();
        if (context) {
            showLoader();
            $.ajax({
                url: '/api/update_context',
                type: 'POST',
                contentType: 'application/json',
                data: JSON.stringify({ context: context }),
                success: function(response) {
                    appendMessage('ai', 'Context has been updated successfully.');
                },
                error: function(response) {
                    appendMessage('error', 'Error saving context: ' + response.responseText);
                },
                complete: function() {
                    clearLoader();
                }
            });
        }
    });

    // Hide context menu when clicking outside
    $(document).on('click', function(e) {
        if (!$(e.target).closest('.context-menu').length) {
            contextMenu.hide();
        }
    });

    // Prevent default context menu
    $('#notebook-viewer').on('contextmenu', function(e) {
        e.preventDefault();
    });

    // Handle chat message sending
    $('#send-message').on('click', function() {
        const message = $('#chat-input').val().trim();
        if (!message) return;

        // Show user message in chat
        appendMessage('user', message);
        
        // Add user message to history
        chatHistory.push({ role: 'user', content: message });
        
        // Clear input
        $('#chat-input').val('');

        // Show loader
        showLoader();

        // Send message to backend with chat history
        $.ajax({
            url: '/api/question_creator_context',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ 
                message: message,
                history: chatHistory
            }),
            success: function(response) {
                // Show AI response in chat
                appendMessage('ai', response);
                
                // Add AI response to history
                chatHistory.push({ role: 'assistant', content: response });
            },
            error: function(response) {
                appendMessage('error', 'Sorry, there was an error processing your message.');
            },
            complete: function() {
                clearLoader();
            }
        });
    });

    // Handle enter key in chat input
    $('#chat-input').on('keypress', function(e) {
        if (e.which === 13 && !e.shiftKey) {
            e.preventDefault();
            $('#send-message').click();
        }
    });

    // Helper function to append messages to chat
    function appendMessage(type, message) {
        const chatMessages = $('#chat-messages');
        const messageDiv = $('<div>', {
            class: `chat-message ${type}-message mb-3`,
            css: {
                padding: '10px',
                borderRadius: '8px',
                maxWidth: '80%',
                whiteSpace: 'pre-wrap'
            }
        });

        if (type === 'user') {
            messageDiv.css({
                backgroundColor: '#007bff',
                color: 'white',
                marginLeft: 'auto'
            });
        } else if (type === 'ai') {
            messageDiv.css({
                backgroundColor: '#f8f9fa',
                color: '#212529',
                marginRight: 'auto'
            });
        } else {
            messageDiv.css({
                backgroundColor: '#dc3545',
                color: 'white',
                marginRight: 'auto'
            });
        }

        // Replace newlines with <br> tags and set as HTML
        messageDiv.html(message.replace(/\n/g, '<br>'));
        chatMessages.append(messageDiv);
        chatMessages.scrollTop(chatMessages[0].scrollHeight);
    }
});
