def find_next_empty(puzzle):
    '''
    find the next row, col on the puzzle that's not filled yet -> rep with -1
    return row, col tuple (or (None, None) if there is none)
    '''
    for r in range(9):
        for c in range(9):
            if puzzle[r][c] == -1:
                return r,c
    return None,None # if no spaces left

def is_valid(puzzle, guess, row, col):
    '''
    figures out whether the guess at the row/col of the puzzle is valid  guess
    return True if is valid, otherwise False
    '''
    # Row 
    row_vals = puzzle[row]
    if guess in row_vals:
        return False
    
    # Columns
    col_vals = [puzzle[i][col] for i in range(9)]
    
    if guess in col_vals:
        return False

    # 3x3 grids in sudoku
    row_start = (row//3)*3
    col_start = (col//3)*3
    for r in range(row_start, row_start +3):
        for c in range(col_start, col_start+3):
            if puzzle[r][c] == guess:
                return False
    
    return True

def solve_sudoku(puzzle):
    '''
    solve soduke using backtracking!
    our puzzle is a list of lists, where each  inner list is a row in a soduko puzzle
    return whether a solution exists
    mutates puzzle to be the solution (if solution exists)
    '''
    # Step 1 choose somewhere on the puzzle to make a guess
    row, col = find_next_empty(puzzle)

    # Step 1.1 if there's nowhere left then we're done because we only allowed valid inputs
    if row is None:
        return True
    
    # Step 2 if there is a place to put a number, then make a guess between 1 and 9
    for guess in range (1,10):
        # Step 3 check if this guess is valid
        if is_valid(puzzle,guess,row,col):
            # Step 3.1 if this is valid, then place that guess on that puzzle
            puzzle[row][col] = guess
            
            # Step 4 recursively call our function
            if solve_sudoku(puzzle):
                return True
        
        # Step 5 if not valid OR if our guess does not solve the puzzle, then we need to backtrack and try a new number
        puzzle[row][col] = -1 # reset the guess
    
    # Step 6: if none of our guesses work, then this puzzle is unsolvable
    return False

if __name__ == '__main__':
    # change this board as you want
    example_board = [
        [3, 9, -1,   -1, 5, -1,   -1, -1, -1],
        [-1, -1, -1,   2, -1, -1,   -1, -1, 5],
        [-1, -1, -1,   7, 1, 9,   -1, 8, -1],

        [-1, 5, -1,   -1, 6, 8,   -1, -1, -1],
        [2, -1, 6,   -1, -1, 3,   -1, -1, -1],
        [-1, -1, -1,   -1, -1, -1,   -1, -1, 4],

        [5, -1, -1,   -1, -1, -1,   -1, -1, -1],
        [6, 7, -1,   1, -1, 5,   -1, 4, -1],
        [1, -1, 9,   -1, -1, -1,   2, -1, -1]
    ]
    print(solve_sudoku(example_board))
    print(example_board)