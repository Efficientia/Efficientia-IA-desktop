async function enviar() {
    const input = document.getElementById('userInput');
    const chat = document.getElementById('chat');
    const loader = document.getElementById('loader');
    const message = input.value;
    
    if (!message.trim()) return;

    // Adiciona mensagem do usuário
    chat.innerHTML += `<div class="message user">${message}</div>`;
    input.value = '';
    
    // Mostra loader
    loader.style.display = 'flex';
    chat.scrollTop = chat.scrollHeight;

    try {
        const response = await fetch('/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
                user_id: "user123", 
                session_id: "session123", 
                message: message 
            })
        });

        if (!response.ok) {
            throw new Error('Erro ao comunicar com o servidor');
        }

        const data = await response.json();
        
        // Renderiza Markdown usando marked
        const botResponseHTML = marked.parse(data.response.resposta);
        
        chat.innerHTML += `<div class="message bot">${botResponseHTML}</div>`;
        chat.scrollTop = chat.scrollHeight;
    } catch (error) {
        chat.innerHTML += `<div class="message bot" style="color:red;">Erro: ${error.message}</div>`;
    } finally {
        loader.style.display = 'none';
    }
}

// Permitir envio com a tecla "Enter"
document.getElementById('userInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        enviar();
    }
});
