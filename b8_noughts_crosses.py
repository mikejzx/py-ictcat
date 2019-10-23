# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category B - Problem 8: Noughts and Crosses
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
    
    # Prevent divison by zero from the modulo.
    if sel == 0:
        return [0, 0]

    # Convert the 1D value to 2D position using some wizard-like sorcery.
    grid_val_size = GRID_WIDTH * GRID_HEIGHT
    column = grid_val_size % sel
    row = int(round((grid_val_size - column) / GRID_HEIGHT))

    print("sel: ", sel, "row: ", row, " col:", column)

    # Return list constructed from the position.
    return [column, row - 1]

# Make the move of the passed ID.
# Checks for pre-occupation must be done PRIOR 
# to calling this method!
def next_move(move_pos, id):
    # Set the ID at the specified point to the ID.
    grid_vals[move_pos[1] * GRID_WIDTH + move_pos[0]] = id

# Looks for a solution for the ID's points.
# If found return value is True, if not - False.
def find_solution(id):
    # ------------------------
    # STRAIGHT-LINE ALGORITHMS:
    # ------------------------

    # Check horizontal.
    for y in range(0, GRID_HEIGHT):
        count = 0
        for x in range(0, GRID_WIDTH):
            if grid_vals[y * GRID_HEIGHT + x] == id:
                count += 1
        if count == GRID_WIDTH:
            return True
    
    # Check Vertical.
    for x in range(0, GRID_WIDTH):
        count = 0
        for y in range(0, GRID_HEIGHT):
            if grid_vals[y * GRID_HEIGHT + x] == id:
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
        if grid_vals[i * GRID_WIDTH + i] == id:
            count += 1
    if count == GRID_WIDTH:
        return True

    # Check forwards diagonal
    idx = 0
    count = 0
    for i in range(0, GRID_WIDTH):
        idx += GRID_WIDTH - 1
        if grid_vals[idx] == id:
            count += 1
    if count == GRID_WIDTH:
        return True
        
    return False

# This is the main function. Gets called
# when the program is executed.
def main_func():
    print("-- -- Noughts & Crosses -- --")
    
    # Score of player and computer.
    score_player = 0
    score_ai = 0
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
            next_move(ai_random_move(), ai_id)
            print("Computer played the first move.")
        else:
            print("You are playing the first move.")

        # Main game loop.
        while True:
            draw_grid();
            next_move(parse_input(), player_id)
            next_move(ai_random_move(), ai_id)

            # Check for winner.
            if find_solution(player_id):
                print("Congratulations, you won.")
                score_player += 1
                break
            if find_solution(ai_id):
                print("You lose.")
                score_ai += 1
                break

        print("Score:\n  You:", score_player, "\n  Computer:", score_ai)
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