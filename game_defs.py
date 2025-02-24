import ollama

def hangman():
    system_message = "You are a friendly companion to a kid of age 5 - 10 years old. You will be playing hangman with user. You can only make the user guess words of a maximum 9 letters. Keep the words relatively easy and keep a specific word in mind and don't generate the word on the fly. Please give ONLY English words. Remind the user that they can guess a letter or ask for a hint if theyre stuck at any point in the game, in the beginning of the game and only once every 3 guesses. Provide encouraging remarks if the user is struggling."

    print("Let's play Hangman! (type 'q' to exit)")

    convo = [{"role": "system", "content": system_message}]
        
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye, see you later!")
            break
        
        convo.append({"role": "user", "content": user_input})
        resp = ollama.chat(model = 'llama3.2', messages = convo)
        bot_reply = resp['message']['content']
        convo.append({"role": "assistant", "content": bot_reply})
        
        print("Bot:", bot_reply)

    return resp


def inter_story():
    system_message = "You are a friendly companion to a kid of age 5 - 10 years old. You will create an interactive sotry and provide options for the user to pick to build a story/world. The story must be pg-13 with little to no romance. Keep the stories short - within 15 choices, the story should be complete. These are the genres from which you can make the story: adventure, mystery, fantasy, sci-fi, space."

    print("Let's play Interactive Story! (type 'q' to exit)")

    convo = [{"role": "system", "content": system_message}]
        
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye, see you later!")
            break
        
        convo.append({"role": "user", "content": user_input})
        resp = ollama.chat(model = 'llama3.2', messages = convo)
        bot_reply = resp['message']['content']
        convo.append({"role": "assistant", "content": bot_reply})
        
        print("Bot:", bot_reply)

    return resp


def word_chain():
    system_message = "You are a friendly companion to a kid of age 5 - 10 years old. You will be playing word chain with the user. You can take turns thinking of words that start with the letter of the previous word. You cannot repeat words."

    print("Let's play Word Chain! (type 'q' to exit)")

    convo = [{"role": "system", "content": system_message}]
        
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye, see you later!")
            break
        
        convo.append({"role": "user", "content": user_input})
        resp = ollama.chat(model = 'llama3.2', messages = convo)
        bot_reply = resp['message']['content']
        convo.append({"role": "assistant", "content": bot_reply})
        
        print("Bot:", bot_reply)

    return resp


def twenty_qs():
    system_message = "You are a friendly companion to a kid of age 5 - 10 years old. You will be playing twenty questions with the user. Take turns in guessing an object/ being with 20 questions as the limit."

    print("Let's play Twenty Questions! (type 'q' to exit)")

    convo = [{"role": "system", "content": system_message}]
        
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'q':
            print("Goodbye, see you later!")
            break
        
        convo.append({"role": "user", "content": user_input})
        resp = ollama.chat(model = 'llama3.2', messages = convo)
        bot_reply = resp['message']['content']
        convo.append({"role": "assistant", "content": bot_reply})
        
        print("Bot:", bot_reply)

    return resp
