import random

def play():
    rounds  = int(input ("Please enter an integer to select how many rounds you want to play: "))
    c_points = 0
    u_points = 0
    while (rounds != 0):            
        user = input("Enter your input from the following \n 'r' for rock, 'p' for papers, 's' for scissors: ")
        computer =  random.choice(['r', 'p', 's'])
        if user == computer:
            display_choice(user, computer)
            display_points(u_points, c_points)
        if is_win(user, computer):
            display_choice(user, computer)
            u_points +=10
            display_points(u_points, c_points)
        if is_win(computer, user):
            display_choice(user, computer)
            c_points +=10
            display_points(u_points, c_points)
        rounds -=1

    if u_points == c_points:
        print ('Final Points')
        display_points(u_points,c_points)
        return "It's a Tie"

    if u_points > c_points:
        print ('Final Points')
        display_points(u_points,c_points)
        return "You Won"
    else:
        print ('Final Points')        
        display_points(u_points,c_points)
        return "You Lost"
# helper function
def is_win(player, opponent):
    # return true if player wins
    # r > s, s > p, p > r
    if (player == 'r' and opponent == 's') or (player == 's' and opponent == 'p') or (player == 'p' and opponent == 'r'):
        return True
    
def display_points(p1, p2):
    print("User Points: " ,p1)
    print ("Computer points: " ,p2)

def display_choice(c1, c2):
    print("Your Choice: " + c1)
    print("Computer Choice: " + c2)

print(play())