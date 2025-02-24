from game_defs import hangman, inter_story, word_chain, twenty_qs

#give options. system message: "if the user wants to play a game, display these 4 options and ask for the number inputs to pick a specific game: 1 for hangman, 2 for interactive story, 3 for word chain, 4 for 20 questions"

user_input = input("You: ")

if user_input == 1:
    response = hangman()
    print(response)

if user_input == 2:
    response = inter_story()
    print(response)

if user_input == 3:
    response = word_chain()
    print(response)

if user_input == 4:
    response = twenty_qs()
    print(response)