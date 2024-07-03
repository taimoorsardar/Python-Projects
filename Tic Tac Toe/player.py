import math
import random

class Player:
    def __init__(self, letter):
        # letter is x or o
        self.letter = letter

    # we want all players to get their next move
    def get_move(self, game):
        pass

class RandomComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        # get a random valid spot for our next game
        square = random.choice(game.available_moves())
        return square

class HumanPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)
    
    def get_move(self, game):
        valid_square = False
        val =  None
        while not valid_square:
            square =  input(self.letter + '\'s turn. Input move (0-8): ')
            '''
            check that this is a correct value by trying to cast
            it into an integer and if its not, then we say it's invalid 
            if that spot is not available on the board, we also say it is invalid
            '''
            try: 
                val = int(square)
                if val not in game.available_moves():
                    raise ValueError
                valid_square = True
            except ValueError:
                print ('Invalid Square. Try Again.')

        return val

class GeniusComputerPlayer(Player):
    def __init__(self, letter):
        super().__init__(letter)

    def get_move(self, game):
        if len(game.available_moves()) == 9:
            square = random.choice(game.available_moves()) # randomly start with one

        else:
            # get the square based off the minimax algorithm
            square = self.minimax(game, self.letter)['position']
        return square
    
    def minimax(self, state, player):
        # state refers to screenshots of the game
        max_player = self.letter # yourself!!
        other_player = 'O' if player == 'X' else 'X'

        '''
        check if the previous move is a winner
        this is our base case
        '''
        if state.current_winner == other_player:
            '''
            return position and score because we need to keep track of the score
            for minimax to work
            '''
            return {'position': None, 'score': 1 * (state.num_empty_squares() + 1) if other_player == max_player else -1 * (
                        state.num_empty_squares() + 1)
                    }
        elif not state.empty_squares(): # no empty squares
            return {'position': None, 'score': 0}
        
        if player == max_player:
            best = {'position': None, 'score': -math.inf} # each score should maximize (be larger)
        else:
            best = {'position': None, 'score': math.inf} # each score should minimize (be smaller)
        
        for possible_move in state.available_moves():
            # step 1 make a move, try that spot
            state.make_move(possible_move, player)
            
            # step 2 recurse using minimax to simulate a game after making that move
            sim_score = self.minimax(state, other_player) # now we alternate players
            
            # step 3 undo that move
            state.board[possible_move] = ' '
            state.current_winner = None
            sim_score['position'] = possible_move # otherwise we will get messed up from the recursion

            # step 4 update the dictionaries if necessary
            if player == max_player:
                if sim_score['score'] > best['score']:
                    best = sim_score    # replace best
            else:
                if sim_score['score'] < best['score']:
                    best = sim_score    # replace best
        return best