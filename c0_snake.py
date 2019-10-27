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

SCREEN_MENU  = 0    # Screen ID for main menu
SCREEN_GAME  = 1    # Screen ID for game screen
SCREEN_PAUSE = 2    # Screen ID for pause menu
BTNID_MENU_PLAY = 0 # ID For play button on main menu
BTNID_MENU_QUIT = 1 # ID For quit button on main menu

# Global variables.
cur_screen = SCREEN_MENU # Current screen.
wnd = None               # The main window
scrdims = None           # The screen dimensions
sel_idx = 0              # The current selection index for button on the cur screen. 

# Initialise the game.
def game_init():
    # Hide cursor
    curses.curs_set(False)
    #wnd.notimeout(True)

# Adds a centred string to the curses TUI.
# Pass an integer as ypos to adjust the y offset.
# Pass string attributes into attr.
def addstr_centred(ypos, data, attr=0):
    xpos = int((int(scrdims[1]) - int(len(data))) / 2)
    if attr != 0:
        wnd.addstr(ypos, xpos, data, attr)
    else:
        wnd.addstr(ypos, xpos, data)

# Loop method for the main menu
def game_loop_menu():
    # Global variable usage
    global sel_idx

    # Draw header.
    addstr_centred(1, " -- SNAKE GAME -- ")
    addstr_centred(2, " Written by mikejzx for ICT CAT ")
    addstr_centred(3, " (Use arrow keys to navigate.)")

    # Draw buttons
    btn_attrs = [0, 0]
    btn_attrs[sel_idx] = curses.A_STANDOUT
    addstr_centred(5, "Play game", btn_attrs[BTNID_MENU_PLAY])
    addstr_centred(6, "Quit", btn_attrs[BTNID_MENU_QUIT])

    # Get input.
    key = wnd.getch()

    # Key up, decrement selected button index. 
    if key == curses.KEY_UP:
        sel_idx = sel_idx - 1
    elif key == curses.KEY_DOWN:
        sel_idx = sel_idx + 1

    # Wrap selection around from 0 to 1
    sel_idx %= 2

# Loop method for the game itself.
def game_loop_main():
    pass

# Loop method for the pause menu.
def game_loop_pause():
    pass


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

    # Re-draw
    wnd.refresh()

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
    while True:
        game_loop()

# Call the main method in a curses TUI wrapper object.
# This allows for cleaner error handling...
wrapper(main)