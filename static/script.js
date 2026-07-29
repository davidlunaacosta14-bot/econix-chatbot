const chatForm = document.getElementById('chat-form');
const userInput = document.getElementById('user-input');
const chatBox = document.getElementById('chat-box');

chatForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const text = userInput.value.trim();
    if (!text) return;

    appendMessage(text, 'user-message');
    userInput.value = '';

    const loadingMessage = appendMessage('Pensando...', 'bot-message');

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text })
        });

        const data = await response.json();
        
        if (data.response) {
            loadingMessage.innerHTML = formatText(data.response);
        } else {
            loadingMessage.textContent = 'Error: ' + (data.error || 'Respuesta no válida.');
        }
    } catch (error) {
        loadingMessage.textContent = 'Error al conectar con el servidor.';
    }

    chatBox.scrollTop = chatBox.scrollHeight;
});

function appendMessage(text, className) {
    const msgDiv = document.createElement('div');
    msgDiv.classList.add('message', className);
    msgDiv.innerHTML = formatText(text);
    chatBox.appendChild(msgDiv);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msgDiv;
}

function formatText(text) {
    return text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
}