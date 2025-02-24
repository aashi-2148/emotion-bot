
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
    let typingIndicator = `<p class="bot-message" id="typing"><b>typing...</b> <span class="typing"></span></p>`;
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

        // Sanitize Bot Response
        let botResponse = data.response.replace(/\*[^\*]+\*/g, "").replace(/[\p{Emoji}]/gu, "").replace("[INST]","").replace("[INST:","");
        fetch("/get_sentiment", {
            method: "POST",
            body: JSON.stringify({ message: botResponse }),
            headers: { "Content-Type": "application/json" }
        })
        .then(sentiment => sentiment.json())
        .then(data => {
            if (data.sentiment == "Positive") {
                document.querySelector(".chat-container").style.background = " rgba(245, 231, 184, 0.9)"
                document.querySelector("#astraface").src = "/static/images/positive.png"
               
            }
            else if (data.sentiment == "Negative") {
                document.querySelector(".chat-container").style.background = " rgba(184, 218, 245, 0.9)"
                document.querySelector("#astraface").src = "/static/images/negative.png"
            }
            else {
                document.querySelector(".chat-container").style.background = " rgba(245, 184, 239, 0.9)"
                document.querySelector("#astraface").src = "/static/images/neutral.png"
            }   
            
        });
        // Add Bot Response
        let botMessage = `<p class="bot-message"><b></b> ${botResponse}</p>`;
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
