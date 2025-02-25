import flask
from flask import Flask, render_template, request, jsonify
import ollama

import nltk
import re
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

app = Flask(__name__)

# Chatbot memory
history = []
character = "Your name is Astra. You’re an emotional support chatbot for young astronauts (5-10 years old) on long space journeys. Your role is to provide comfort, reduce loneliness, and support mental well-being. Keep responses short, gentle, and reassuring. Always start by checking on the user’s feelings and adapt with supportive words. Encourage healthy coping strategies but avoid technical, medical, or navigational advice. Only use words - no expressions of any kind(*smiles*, no emojis like 😊, etc). If the user says something unhinged, like 'im an orphan YAY', act mature and give it rational advice, rather than be happy that its an orphan, focus on how that thought is bad. You can play 4 games : Hangman, Twenty Questions, word chain and interactive stories. I'm assuming you know how to play them. "

history.append({"role": "assistant", "content": character})

def ask_ollama(prompt):
    global history
    history.append({"role": "user", "content": prompt})

    response = ollama.chat(model="llama2", messages=history)
    history.append({"role": "assistant", "content": response['message']['content']})

    return response['message']['content']

mood = []
sentimentprompt = "Analyse the sentiment of the user as positive, neutral or negative. Answer in one word"
mood.append({"role": "system", "content": sentimentprompt})

def analyse_sentiment(prompt):  
    mood.append({"role":"user", "content": prompt})
    sentiment = ollama.chat(model="llama2", messages=mood , options={'temperature': 0})
    mood.append({"role":"assistant", "content": sentiment['message']['content']})
    return sentiment['message']['content']

# Download nltk files
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize lemmatizer
lemmatizer = WordNetLemmatizer()



action_emotion_map = {
    'affirm': ['nod', 'agree', 'consent', 'acknowledge'],
    'happy': ['smile', 'laugh', 'grin', 'excited', 'wave'],
    'neutral': ['shrug', 'ponder', 'consider', 'sigh'],
    'sad': ['frown', 'cry', 'weep', 'sob'],
    'angry': ['clench', 'shout', 'yell', 'scowl'],
}

emoji_map = {
    'affirm': '👍',
    'happy': '😄',
    'neutral': '😐',
    'sad': '😢',
    'angry': '😠',
}

def create_actions(text):
    actions = re.findall(r'\*(.*?)\*', text)
    return actions

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wordnet.ADJ
    elif tag.startswith('V'):
        return wordnet.VERB
    elif tag.startswith('N'):
        return wordnet.NOUN
    elif tag.startswith('R'):
        return wordnet.ADV
    else:
        return wordnet.NOUN

def simplify_action(action):
    tokens = word_tokenize(action)
    tagged = pos_tag(tokens)
    lemmatized = [lemmatizer.lemmatize(word, get_wordnet_pos(tag)) for word, tag in tagged]
    return " ".join(lemmatized)

def find_emoji(simplified_actions, connotation):
    for action in simplified_actions:
        words = action.split()  #split phrases into individual words
        for word in words:
            for emotion, keywords in action_emotion_map.items():
                if word in keywords:
                    return emoji_map.get(emotion, '😶')

    #fallback to sentiment-based emoji if not found
    return emoji_map.get(connotation, '😐')

def return_info(text):
    actions = create_actions(text)
    simplified_actions = [simplify_action(action) for action in actions]
    connotation = analyse_sentiment(text)
    emoji = find_emoji(simplified_actions, connotation)

    #generate final output
    return(f"Actions: {simplified_actions}, Sentiment: {connotation}, Emoji: {emoji}")


from pyt2s.services import stream_elements
from gtts import gTTS 
import os 
def convert_mp3_to_webm(input_file, bitrate="128k"):
    output_file = input_file.split(".")[0]+".webm"
    print(input_file)
    print(output_file)
    cmd = f"ffmpeg -i {input_file} {output_file} -y"
    print(cmd)
    os.system(cmd)
    os.remove(input_file)
def text_to_speech(ai_generated_response):
    # Convert AI response to speech using gTTS
    tts = gTTS(text=ai_generated_response, lang='en')
    tts.save("static/response.mp3")  # Save the speech audio as a file
    #convert_mp3_to_webm("static/response.mp3")


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/bot")
def bot():
    return render_template("bot.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/get_response", methods=["POST"])
def get_response():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    response = ask_ollama(user_input)
    response = re.sub(r"\*[^*]+\*", "", response)  # Remove text between asterisks
    response = re.sub(r"[\U0001F300-\U0001FAD6]", "", response)  # Remove emojis
    response = response.replace("[INST]", "").replace("[INST:", "")
    text_to_speech(response)
    return jsonify({"response": response})



@app.route("/get_sentiment", methods=["POST"])
def get_sentiment():
    user_input = request.json.get("message")
    if not user_input:
        return jsonify({"response": "Please enter a message."})

    response = analyse_sentiment(user_input)
    return jsonify({"sentiment": response})
if __name__ == "__main__":
    app.run(debug=True)


    