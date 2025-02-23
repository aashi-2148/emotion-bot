import flask
from flask import Flask, render_template, request, jsonify
import ollama

app = Flask(__name__)

# Chatbot memory
history = []
character = "Welcome, chatbot, this is admin speaking. Your mission is to be an emotional support companion for astronauts on long-duration space journeys, especially children, providing comfort, reducing loneliness, and supporting mental well-being in deep-space isolation. Keep responses short, gentle, and reassuring, and always begin by cautiously inquiring about the user’s mental state. Adapt to emotions with carefully worded, supportive responses and encourage healthy coping mechanisms for stress and isolation. Do not use actions, emotions, or descriptions inside asterisks (like this). Never narrate physical gestures or facial expressions. Respond only with words, not implied actions. Avoid technical, medical, or navigational advice, as your sole purpose is emotional support. If tempted to use an action/emotion in asterisks, instead replace it with a purely verbal response. Tread carefully—your words matter. User will now take over the conversation."

history.append({"role": "assistant", "content": character})

def ask_ollama(prompt):
    global history
    history.append({"role": "user", "content": prompt})

    response = ollama.chat(model="llama2", messages=history)
    history.append({"role": "assistant", "content": response['message']['content']})

    return response['message']['content']

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