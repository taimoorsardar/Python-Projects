import random
import re
class Board:
    def __init__(self,dim_size, num_bombs):
        self.dim_size = dim_size
        self.num_bombs = num_bombs

        # helper function
        self.board = self.make_new_board()
        self.assign_values_to_board()
        # initialize a set to keep track of whihc locations we've uncovered
        # we'll save (row, col) tuples
        self.dug = set() # if we dig at (0,0), then self.dug = (0,0)

    def make_new_board(self):
        
        # generate a new board
        board =[[None for _ in range (self.dim_size)] for _ in range(self.dim_size)]

        bombs_planted = 0
        while bombs_planted < self.num_bombs:
            loc = random.randint(0, self.dim_size**2 - 1) # getting a random location for the bomb
            row = loc//self.dim_size                      # extracting the row for the bomb
            col = loc % self.dim_size                     # extracting the col for the bomb 

            if board[row][col] == "*":
                # bomb already there
                continue
            board[row][col] = "*" # planting the bomb
            bombs_planted += 1

        return board
    
    def assign_values_to_board(self):
        # assign number 0-8 in the empty spaces representing the neighboring bombs

        for r in range(self.dim_size):
            for c in range(self.dim_size):
                if self.board[r][c] == "*":
                    # if this is already a bomb, we don't want to calculate anything
                    continue
                self.board[r][c] = self.get_num_neighboring_bombs(r,c)

    def get_num_neighboring_bombs(self,row,col):
        '''
        let's iterate through each of the neighboring positions and sum number of bombs
        top left: row-1, col-1
        top middle: row-1, col
        top right: row-1, col+1
        left: row, col-1
        right: row, col+1
        bottom left: row+1, col-1
        ttom middle: row+1, col
        bottom right: row+1, col+1
        '''
        # make sure to not go out of bounds!
        num_neighboring_bombs = 0 # a counter
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range (max(0,col-1),min(self.dim_size-1,col+1)+1):
                if r == row and c == col:
                    # our original location, we dont check this
                    continue
                if self.board[r][c] == "*":
                    num_neighboring_bombs += 1
        return num_neighboring_bombs 

    def dig (self, row, col):
        ''' 
        dig at that location
        return True if successful dig, False if bomb dug

        a few scenarios:
        hit a bomb -> game over
        dig at location with neighboring bombs -> finish dig
        dig at location with no neighboring bombs -> recursively dig neighbors!
        '''
        self.dug.add((row,col)) # keep track that we dug here

        if self.board[row][col]== "*":
            return False
        elif self.board[row][col] > 0:
            return True
        for r in range(max(0,row-1),min(self.dim_size-1,row+1)+1):
            for c in range (max(0,col-1),min(self.dim_size-1,col+1)+1):
                if (r,c) in self.dug:
                    continue # do not dig at the same postion again
                self.dig(r,c)
        
        # if our dig didn't hit a bomb, we shouldn't hit a bomb here
        return True

    def __str__(self):
        '''
        this function will run if you call print on this object,
        it'll print out what this function returns
        return the string that shows the board to a player
        '''
        # creating a new array that represents what the user would see
        visible_board = [[None for _ in range(self.dim_size)] for _ in range(self.dim_size)]
        for r in range (self.dim_size):
            for c in range(self.dim_size):
                if (r,c) in self.dug:
                    visible_board[r][c] = str(self.board[r][c])
                else:
                    visible_board[r][c] = " "

        # put this together in a string 
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.dim_size):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.dim_size)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.dim_size)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep
    
    def display(self):
        self.dug =[(r,c) for r in range(self.dim_size) for c in range(self.dim_size)]
        print (self)
# play the game
def play(dim_size = 10, num_bombs = 10):
    # Step 1 create the board and plant the bombs
    board = Board(dim_size, num_bombs)

    safe = True
    while len(board.dug) < board.dim_size**2 - num_bombs:
        print(board)
        # Step 2 show the user the board and ask for where they wan to dig
        user_input = re.split(',(\\s)*',input ("Where would you like to dig? ( Input as row,col ): "))
        row, col = int(user_input[0]), int(user_input[-1])

        if row<0 or col<0 or row> board.dim_size or col>board.dim_size:
            print("Invalid location.Try again.")
            continue
        # Step 3a: if location is not bomb, dig recursively until each square is at least next to a bomb
        safe = board.dig(row,col)

        if not safe:
            break # game over

    # 2 ways to end a loop, lets check which one
    if safe:
        print("CONGRATULATIONS!!!! YOU ARE VICTORIOUS")
    
    # Step 3b: if location is bomb show game over message
    else:
        print("SORRY GAME OVER :(")
    board.display()
if __name__ == '__main__': # good practice
    play()