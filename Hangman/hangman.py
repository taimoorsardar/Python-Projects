import random
from words import words
import string

# this function is used to get a valid word from the above lists as some words have dashes or spacec in between them 
def get_valid_words(words):
    word = random.choice(words) # randomly choosing something from the list
    while "-" in word or " " in word:
        word = random.choice(words)
    
    return word.upper() # uppercase all letters

# we need to keep track of which letters we guessed and which correct letters in the word we guessed 
def hangman():
    word = get_valid_words(words)
    word_letters = set(word) # letters in the words
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # what the user has guessed

    lives = 10

    # getting user input
    while len(word_letters) > 0 and lives > 0:
        #letters used
        #print ("You have "+lives+" lives left")
        print('You have ',lives,'used these lettrs:  ', ' '.join(used_letters))

        #what current word is but with dashes which letters are yet to be guessed
        word_list = [letter if letter in used_letters else '-' for letter in word]
        print ('Current word: ',' '.join(word_list))

        user_letter =  input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
            else:
                lives-=1
                print("Wrong letter")
        elif user_letter in used_letters:
            print("You have already used this character. Please try again")
        else: 
            print ("Invalid Character. Please try again")
    if lives == 0:
        print('You died , Sorry\nBetter luck next time\nThe Word was:  ', word)
    else:
        print("Yay you have guessed the word.\nThe word was: ",  word)
hangman()