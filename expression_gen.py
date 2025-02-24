import nltk
from nltk.sentiment import SentimentIntensityAnalyzer
import re
from nltk import pos_tag, word_tokenize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet

# Download VADER model
nltk.download('vader_lexicon')
nltk.download('averaged_perceptron_tagger_eng')
nltk.download('wordnet')
nltk.download('punkt_tab')

# Initialize analyzer and lemmatizer
sia = SentimentIntensityAnalyzer()
lemmatizer = WordNetLemmatizer()

# Sample text
text = "I'm so happy about this! *smiling brightly*"

action_emotion_map = {
    'affirm': ['nod', 'agree', 'consent', 'acknowledge'],
    'happy': ['smile', 'laugh', 'grin', 'excited', 'wave'],
    'neutral': ['shrug', 'ponder', 'consider', 'sigh'],
    'sad': ['frown', 'cry', 'weep', 'sob'],
    'angry': ['clench', 'shout', 'yell', 'scowl'],
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

def analyse_sentiment(text):
    scores = sia.polarity_scores(text)
    return (scores)

def map_scores(scores):
    if scores["compound"] >= 0.05:
        return 'positive'
    elif scores["compound"] <= -0.05:
        return 'negative'
    else:
        return 'neutral'
    
emoji_map = {
    'affirm': '👍',
    'happy': '😄',
    'neutral': '😐',
    'sad': '😢',
    'angry': '😠',
}

def find_emoji(simplified_actions, connotation):
    for action in simplified_actions:
        words = action.split()  #split phrases into individual words
        for word in words:
            for emotion, keywords in action_emotion_map.items():
                if word in keywords:
                    return emoji_map.get(emotion, '😶')

    #fallback to sentiment-based emoji if not found
    return emoji_map.get(connotation, '😐')

actions = create_actions(text)
simplified_actions = [simplify_action(action) for action in actions]
sentiment_scores = analyse_sentiment(text)
connotation = map_scores(sentiment_scores)
emoji = find_emoji(simplified_actions, connotation)

#generate final output
print(f"Actions: {simplified_actions}, Sentiment: {connotation}, Emoji: {emoji}")
