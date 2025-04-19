const chatForm = document.getElementById('chat-form');
    const userInput = document.getElementById('user-input');
    const chatLog = document.getElementById('chat-log');
    const sendBtn = document.getElementById('send-btn');
    const typingIndicator = document.getElementById('typing-indicator');
    const suggestionButtons = document.querySelectorAll('.suggestion-btn');

    function addMessage(content, isUser) {
      const messageDiv = document.createElement('div');
      messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;
      const bubbleDiv = document.createElement('div');
      bubbleDiv.className = 'chat-bubble';
      bubbleDiv.innerHTML = `<strong>${isUser ? 'You' : 'Bot'}:</strong> ${content}`;
      messageDiv.appendChild(bubbleDiv);
      chatLog.appendChild(messageDiv);
      chatLog.scrollTop = chatLog.scrollHeight;
    }

    function showTyping() {
      typingIndicator.style.display = 'block';
      chatLog.scrollTop = chatLog.scrollHeight;
    }

    function hideTyping() {
      typingIndicator.style.display = 'none';
    }

    async function sendMessage(message) {
      addMessage(message, true);
      userInput.value = '';
      userInput.disabled = true;
      sendBtn.disabled = true;
      showTyping();

      try {
        const res = await fetch('http://localhost:5000/chat', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ message })
        });

        if (!res.ok) throw new Error('Network response was not ok');

        const data = await res.json();
        const rendered = DOMPurify.sanitize(marked.parse(data.response || 'Sorry, I couldn’t process that.'));
        addMessage(rendered, false);
      } catch (error) {
        addMessage('Oops! Something went wrong. Please try again.', false);
        console.error(error);
      } finally {
        hideTyping();
        userInput.disabled = false;
        sendBtn.disabled = false;
        userInput.focus();
      }
    }

    chatForm.addEventListener('submit', async (e) => {
      e.preventDefault();
      const message = userInput.value.trim();
      if (!message) return;
      await sendMessage(message);
    });

    // Handle suggestion buttons
    suggestionButtons.forEach(btn => {
      btn.addEventListener('click', () => {
        const prompt = btn.dataset.prompt;
        userInput.value = prompt;
        sendMessage(prompt);
      });
    });

    // Auto-focus input on load
    userInput.focus();