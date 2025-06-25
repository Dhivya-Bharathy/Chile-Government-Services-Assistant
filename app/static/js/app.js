document.addEventListener('DOMContentLoaded', function() {
    console.log("DOM fully loaded and parsed. Initializing chat app.");
    const sendBtn = document.getElementById('send-btn');
    const userInput = document.getElementById('user-input');
    const chatWindow = document.getElementById('chat-window');
    const loadingIndicator = document.getElementById('loading-indicator');

    // Variable para controlar si la síntesis de voz está activa
    let speechSynthesis = window.speechSynthesis;
    let currentUtterance = null;

    // Ajustar altura del textarea dinámicamente
    userInput.addEventListener('input', function () {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    function appendMessage(sender, text, isHtml = false) {
        const msgArticle = document.createElement('article');
        msgArticle.classList.add('chat-message', sender);
        console.log(`Adding message from ${sender}:`, isHtml ? "(HTML)" : text);
        
        const contentDiv = document.createElement('div');
        contentDiv.classList.add('message');

        if (sender === 'bot' && isHtml) {
            contentDiv.innerHTML = text; // HTML sanitizado para mitigar XSS
        } else {
            contentDiv.textContent = text;
        }
        
        msgArticle.appendChild(contentDiv);

        // Añadir botón de audio solo para mensajes del bot
        if (sender === 'bot') {
            const audioButton = document.createElement('button');
            audioButton.classList.add('audio-button');
            audioButton.setAttribute('aria-label', 'Play message aloud');
            audioButton.innerHTML = `
                <svg class="speaker-icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"></polygon>
                    <path class="sound-waves" d="M19.07 4.93a10 10 0 0 1 0 14.14M15.54 8.46a5 5 0 0 1 0 7.07"></path>
                </svg>
            `;
            
            // Obtener el texto plano del mensaje para la síntesis de voz
            const plainText = contentDiv.textContent || contentDiv.innerText;
            
            audioButton.addEventListener('click', function() {
                toggleSpeech(plainText, audioButton);
            });
            
            msgArticle.appendChild(audioButton);
        }

        chatWindow.appendChild(msgArticle);
        chatWindow.scrollTop = chatWindow.scrollHeight; // Mantener el scroll abajo
    }

    function toggleSpeech(text, button) {
        if (speechSynthesis.speaking) {
            speechSynthesis.cancel();
            console.log("Speech synthesis stopped.");
            if (button.classList.contains('speaking')) {
                button.classList.remove('speaking');
                return;
            }
            document.querySelectorAll('.audio-button.speaking').forEach(btn => {
                btn.classList.remove('speaking');
            });
        }
        console.log("Starting speech synthesis for text:", text.substring(0, 50) + "...");
        currentUtterance = new SpeechSynthesisUtterance(text);
        currentUtterance.lang = 'en-US'; // English
        currentUtterance.rate = 1.0;
        currentUtterance.pitch = 1.2;
        button.classList.add('speaking');
        currentUtterance.onend = function() {
            button.classList.remove('speaking');
            console.log("Speech synthesis finished.");
        };
        currentUtterance.onerror = function(event) {
            button.classList.remove('speaking');
            console.error('Speech synthesis error:', event.error);
        };
        speechSynthesis.speak(currentUtterance);
    }

    function showLoading(isLoading) {
        if (isLoading) {
            loadingIndicator.style.display = 'block';
            sendBtn.disabled = true;
            userInput.disabled = true;
            console.log("Showing loading indicator.");
        } else {
            loadingIndicator.style.display = 'none';
            sendBtn.disabled = false;
            userInput.disabled = false;
            userInput.focus();
            console.log("Hiding loading indicator.");
        }
    }

    async function handleSendMessage() {
        const text = userInput.value.trim();
        if (!text) return;
        console.log("Sending user message:", text);
        appendMessage('user', text);
        userInput.value = '';
        userInput.style.height = 'auto';
        showLoading(true);
        try {
            const res = await fetch('/api/chat', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({message: text})
            });
            if (!res.ok) {
                let errorMsg = `Server error: ${res.status}`;
                try {
                    const errorData = await res.json();
                    errorMsg = errorData.error || errorMsg;
                } catch (e) { /* Do nothing if error body is not JSON */ }
                throw new Error(errorMsg);
            }
            const data = await res.json();
            if (data.error) {
                appendMessage('bot', `Error: ${data.error}`);
                console.error("Error received from backend:", data.error);
            } else {
                const htmlResponse = marked.parse(data.response);
                const safeHtml = DOMPurify.sanitize(htmlResponse);
                appendMessage('bot', safeHtml, true);
                console.log("Bot response (HTML) received and added to chat.");
            }
        } catch (e) {
            appendMessage('bot', `Communication error: ${e.message}`);
            console.error("Communication error in handleSendMessage:", e);
        } finally {
            showLoading(false);
        }
    }

    sendBtn.addEventListener('click', handleSendMessage);

    userInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    });

    userInput.focus(); // Enfocar el input al cargar la página

    // Añadir funcionalidad al botón de audio del mensaje inicial
    const initialAudioButton = document.querySelector('.chat-message.bot .audio-button');
    if (initialAudioButton) {
        const initialMessageElement = document.querySelector('.chat-message.bot .message');
        if (initialMessageElement) {
            const initialMessage = initialMessageElement.textContent || initialMessageElement.innerText;
            initialAudioButton.addEventListener('click', function() {
                toggleSpeech(initialMessage, initialAudioButton);
                console.log("Playing initial bot message.");
            });
        }
    }
}); 