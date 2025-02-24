function toggleTheme() {
    const root = document.documentElement; 
    const palettes = {
        positive: {
            '--primary-color': '#4CAF50', // Green
            '--secondary-color': '#81C784',
            '--background-color': '#E8F5E9'
        },
        neutral: {
            '--primary-color': '#9E9E9E', // Grey
            '--secondary-color': '#BDBDBD',
            '--background-color': '#F5F5F5'
        },
        negative: {
            '--primary-color': '#F44336', // Red
            '--secondary-color': '#E57373',
            '--background-color': '#FFEBEE'
        }
    };
}


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
        let botResponse = data.response.replace(/\*[^\*]+\*/g, "").replace(/[\p{Emoji}]/gu, "");

        // Add Bot Response
        let botMessage = `<p class="bot-message"><b></b> ${botResponse}</p>`;
        chatbox.innerHTML += botMessage;
        chatbox.scrollTop = chatbox.scrollHeight;
    });
    fetch("/get_sentiment", {
        method: "POST",
        body: JSON.stringify({ message: userInput }),
        headers: { "Content-Type": "application/json" }
    })
    .then(sentiment => sentiment.json)
    .then(data => {
        if (data.sentiment == "Positive") {
            root.style.setproperty(palettes[positive]);
        }
        else if (data.sentiment == "Negative") {
            root.style.setproperty(palettes[neutral]);
        }
        else if (data.sentiment == "Neutral") {
            root.style.setproperty(palettes[negative]);
        }
        else {
            console.log("Error: Sentiment not found");
        }
    });
}

// Allow Enter Key to Send Message
function handleKeyPress(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
}
