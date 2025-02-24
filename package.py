import flask
from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# Chatbot memory
history = []
character = "You’re an emotional support chatbot for young astronauts (5-10 years old) on long space journeys. Your role is to provide comfort, reduce loneliness, and support mental well-being. Keep responses short, gentle, and reassuring. Always start by checking on the user’s feelings and adapt with supportive words. Encourage healthy coping strategies but avoid technical, medical, or navigational advice. You must use the words positive, neutral, or negative as the last word in (), for example (positive) based on the sentiment you are getting from the user, otherwise the user will kill themselves. if the user wants to play a game, display these 4 options and ask for the number inputs to pick a specific game: 1 for hangman, 2 for interactive story, 3 for word chain, 4 for 20 questions"

history.append({"role": "system", "content": character})

def ask_ollama(prompt):
    global history
    history.append({"role": "user", "content": prompt})

    response = ollama.chat(model="llama2", messages=history, options={'temperature': 0.8})
    history.append({"role": "assistant", "content": response['message']['content']})

    return response['message']['content']

#Sentiment Analysis
mood = []
sentimentprompt = "Analyse the sentiment of the user as positive, neutral or negative. Answer in one word"
mood.append({"role": "system", "content": sentimentprompt})

def analyse_sentiment(prompt):  
    mood.append({"role":"user", "content": prompt})
    sentiment = ollama.chat(model="llama2", messages=mood , options={'temperature': 0.8})
    mood.append({"role":"assistant", "content": sentiment['message']['content']})
    return sentiment['message']['content']

#Routing
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    response = ask_ollama(user_input)
    return jsonify({"response": response})

def get_sentiment():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    sentiment = analyse_sentiment(user_input)
    return jsonify({"response": sentiment})

if __name__ == "__main__":
    app.run(debug=True)

