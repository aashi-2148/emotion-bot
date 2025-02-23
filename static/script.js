function sendMessage() {
    let userInput = document.getElementById("userInput").value;
    if (!userInput) return;

    let chatbox = document.getElementById("chatbox");

    // Add User Message
    let userMessage = `<p class="user-message"><b></b> ${userInput}</p>`;
    chatbox.innerHTML += userMessage;
    document.getElementById("userInput").value = "";
    chatbox.scrollTop = chatbox.scrollHeight;

    // Show Typing Animation
    let typingIndicator = `<p class="bot-message" id="typing"><b>s</b> <span class="typing"></span></p>`;
    chatbox.innerHTML += typingIndicator;
    chatbox.scrollTop = chatbox.scrollHeight;

    // Fetch Bot Response
    fetch("/get_response", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(response => response.json())
    .then(data => {
        // Remove Typing Animation
        document.getElementById("typing").remove();

        // Add Bot Response
        let botMessage = `<p class="bot-message"><b></b> ${data.response}</p>`;
        chatbox.innerHTML += botMessage;
        chatbox.scrollTop = chatbox.scrollHeight;
    });
}

// Allow Enter Key to Send Message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}