'''
[CS2] Wordle- Guess a five-letter secret word in at most six attempts.
'''
import random
# To install colorama, run the following command in your VS Code terminal:
# py -m pip install colorama
#from colorama import Fore, Back, Style, init
#init(autoreset=True) #Ends color formatting after each print statement
from wordle_wordlist import get_word_list

def get_feedback(guess: str, secret_word: str) -> str:
    '''Generates a feedback string based on comparing a 5-letter guess with the secret word. 
       The feedback string uses the following schema: 
        - Correct letter, correct spot: uppercase letter ('A'-'Z')
        - Correct letter, wrong spot: lowercase letter ('a'-'z')
        - Letter not in the word: '-'

       For example:
        - get_feedback("lever", "EATEN") --> "-e-E-"
        - get_feedback("LEVER", "LOWER") --> "L--ER"
        - get_feedback("MOMMY", "MADAM") --> "M-m--"
        - get_feedback("ARGUE", "MOTTO") --> "-----"

        Args:
            guess (str): The guessed word
            secret_word (str): The secret word
        Returns:
            str: Feedback string, based on comparing guess with the secret word
    '''
    #edge cases
    guessUpper = guess.upper()
    guessList = list(guessUpper)
    secretList = list(secret_word)
    feedBack = []

    if len(guess)!=5 or guessUpper not in get_word_list():
        return 'This is an invalid word. Guess again!'
    else:
        for i in range(len(guessList)):
            if guessList[i] == secretList[i]:
                secretList[i] = '*'
                feedBack.append(guessList[i])
            else:
                feedBack.append("-")

        for i in range(len(guessList)):
            if feedBack[i] == "-":
                if guessList[i] in secretList:
                    if secretList[secretList.index(guessList[i])] == guessList[secretList.index(guessList[i])]:
                        feedBack[i] = "-"
                    else:
                        feedBack[i] = guessList[i].lower()
                        secretList[secretList.index(guessList[i])] = "*" 
                else:
                    feedBack[i] = "-"

    return ''.join(feedBack)

word_list_global = set(get_word_list().copy())
invalid_indexes = {'A':set(), 'B':set(), 'C':set(), 'D':set(), 'E':set(), 'F':set(), 'G':set(), 'H':set(), 'I':set(), 
                   'J':set(), 'K':set(), 'L':set(), 'M':set(), 'N':set(), 'O':set(), 'P':set(), 'Q':set(), 'R':set(), 
                   'S':set(), 'T':set(), 'U':set(), 'V':set(), 'W':set(), 'X':set(), 'Y':set(), 'Z':set()}
invalid_index_copy = invalid_indexes.copy()
scrabble_dict = {'A': 9, 'B': 2, 'C': 2, 'D': 4, 'E': 12, 'F': 2,
    'G': 3, 'H': 2, 'I': 9, 'J': 1, 'K': 1, 'L': 4, 'M': 2, 'N': 6,
    'O': 8, 'P': 2, 'Q': 1, 'R': 6, 'S': 4, 'T': 6, 'U': 4, 'V': 2,
    'W': 2, 'X': 1, 'Y': 2, 'Z': 1 }
confirmed_list = ['-','-','-','-','-']
def get_AI_guess(word_list: list[str], guesses: list[str], feedback: list[str]) -> str:
    '''Analyzes feedback from previous guesses (if any) to make a new guess
        Args:
            word_list (list): A list of potential Wordle words
            guesses (list): A list of string guesses, could be empty
            feedback (list): A list of feedback strings, could be empty
        Returns:
         str: a valid guess that is exactly 5 uppercase letters
    '''
    global word_list_global, invalid_indexes, invalid_index_copy, scrabble_dict, confirmed_list
    deleted = set()
    max_score = 0
    final_word = ''
    
    if len(guesses) == 0: #first guess
        word_list_global = set(word_list)
        invalid_indexes = invalid_index_copy
        confirmed_list = ['-', '-', '-', '-', '-']
        return 'SIREN'
    elif len(guesses) >= 1: #second guess beyond
        for i in range(5):
            if feedback[-1][i] == '-' and len(invalid_indexes[guesses[-1][i]]) == 0: #update invalid_indexes with every index for letters not in word
                invalid_indexes[guesses[-1][i]].update([0,1,2,3,4])
            elif ord(feedback[-1][i]) >= 65 and ord(feedback[-1][i]) <= 90: #if upper case, add to confirmed list
                confirmed_list[i] = feedback[-1][i]
            else: #if lowercase, update invalid indexes 
                invalid_indexes[guesses[-1][i]].add(i)

    if feedback[0] == '-----' and len(guesses) == 1:
        return 'ABOUT'
    
    for word in word_list_global:
        score = 0
        for index in range(len(word)):
            if (confirmed_list[index] != '-' and confirmed_list[index] != word[index]):
                deleted.add(word)
                print(confirmed_list)
                break
            elif (index in invalid_indexes[word[index]]):
                deleted.add(word)
                print(invalid_indexes)
                break
            else:
                score += scrabble_dict[word[index]]
        if score > max_score:
            max_score = score
            final_word = word

    word_list_global = word_list_global.difference(deleted)
    
    return final_word

    '''
                does to fit clues check
                - make sure all the confirmed letter are in the right place
                    for char in word:
                        if char != confirmed_dict[char] #value at key
                            not valid word
                - make sure no letter in a index they are known to not be in
                    for index in range(len(word)):
                        if index in invalid_indexes[word[index]]
                            not valid word
                - combine it together
                    for index in range(len(word)):
                        if (confirmed_list[index] != '-' and confirmed_list[index] != word[index])
                            or index in invalid_indexes[word[index]]
                            not valid word
    '''


# TODO: Define and implement your own functions!
def start_game():
    print("WELCOME TO WORDLE")
    num_guesses = 0
    secret_word = word_generator()
    winner = False
    guesses = []
    while num_guesses <= 6 and winner == False:
        guess = input("Please enter your guess: ")
        result = get_feedback(guess, secret_word)
        if result != 'This is an invalid word. Guess again!':
            num_guesses += 1
            guesses.append(result)
            for i in guesses:
                print(i)
        else:
            print(result)
            
        if result == secret_word:
            winner = True
    if winner == False:
        print("YOU LOST THE GAME!!")
        print(f"The secret word was {secret_word}.")
    else:
        print(f"YOU WON THE GAME IN {num_guesses} GUESSES!")
    
    start_over = input("Do you want to play again? Y/N ")
    if start_over.upper() == 'Y':
        return start_game()
    else:
        print("THANKS FOR PLAYING!")
    

def word_generator():
    return get_word_list()[random.randint(0, len(get_word_list())-1)]




if __name__ == "__main__":
    # TODO: Write your own code to call your functions here
    #start_game()
    guess_count = 0
    secret_word = word_generator()
    print(f"secret word: {secret_word}")
    guesses = []
    feedback_list = []
    guessed = False
    while guess_count < 5 and not guessed:
        AI_guess = get_AI_guess(get_word_list(), guesses, feedback_list)
        guesses.append(AI_guess)
        feedback_list.append(get_feedback(AI_guess, secret_word))
        guess_count += 1

        if AI_guess == secret_word:
            break
    
    word_list_global = word_generator()
    invalid_indexes = invalid_index_copy

    print(f"guess list: {guesses}")
    print(f"feedback list: {feedback_list}")