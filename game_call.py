from game_defs import hangman, inter_story, word_chain, twenty_qs

user_input = int(input("Enter a number: "))

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
