# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category B - Problem 8: Noughts and Crosses (Difficulty: ****)
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# This is a simple Noughts and Crosses
# game written for the terminal.
# The values on the grid are stored
# as integers in a 1D array.
# (screw ugly 2D arrays...)
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Imports
import random

# Constants
GRID_WIDTH     = 3
GRID_HEIGHT    = 3
ID_EMPTY       = 2
ID_NOUGHTS     = 0
ID_CROSSES     = 1
GRID_SYMBOLS   = ["0", "X", " "]
GRID_HEADER    = "   - 0 - 1 - 2 -"
GRID_SEPERATOR = "   -------------"

# Global vars
grid_vals      = [ID_EMPTY] * (GRID_WIDTH * GRID_HEIGHT) # All values on the grid. Initialised to empty.

# Score of player and computer.
score_player = 0
score_ai = 0
tie_count = 0

# Draw the grid.
def draw_grid():
    # Iterate through every cell in the grid.
    s = ""
    print(GRID_HEADER)
    print(GRID_SEPERATOR)
    for y in range(0, GRID_HEIGHT):
        # chr will convert int to ASCII representation.
        # (add 0x41 to start at 'A')
        s = " {} |".format(chr(y + 0x41))
        for x in range(0, GRID_WIDTH):
            symb = GRID_SYMBOLS[grid_vals[y * GRID_WIDTH + x]]
            s += " {} |".format(symb)
        print(s)
        print(GRID_SEPERATOR)

# Gets the input from the player, and parses
# it into a grid position.
# Inputs are written in the format a0, b2, c1, etc,
# where the letter represents row, and number represents
# column.
def parse_input():
    global grid_vals
    row    = 0
    column = 0
    while True:
        inp = input("Enter your next move: ").lower()
        try:
            # ord converts ASCII to integer.
            # Subtract 0x61 ('a') to get position in alphabet.
            row = ord(inp[0]) - 0x61;
            column = int(inp[1])
        except:
            print("Invalid input.")
            continue

        # Make sure it was a valid letter, from zero to grid height, and valid number from 0 to grid width.
        if not row < GRID_HEIGHT or row < 0 or not column < GRID_WIDTH or column < 0:
            print("Invalid input.")
            continue

        # Check to make sure the cell isn't already occupied.
        if grid_vals[row * GRID_WIDTH + column] != ID_EMPTY:
            print("Position '" + inp + "' is already occupied. Specify a different one.")
            continue

        break
    return [column, row]

# Generates a random move on the board.
# This is used for the first move.
# (and currently all the AI's moves.)
def ai_random_move():
    legalmoveindices = []
    idx = 0
    for i in grid_vals:
        if i == ID_EMPTY:
            legalmoveindices.append(idx)
        idx += 1

    # Select a random move that is legal.
    sel = legalmoveindices[random.randrange(0, len(legalmoveindices))]

    # Convert the 1D value to 2D position using some wizard-like sorcery.
    column = sel % GRID_WIDTH
    row = int(round((sel - column) / GRID_HEIGHT))
    #print("sel:", sel, "column:", column, "row:", row)

    # Return list constructed from the position.
    return [column, row]

# Convert a 1D position on the grid to 2D.
def pos1d_to_2d(i):
    column = i % GRID_WIDTH
    row = int(round((i - column) / GRID_HEIGHT))
    return [column, row]

# Generates a move on the board that is either
# random or a winning move.
def ai_smart_move(ai_id, player_id):
    global grid_vals

    # Temporary grid used for checking winning moves.
    grid_temp = []
    for j in grid_vals:
        grid_temp.append(j)

    # First check any moves that are winning moves.
    for i in range(0, len(grid_vals)):
        if grid_vals[i] != ID_EMPTY:
            # Occupied cell, skip.
            continue
        # Set this point in a temporary board to be the AI's move.
        grid_temp[i] = ai_id

        # Check if the solution exists by setting this point to AI's.
        if find_solution(ai_id, grid_temp):
            # Convert the 1D value to 2D position.
            return pos1d_to_2d(i)

        # See if the move can be used by other player to win.
        # If it can the AI will take it.
        grid_temp[i] = player_id
        if find_solution(player_id, grid_temp):
            # Convert pos to 2D and take it.
            return pos1d_to_2d(i)

        # Didn't find solution, reset the grid to old.
        grid_temp[i] = ID_EMPTY

    # No winning moves, pick a random one.
    return ai_random_move()

# Make the move of the passed ID.
# Checks for pre-occupation must be done PRIOR 
# to calling this method!
def next_move(move_pos, id, player_id, ai_id):
    # Set the ID at the specified point to the ID.
    grid_vals[move_pos[1] * GRID_WIDTH + move_pos[0]] = id

    # Check for winner.
    if find_solution(player_id, grid_vals):
        global score_player
        draw_grid()
        print("Congratulations, you won.")
        score_player += 1
        return False
    if find_solution(ai_id, grid_vals):
        global score_ai
        draw_grid()
        print("You lose.")
        score_ai += 1
        return False
    # Check for tie
    if not ID_EMPTY in grid_vals:
        global tie_count
        draw_grid()
        print("You tied with the computer.")
        tie_count += 1
        return False
    return True

# Looks for a solution for the ID's points.
# If found return value is True, if not - False.
def find_solution(id, grid):
    # ------------------------
    # STRAIGHT-LINE ALGORITHMS:
    # ------------------------

    # Check horizontal.
    for y in range(0, GRID_HEIGHT):
        count = 0
        for x in range(0, GRID_WIDTH):
            if grid[y * GRID_HEIGHT + x] == id:
                count += 1
        if count == GRID_WIDTH:
            return True
    
    # Check Vertical.
    for x in range(0, GRID_WIDTH):
        count = 0
        for y in range(0, GRID_HEIGHT):
            if grid[y * GRID_HEIGHT + x] == id:
                count += 1
        if count == GRID_HEIGHT:
            return True

    # ------------------------
    # DIAGONAL ALGORITHMS:
    # (Note that these will break if GRID_WIDTH != GRID_HEIGHT)
    # ------------------------

    # Check backwards diagonal
    count = 0
    for i in range(0, GRID_WIDTH):
        if grid[i * GRID_WIDTH + i] == id:
            count += 1
    if count == GRID_WIDTH:
        return True

    # Check forwards diagonal
    idx = 0
    count = 0
    for i in range(0, GRID_WIDTH):
        idx += GRID_WIDTH - 1
        if grid[idx] == id:
            count += 1
    if count == GRID_WIDTH:
        return True
        
    return False

# This is the main function. Gets called
# when the program is executed.
def main_func():
    print("-- -- Noughts & Crosses -- --")
    global grid_vals

    # Number of rounds played.
    round_counter = 0

    # Loop over infinite number of rounds. User is asked at
    # end of round whether they want to continue or exit.
    while True:
        # Is the player noughts?
        player_id = random.choice([ID_NOUGHTS, ID_CROSSES])
        ai_id = player_id ^ ID_CROSSES
        print("You are", "noughts" if player_id == ID_NOUGHTS else "crosses")
        
        # Reinitialise grid to empty.
        for i in range(GRID_WIDTH * GRID_HEIGHT):
            grid_vals[i] = ID_EMPTY

        # Choose a player to go first by random.
        # If computer is chosen, they will pick a random cell.
        first_player = random.choice([ID_NOUGHTS, ID_CROSSES]) 
        if first_player == ai_id :
            next_move(ai_random_move(), ai_id, player_id, ai_id)
            print("Computer played the first move.")
        else:
            print("You are playing the first move.")

        # Main game loop.
        while True:
            draw_grid();
            if not next_move(parse_input(), player_id, player_id, ai_id):
                break
            # Stupid AI: Picks a random cell.
            # next_move(ai_random_move(), ai_id)
            # Smart AI: Checks for move that will yield a win.
            if not next_move(ai_smart_move(ai_id, player_id), ai_id, player_id, ai_id):
                break

        tie_str = "\n  Ties: " + str(tie_count) if tie_count > 0 else "" 
        print("Scores:\n  You:", score_player, "\n  Computer:", score_ai, tie_str)
        s = "Type 'p' to play again, 'x' to exit.\n"
        while True:
            exitcode = input(s)[0]
            s = ""
            if exitcode == 'x':
                return
            if exitcode == 'p':
                break
            print("Invalid response.")

        round_counter += 1

main_func()