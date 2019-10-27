# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category C - Major Project: Snake
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# This is a simple snake game with
# basic functionality.
# Curses TUI reference:
# https://docs.python.org/2/howto/curses.html
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Imports
import curses # The TUI library the project uses.
from curses import wrapper

# Constants
GAME_WIDTH   = 48        # Width of the game.
GAME_HEIGHT  = 16        # Height of the game.
SCREEN_NONE  = -1        # Set cur_screen to this to quit.
SCREEN_MENU  = 0         # Screen ID for main menu
SCREEN_GAME  = 1         # Screen ID for game screen
SCREEN_PAUSE = 2         # Screen ID for pause menu
BTNID_MENU_PLAY = 0      # ID For play button on main menu
BTNID_MENU_QUIT = 1      # ID For quit button on main menu
BTNID_PAUSE_RESUME = 0   # ID for Resume button on pause menu.
BTNID_PAUSE_GOTOMENU = 1 # ID for Menu button on pause menu.
GRIDID_EMPTY = 0         # Grid cell: empty
GRIDID_HEAD  = 1         # Grid cell: snake head
GRIDID_TAIL  = 2         # Grid cell: snake tail.
GRIDATTR_EMPTY = curses.A_DIM
GRIDATTR_HEAD  = 0
GRIDATTR_TAIL  = 0
GRIDCHR_HEAD   = 'Y'
GRIDCHR_TAIL   = 'X'
IDX_X = 1 # Index in a position list which represents x.
IDX_Y = 0 # Index in a position list which represents y.

# Global variables.
cur_screen = SCREEN_MENU    # Current screen.
wnd = None                  # The main window
scrdims = None              # The screen dimensions of curses window, (y, x)
sel_idx = 0                 # The current selection index for button on the cur screen.
colour_supported = False    # Are colours supported?
player_pos_head  = [3, 5]   # Position of the player head. ([y, x] because curses uses this format for some reason...)
player_velo      = [0, 1]   # Velocity of the player, initialised to move right.

# List of tail nodes that the player has. (Currently initialised to have 4 points for testing.)
player_tail      = [[3, 4], [3, 3], [3, 2], [3, 1]]

# The game grid, initialised to empty by default.
game_grid  = [GRIDID_EMPTY] * GAME_WIDTH * GAME_HEIGHT

# Initialise the game.
def game_init():
    global wnd
    global colour_supported

    # Hide cursor and set timeout
    curses.curs_set(False)
    wnd.timeout(500)
    #wnd.notimeout(True)

    # Check for terminal colour support.
    colour_supported = curses.has_colors()
    if colour_supported:
        # Initialise colours.
        # (Source: https://repl.it/talk/learn/Game-Tutorial-Space-Invaders/9550)
        curses.init_pair(1, curses.COLOR_RED,     curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLUE,    curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_GREEN,   curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(5, curses.COLOR_CYAN,    curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_YELLOW,  curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLACK,   curses.COLOR_BLACK)

        # Reinitialise these "constants", (can't use color_pair
        #    until initscr gets called...)
        global GRIDATTR_EMPTY
        global GRIDATTR_HEAD
        global GRIDATTR_TAIL
        GRIDATTR_EMPTY = curses.color_pair(7) # Set bg to white.
        GRIDATTR_HEAD  = curses.color_pair(3) # Set head to green.
        GRIDATTR_TAIL  = curses.color_pair(3) # Set tail to green.


# Adds a centred string to the curses TUI.
# Pass an integer as ypos to adjust the y offset.
# Pass string attributes into attr.
def addstr_centred(ypos, data, attr=0):
    # Compute x-pos by getting total width and subtracting
    #   half of the string's length.
    xpos = int((int(scrdims[1]) - int(len(data))) / 2)
    if attr != 0:
        wnd.addstr(ypos, xpos, data, attr)
    else:
        wnd.addstr(ypos, xpos, data)

# Wraps position between the grid bounds
def grid_wrap(vinp):
    v = [vinp[0], vinp[1]]
    # Wrap X
    if (v[IDX_X] < 0):
        v[IDX_X] += GAME_WIDTH
    if (v[IDX_X] >  GAME_WIDTH - 1):
        v[IDX_X] -= GAME_WIDTH

    # Wrap Y
    if (v[IDX_Y] < 0):
        v[IDX_Y] += GAME_HEIGHT
    if (v[IDX_Y] >  GAME_HEIGHT - 1):
        v[IDX_Y] -= GAME_HEIGHT

    return v


# Add two vectors, which are represented as lists.
# (Used as just a shorthand, since operator overloading
#    would slightly over-complicate things here.)
def add_vectors(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

# Loop method for the main menu
def game_loop_menu():
    # Global variable usage
    global sel_idx
    global cur_screen

    # Draw header.
    addstr_centred(1, " -- SNAKE GAME -- ")
    addstr_centred(2, "Written by mikejzx for ICT CAT")
    addstr_centred(3, "(Use arrow keys to navigate.)")

    # Draw buttons
    btn_attrs = [0, 0]
    btn_attrs[sel_idx] = curses.A_STANDOUT
    addstr_centred(5, "Play game", btn_attrs[BTNID_MENU_PLAY])
    addstr_centred(6, "Quit", btn_attrs[BTNID_MENU_QUIT])

    # Get and check input.
    key = wnd.getch()
    if key == curses.KEY_UP:
        # Key up, decrement selected button index. 
        sel_idx = sel_idx - 1
    elif key == curses.KEY_DOWN:
        # Key down, increment selection
        sel_idx = sel_idx + 1
    elif (key == curses.KEY_ENTER or key == 0x0A or key == 0x0D):
        # Return key pressed, check what was pressed. (Checks for both CR and LF ASCII codes just in case.)
        if sel_idx == BTNID_MENU_PLAY:
            # Play button, switch to game screen.
            cur_screen = SCREEN_GAME
        elif sel_idx == BTNID_MENU_QUIT:
            # Quit the game
            cur_screen = SCREEN_NONE
            sel_idx = 0
    
    # Wrap selection around from 0 to 1
    sel_idx %= 2

# Loop method for the game itself.
def game_loop_main():
    global cur_screen
    global wnd
    global game_grid
    global player_pos_head
    global player_velo
    global player_tail

    # Game logic.
    
    # To shift tail nodes we need to store the old tail.
    player_tail_old = []
    for i in player_tail:
        player_tail_old.append(i)

    # Give first node the head position, and shift all nodes of tail.
    player_tail[0] = player_pos_head
    for i in range(1, len(player_tail)):
            player_tail[i] = player_tail_old[i - 1]

    # Apply velocity and clamp position to grid bounds
    player_pos_head = grid_wrap(add_vectors(player_pos_head, player_velo))

    # Clear entire grid.
    # (Probably not very efficient)
    game_grid = [GRIDID_EMPTY] * GAME_WIDTH * GAME_HEIGHT
    
    # Set head cell.
    game_grid[player_pos_head[IDX_Y] * GAME_WIDTH + player_pos_head[IDX_X]] = GRIDID_HEAD

    # Set tail cells.
    for i in player_tail:
        game_grid[i[IDX_Y] * GAME_WIDTH + i[IDX_X]] = GRIDID_TAIL

    # Draw the game
    for y in range(0, GAME_HEIGHT):
        for x in range(0, GAME_WIDTH):
            cell = game_grid[y * GAME_WIDTH + x]

            # Change colour based on cell.
            if cell == GRIDID_EMPTY:
                # Empty cell.
                wnd.addstr(y, x, "." if x % 2 == 0 else " ", GRIDATTR_EMPTY)
            elif cell == GRIDID_HEAD:
                # Head cell.
                wnd.addstr(y, x, GRIDCHR_HEAD, GRIDATTR_HEAD)
            elif cell == GRIDID_TAIL:
                # Tail cell.
                wnd.addstr(y, x, GRIDCHR_TAIL, GRIDATTR_TAIL)

    # Get and check input.
    # (May adjust timeout to be 2x faster in X)
    key = wnd.getch()
    if key == ord("p") or key == ord("P"):
        cur_screen = SCREEN_PAUSE
    elif key == curses.KEY_UP:
        player_velo = [-1, 0]
    elif key == curses.KEY_DOWN:
        player_velo = [1, 0]
    elif key == curses.KEY_LEFT:
        player_velo = [0, -1]
    elif key == curses.KEY_RIGHT:
        player_velo = [0, 1]


# Loop method for the pause menu.
def game_loop_pause():
    # Global variable usage
    global sel_idx
    global cur_screen

    # Draw header.
    addstr_centred(1, " -- PAUSED -- ")

    # Draw buttons
    btn_attrs = [0, 0]
    btn_attrs[sel_idx] = curses.A_STANDOUT
    addstr_centred(3, "Resume", btn_attrs[BTNID_PAUSE_RESUME])
    addstr_centred(4, "Goto Menu", btn_attrs[BTNID_PAUSE_GOTOMENU])

    # Get and check input.
    # (Very similar to menu's stuff, may need to make a method...)
    key = wnd.getch()
    if key == curses.KEY_UP:
        # Key up, decrement selected button index. 
        sel_idx = sel_idx - 1
    elif key == curses.KEY_DOWN:
        # Key down, increment selection
        sel_idx = sel_idx + 1
    elif (key == curses.KEY_ENTER or key == 0x0A or key == 0x0D):
        # Return key pressed, check what was pressed. (Checks for both CR and LF ASCII codes just in case.)
        if sel_idx == BTNID_PAUSE_RESUME:
            # Play button, switch to game screen.
            cur_screen = SCREEN_GAME
        elif sel_idx == BTNID_PAUSE_GOTOMENU:
            # Quit to menu.
            cur_screen = SCREEN_MENU
            sel_idx = 0

            # Reset game here.
            # ...
    
    # Wrap selection around from 0 to 1
    sel_idx %= 2


# The main game loop.
def game_loop():
    # Clear the screen.
    wnd.clear()

    # Adjust what is drawn based on the "screen" index.
    if cur_screen   == SCREEN_MENU:
        # -- Drawing the menu. --
        game_loop_menu()
    elif cur_screen == SCREEN_GAME:
        # -- Drawing the menu. --
        game_loop_main()
    elif cur_screen == SCREEN_PAUSE:
        # -- Drawing the menu. --
        game_loop_pause()
    elif cur_screen == SCREEN_NONE:
        # -- Exit the game loop.
        return False

    # Re-draw
    wnd.refresh()

    # Allow next loop
    return True

# Called on application exit.
def game_deinitialise():
    # Nothing to do...
    pass

# The main method. This gets called when the application
# is executed.
def main(stdscr):
    # Assign global screen object.
    global wnd
    wnd = stdscr

    # Get the screen dimensions.
    global scrdims
    scrdims = wnd.getmaxyx()

    # Initialise the game. 
    game_init()

    # Run the main game loop.
    while game_loop():
        pass

# Call the main method in a curses TUI wrapper object.
# This allows for cleaner error handling...
wrapper(main)