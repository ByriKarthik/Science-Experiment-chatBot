const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatLog = document.getElementById('chat-log');
const sendBtn = document.getElementById('send-btn');
const typingIndicator = document.getElementById('typing-indicator');
const suggestionButtons = document.querySelectorAll('.suggestion-btn');

// Typing effect function
function typeWriterEffect(targetElement, text, delay = 20) {
  let i = 0;
  const interval = setInterval(() => {
    targetElement.innerHTML += text.charAt(i);
    i++;
    if (i === text.length) clearInterval(interval);
    chatLog.scrollTop = chatLog.scrollHeight;
  }, delay);
}

// Function to add messages to chat
function addMessage(content, isUser, typewriter = false) {
  const messageDiv = document.createElement('div');
  messageDiv.className = `chat-message ${isUser ? 'user' : 'bot'}`;

  const bubbleDiv = document.createElement('div');
  bubbleDiv.className = 'chat-bubble';

  if (isUser) {
    bubbleDiv.innerHTML = `<strong>You:</strong> ${content}`;
  } else {
    const label = document.createElement('strong');
    label.textContent = 'Bot: ';
    bubbleDiv.appendChild(label);

    const span = document.createElement('span');
    bubbleDiv.appendChild(span);

    if (typewriter) {
      typeWriterEffect(span, content);
    } else {
      span.innerHTML = content;
    }
  }

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

// Send message to backend
async function sendMessage(message) {
  addMessage(message, true); // Show user message
  userInput.value = '';
  userInput.disabled = true;
  sendBtn.disabled = true;
  showTyping();

  try {
    const apiUrl = window.location.port === "5500"
      ? "http://localhost:5000/chat"
      : "/chat";

    const res = await fetch(apiUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });

    if (!res.ok) throw new Error('Network response was not ok');

    const data = await res.json();
    const cleanHTML = DOMPurify.sanitize(marked.parse(data.response || 'Sorry, I couldn’t process that.'));

    // Strip HTML tags for typing effect (optional enhancement)
    const tempDiv = document.createElement('div');
    tempDiv.innerHTML = cleanHTML;
    const plainText = tempDiv.textContent || tempDiv.innerText || '';

    addMessage(plainText, false, true); // Show bot message with typing effect

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

// Form submission handler
chatForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const message = userInput.value.trim();
  if (!message) return;
  await sendMessage(message);
});

// Suggestion button clicks
suggestionButtons.forEach(btn => {
  btn.addEventListener('click', () => {
    const prompt = btn.dataset.prompt;
    userInput.value = prompt;
    sendMessage(prompt);
  });
});

// Auto-focus on input
userInput.focus();
