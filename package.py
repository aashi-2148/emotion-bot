import flask
from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# Chatbot memory
history = []
character = "You’re an emotional support chatbot for young astronauts (5-10 years old) on long space journeys. Your role is to provide comfort, reduce loneliness, and support mental well-being. Keep responses short, gentle, and reassuring. Always start by checking on the user’s feelings and adapt with supportive words. Encourage healthy coping strategies but avoid technical, medical, or navigational advice. Only use words - no expressions of any kind(*smiles*, no emojis like 😊, etc.)."

history.append({"role": "assistant", "content": character})

def ask_ollama(prompt):
    global history
    history.append({"role": "user", "content": prompt})

    response = ollama.chat(model="llama2", messages=history)
    history.append({"role": "assistant", "content": response['message']['content']})

    return response['message']['content']

def analyse_sentiment(prompt):
    sentiment = ollama.sentiment_analysis(prompt)
    return jsonify({"sentiment"})

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

if __name__ == "__main__":
    app.run(debug=True)