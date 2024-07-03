import random
# user will guess based on feed back from the computer
def user_guess (x):
    random_number = random.randint(1,x)
    guess = 0
    while (guess != random_number):
        guess = int(input(f'Guess a number between 1 and {x}: '))
        if guess > random_number:
            if guess - random_number >= 25:
                print('Sorry, guess again, too high.')
            elif guess - random_number < 25:
                print('Sorry, guess again, high.')
        else:
            if random_number - guess >= 25:
                print('Sorry, guess again, too low.')
            elif random_number - guess < 25:
                print('Sorry, guess again, low.')
        
    print(f'Yay, Congrats. You have guessed the number {random_number} correctly.')

# computer will guess based on feedback from the user    
def computer_guess(x):
    low = 1
    high = x
    feedback = '' # whether guess is low, high, correct

    while feedback != 'c' :
        if low != high:
            guess = random.randint(low, high)
        else:
            guess = low # could also be high, as low = high
        feedback = input(f'is {guess} High (H), low (L) or Correct (C): ').lower()
        if feedback == 'h':
            high  = guess - 1
        elif feedback == 'l':
            low = guess + 1
    print(f'Yay, Congrats. the computer have guessed your number, which is {guess}, correctly.')


user_guess (100)
#computer_guess (100)