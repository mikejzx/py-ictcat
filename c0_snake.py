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
import curses                 # The TUI library the project uses.
from curses import wrapper    # Wrapper to keep error-handling clean.
import random                 # For random.randrange()
import math                   # For math.random()
from datetime import datetime # For datetime.now()

# Constants
GAME_WIDTH   = 24        # Width  of the game.
GAME_HEIGHT  = 16        # Height of the game.
SCREEN_NONE  = -1        # Set cur_screen to this to quit.
SCREEN_MENU  = 0         # Screen ID for main menu
SCREEN_GAME  = 1         # Screen ID for game screen
SCREEN_PAUSE = 2         # Screen ID for pause menu
SCREEN_NEWHIGHEST = 3    # Screen ID for highest score screen.
SCREEN_RANKINGS   = 4    # Screen ID for rankings screen.
BTNID_MENU_PLAY = 0      # ID For play button on main menu
BTNID_MENU_SCORES = 1    # ID For scores button on main menu
BTNID_MENU_QUIT = 2      # ID For quit button on main menu
BTNID_PAUSE_RESUME = 0   # ID for Resume button on pause menu.
BTNID_PAUSE_GOTOMENU = 1 # ID for Menu button on pause menu.
BTNDESC_MENU = [
    "Play the game.", 
    "View the highest scores achieved on this computer.", 
    "Quit the game."
]
BTNDESC_PAUSE = [
    "Resume the game.",
    "Discard this game, and return to menu."
]
GRIDID_EMPTY = 0         # Grid cell: empty
GRIDID_HEAD  = 1         # Grid cell: snake head
GRIDID_TAIL  = 2         # Grid cell: snake tail.
GRIDID_APPL  = 3         # Grid cell: apple.
GRIDID_COLLIDE = 4       # Grid cell: player head collision with tail.
GRIDATTR_EMPTY = curses.A_DIM # Attribute for empty space. (See game_init() for proper initialisation)
GRIDATTR_HEAD  = 0       # Attribute for empty space.
GRIDATTR_TAIL  = 0       # Attribute for tail cell.
GRIDATTR_APPL  = 0       # Attribute for apple cell.
GRIDATTR_COLL  = 0       # Attribute for collission
STRATTR_GAMEOVER = 0     # String attribute for gameover text.
STRATTR_HEADER = 0       # String attribute for header text.
STRATTR_MISC = 0         # String attribute for miscellaneous text.
STRATTR_TOOLTIP = 0      # String attribute for tooltips.
GRIDCHR_HEAD   = "Y "    # Character representing head  for non-colour displays.
GRIDCHR_TAIL   = "X "    # Character representing tail  for non-colour displays.
GRIDCHR_APPL   = "A "    # Character representing apple for non-colour displays.
GRIDCHR_COLL   = "# "    # Character representing collision with tail for non-colour displays.
IDX_X = 1                   # Index in a position list  which represents x.
IDX_Y = 0                   # Index in a position list  which represents y.
BASE_DELAY = 300            # How long the game  takes  to move in seconds.
MINIMUM_DELAY = 50          # Minimum allowed delay.
MAX_APPLES = 3              # Limit to number of apples allowed on screen at once.
APPLE_SPAWN_DEVIATION = 2   # How much deviation there is in the spawn times of apples.
SCORE_INCREMENT = 1         # How much score is given per apple collected.
HISCORE_FPATH = "./hiscores.txt" # Highest score file path.
HISCORE_FSEP  = "/"         # Seperator for information in hiscores file.
HISCORE_NAME_LEN = 4        # Number of chars in hi-score name entries.
HISCORE_VALIDCHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-" # Valid characters for a hi-score entry.
HISCORE_VALIDCHARS_ORDS_UP  = [] # Valid characters for hi-score entry in char-code format. (Uppercase)
HISCORE_VALIDCHARS_ORDS_LOW = [] # Valid characters for hi-score entry in char-code format. (Lowercase)

# Global variables.
cur_screen = SCREEN_MENU    # Current screen.
wnd     = None              # The main window
scrdims = None              # The screen dimensions of curses window, (y, x)
sel_idx = 0                 # The current selection index for button on the cur screen.
colour_supported = False    # Are colours supported?
player_pos_head  = [0, 0]   # Position of the player head. ([y, x] because curses uses this format for some reason...)
player_velo      = [0, 0]   # Velocity of the player, initialised to move right.
game_speed     = BASE_DELAY # The speed of the game.
game_apples      = []       # The apples in the game.
game_score       = 0        # The player's score. Increases based on number of appls collected
game_ticks       = 0        # A game timer used to count when to spawn apples.      
game_over        = False    # Is the game over?
score_man        = None     # The main score manager object.
# High score screen state variables:
hsscr_ltr_idx      = 0                      # [High score screen] Current letter index.
hsscr_name         = ["A"] * HISCORE_NAME_LEN # [High score screen] Name entered currently.
hsscr_name_indices = [0]   * HISCORE_NAME_LEN # [High score screen] Name characters position in valid char string.

# List of tail nodes that the player has.
player_tail      = []

# The game grid, initialised to empty by default.
game_grid  = [GRIDID_EMPTY] * GAME_WIDTH * GAME_HEIGHT

# Score-manager class.
# Handles I/O of scores file.
class score_manager:
    # Constructor. No parameters as of yet.
    def __init__(self):
        self.score_list = []

        # Attempt to open hiscores file.
        try:
            scores_file = open(HISCORE_FPATH, "rt")
            # Read each line of existing file into the list.
            for line in scores_file:
                # Repeated often so put into a lamdba as a shorthand.
                l_find_fsep = lambda : line.find(HISCORE_FSEP)

                # Name
                x = l_find_fsep()     # Find first seperator.
                name = line[:x]     # Get the name
                line = line[x + 1:] # Remove name from line. (+1 to include seperator.)

                # Score.
                x = l_find_fsep()       # Find next seperator.
                score = int(line[:x]) # Read the score integer.
                line = line[x + 1:]   # Remove the score from line.

                # Date
                x = l_find_fsep()     # Find next seperator.
                date = line[:x]     # Read the date string.
                line = line[x + 1:] # Remove date from line.

                # Time, no seperator so just strip NL char.
                time = line.strip("\n")

                # Construct and push to back of list.
                self.score_list.append({
                    "name":     name,
                    "score":    score,
                    "date_str": date,
                    "time_str": time
                })
            
            # Close the file.
            scores_file.close()

            # Re-sort just in case.
            self.sort_scorelist()
        except:
            # Just create and close the file.
            scores_file = open(HISCORE_FPATH, "wt")
            scores_file.close()


    # Sorts the score list.
    def sort_scorelist(self):
        # This sort function sorts the list by the content's score.
        l_sort_func = lambda dict : dict["score"]
        
        # Call sort() with reverse flag enabled, and using the lambda above.
        self.score_list.sort(reverse=True, key=l_sort_func)

    # Add a new score to the score list.
    # Pass name of the user, and their score as arguments.
    # Time and date are computed automatically.
    def add_score(self, name, score):
        # Get date, time, and construct and push 
        # a dictionary of all info to the list.
        now = datetime.now()
        date = now.strftime("%d.%m.%Y")
        time = now.strftime("%H:%M")
        self.score_list.append({
            "name":     name,
            "score":    score,
            "date_str": date,
            "time_str": time
        })

        # Re-sort list of scores.
        self.sort_scorelist()

        # Write to file
        self.write_scores()

    # Write the scorelist to the hiscores file.
    def write_scores(self):
        # Open the scores file with write permission.
        scores_file = open(HISCORE_FPATH, "wt")

        # Iterate over score list and write each line
        for i in self.score_list:
            # Get each value from current score dictionary.
            n = i["name"]
            s = i["score"]
            d = i["date_str"]
            t = i["time_str"]

            # Write the line
            scores_file.write(n + HISCORE_FSEP + str(s) + HISCORE_FSEP + d + HISCORE_FSEP + t + "\n")

        # Close the file
        scores_file.close()

    # Returns the highest score in the list.
    def hiscore(self):
        if len(self.score_list) == 0:
            return 0
        return self.score_list[0]["score"]

    # Returns the name of the highest score owner.
    def hiscore_holder(self):
        if len(self.score_list) == 0:
            return "----"
        return self.score_list[0]["name"]

# Reset the values of the game iteself.
def game_reset():
    # Need these globals.
    global game_grid
    global player_pos_head
    global player_velo
    global player_tail
    global game_speed
    global game_apples
    global game_score
    global game_ticks
    global game_over

    # Reset values
    player_pos_head = [3, 5]
    game_grid   = [GRIDID_EMPTY] * GAME_WIDTH * GAME_HEIGHT
    player_velo = [0, 1]
    player_tail = [[3, 4], [3, 3], [3, 2], [3, 1]]
    game_speed  = BASE_DELAY
    game_apples = []
    game_score  = 0
    game_ticks  = 0
    shuffle_spawntime_offset()
    game_over = False

# Initialise the game.
def game_init():
    game_reset()
    global wnd
    global colour_supported
    global score_man
    global HISCORE_VALIDCHARS_ORDS_LOW
    global HISCORE_VALIDCHARS_ORDS_UP

    # Hide cursor and set timeout
    curses.curs_set(False)
    wnd.timeout(BASE_DELAY)

    # Initialise the valid chars list
    HISCORE_VALIDCHARS_ORDS_LOW = []
    HISCORE_VALIDCHARS_ORDS_UP  = []
    for i in HISCORE_VALIDCHARS:
        HISCORE_VALIDCHARS_ORDS_UP.append(ord(i))
        HISCORE_VALIDCHARS_ORDS_LOW.append(ord(i.lower()))

    # Score manager initialisation.
    score_man = score_manager()

    # Check for terminal colour support.
    colour_supported = curses.has_colors()
    if colour_supported:
        # Initialise colours. Foregroudn and background are same on "blocks"/grid cells.
        # (Source: https://repl.it/talk/learn/Game-Tutorial-Space-Invaders/9550)
        curses.init_pair(1, curses.COLOR_RED,     curses.COLOR_RED)
        curses.init_pair(2, curses.COLOR_BLUE,    curses.COLOR_BLUE)
        curses.init_pair(3, curses.COLOR_GREEN,   curses.COLOR_GREEN)
        curses.init_pair(4, curses.COLOR_MAGENTA, curses.COLOR_MAGENTA)
        curses.init_pair(5, curses.COLOR_CYAN,    curses.COLOR_CYAN)
        curses.init_pair(6, curses.COLOR_YELLOW,  curses.COLOR_YELLOW)
        curses.init_pair(7, curses.COLOR_WHITE,   curses.COLOR_WHITE)
        curses.init_pair(8, curses.COLOR_BLACK,   curses.COLOR_BLACK)
        # Gameover screen colour pair
        curses.init_pair(9, curses.COLOR_RED,     curses.COLOR_WHITE)
        # Header attribute
        curses.init_pair(10, curses.COLOR_MAGENTA,curses.COLOR_BLACK)
        # Misc
        curses.init_pair(11, curses.COLOR_RED,    curses.COLOR_BLACK)
        # Tooltips
        curses.init_pair(12, curses.COLOR_YELLOW, curses.COLOR_BLACK)

        # Reinitialise these "constants", (can't use color_pair
        #    until initscr gets called...)
        global GRIDATTR_EMPTY
        global GRIDATTR_HEAD
        global GRIDATTR_TAIL
        global GRIDATTR_APPL
        global GRIDATTR_COLL
        global STRATTR_GAMEOVER
        global STRATTR_HEADER
        global STRATTR_MISC
        global STRATTR_TOOLTIP
        GRIDATTR_EMPTY = curses.color_pair(7) # Set bg to white.
        GRIDATTR_HEAD  = curses.color_pair(3) # Set head to green.
        GRIDATTR_TAIL  = curses.color_pair(3) # Set tail to green.
        GRIDATTR_APPL  = curses.color_pair(5) # Set apples to cyan.
        GRIDATTR_COLL  = curses.color_pair(1) # Set collisions to red.
        STRATTR_GAMEOVER = curses.color_pair(9) # Set gameover screen to red+white.
        STRATTR_HEADER = curses.color_pair(10)
        STRATTR_MISC = curses.color_pair(11)
        STRATTR_TOOLTIP = curses.color_pair(12)


# Adds a centred string to the curses TUI.
# Pass an integer as ypos to adjust the y offset.
# Pass string attributes into optional attr parameter.
def addstr_centred(ypos, data, attr=0):
    # Compute x-pos by getting total width and subtracting
    #   half of the string's length.
    xpos = int((int(scrdims[1]) - int(len(data))) / 2)
    if attr != 0:
        wnd.addstr(ypos, xpos, data, attr)
    else:
        wnd.addstr(ypos, xpos, data)

# Wraps position between the grid bounds
# vinp -> vector input
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
# v1 -> First vector input, v2 -> Second vector input.
def add_vectors(v1, v2):
    return [v1[0] + v2[0], v1[1] + v2[1]]

# Adds a node to the tail.
def add_tail_node():
    global player_tail
    player_tail.append(player_tail[len(player_tail) - 1])

# Randomises the spawn time offset parameter
def shuffle_spawntime_offset():
    global apple_spawntime_offset
    apple_spawntime_offset = random.randrange(-APPLE_SPAWN_DEVIATION, APPLE_SPAWN_DEVIATION)

# Returns whether the given key is the return key.
def is_return_key(k):
    return k == curses.KEY_ENTER or k == 0x0A or k == 0x0D

# Switch the screen to s
def change_screen(s):
    global cur_screen
    global wnd
    global hsscr_ltr_idx
    global hsscr_name
    global sel_idx

    # Change screen and set button index to zero.
    cur_screen = s
    sel_idx = 0

    # Set the game to have game speed.
    if cur_screen == SCREEN_GAME:
        wnd.timeout(game_speed)
    else:
        wnd.timeout(BASE_DELAY)

    # Hi-score screen needs hsscr_ltr_idx set to zero.
    if cur_screen == SCREEN_NEWHIGHEST:
        hsscr_ltr_idx = 0
        hsscr_name = ["A"] * HISCORE_NAME_LEN

# Clamps a to b and c.
def clamp(a, b, c):
    if a < b:
        return b
    if a > c:
        return c
    return a

# Called whenever an apple is collected.
def on_apple_collect():
    global game_score
    global game_speed

    # Increment score
    game_score += SCORE_INCREMENT

    # Add a new tail node
    add_tail_node()

    # Adjust game speed.
    game_speed = int(round(clamp(BASE_DELAY / math.sqrt(game_score), MINIMUM_DELAY, BASE_DELAY)))
    wnd.timeout(game_speed)

# Loop method for the main menu
def game_loop_menu():
    # Global variable usage
    global sel_idx
    global cur_screen

    # Draw header.
    addstr_centred(1, " -- SNAKE GAME -- ", STRATTR_HEADER)
    addstr_centred(3, "Written by Michael for ICT CAT", curses.color_pair(11))
    addstr_centred(4, "(Use arrow keys to navigate.)")

    # Draw buttons
    btn_attrs = [0, 0, 0]
    btn_attrs[sel_idx] = curses.A_STANDOUT
    addstr_centred(6, "Play game", btn_attrs[BTNID_MENU_PLAY])
    addstr_centred(7, "Rankings", btn_attrs[BTNID_MENU_SCORES])
    addstr_centred(8, "Quit", btn_attrs[BTNID_MENU_QUIT])

    # Draw the tooltip.
    addstr_centred(10, BTNDESC_MENU[sel_idx], STRATTR_TOOLTIP)

    # Get and check input.
    key = wnd.getch()
    if key == curses.KEY_UP:
        # Key up, decrement selected button index. 
        sel_idx = sel_idx - 1
    elif key == curses.KEY_DOWN:
        # Key down, increment selection
        sel_idx = sel_idx + 1
    elif is_return_key(key):
        # Return key pressed, check what was pressed. (Checks for both CR and LF ASCII codes just in case.)
        if sel_idx == BTNID_MENU_PLAY:
            # Play button, switch to game screen.
            change_screen(SCREEN_GAME)
        elif sel_idx == BTNID_MENU_SCORES:
            change_screen(SCREEN_RANKINGS)
        elif sel_idx == BTNID_MENU_QUIT:
            # Quit the game
            change_screen(SCREEN_NONE)
    
    # Wrap selection around from 0 to 2
    sel_idx %= len(btn_attrs)

# Loop method for the game itself.
def game_loop_main():
    global cur_screen
    global wnd
    global game_grid
    global player_pos_head
    global player_velo
    global player_tail
    global game_ticks
    global game_score
    global game_over

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

    # Set tail cells.
    for i in player_tail:
        game_grid[i[IDX_Y] * GAME_WIDTH + i[IDX_X]] = GRIDID_TAIL

    # Set apple cells
    for i in game_apples:
        game_grid[i[IDX_Y] * GAME_WIDTH + i[IDX_X]] = GRIDID_APPL

    # Check if player is colliding with an apple.
    if player_pos_head in game_apples:
        game_apples.remove(player_pos_head)
        on_apple_collect()

    # Set head cell. Is after player apple cell setting so that it overwrites.
    game_grid[player_pos_head[IDX_Y] * GAME_WIDTH + player_pos_head[IDX_X]] = GRIDID_HEAD

    # Check if player is colliding with their tail
    if player_pos_head in player_tail:
        # Set cell to show the collision point.
        game_grid[player_pos_head[IDX_Y] * GAME_WIDTH + player_pos_head[IDX_X]] = GRIDID_COLLIDE

        game_over = True

    # Draw the game
    for y in range(0, GAME_HEIGHT):
        for x_real in range(0, GAME_WIDTH):
            cell = game_grid[y * GAME_WIDTH + x_real]

            # Change colour based on cell.
            # This 'x' is multiplied by two to stretch the TUI a bit horizontally.
            x = x_real * 2
            if cell == GRIDID_EMPTY:
                # Empty cell.
                wnd.addstr(y, x, ". ", GRIDATTR_EMPTY)
                #wnd.addstr(y, x, "." if x % 2 == 0 else " ", GRIDATTR_EMPTY)
            elif cell == GRIDID_HEAD:
                # Head cell.
                wnd.addstr(y, x, GRIDCHR_HEAD, GRIDATTR_HEAD)
            elif cell == GRIDID_TAIL:
                # Tail cell.
                wnd.addstr(y, x, GRIDCHR_TAIL, GRIDATTR_TAIL)
            elif cell == GRIDID_APPL:
                # Apple cell
                wnd.addstr(y, x, GRIDCHR_APPL, GRIDATTR_APPL)
            elif cell == GRIDID_COLLIDE:
                # Collided cell
                wnd.addstr(y, x, GRIDCHR_COLL, GRIDATTR_COLL)

    # Draw the score
    wnd.addstr(GAME_HEIGHT + 1, 1, "SCORE:    {:04d}".format(game_score))
    wnd.addstr(GAME_HEIGHT + 2, 1, "HI-SCORE: {:04d}".format(score_man.hiscore()) + ", '" + score_man.hiscore_holder() + "'")
    wnd.addstr(GAME_HEIGHT + 4, 1, "Press 'p' to pause the game.")

    # Get and check input.
    key = wnd.getch()
    if key == ord("p") or key == ord("P"):
        change_screen(SCREEN_PAUSE)
    elif key == curses.KEY_UP:
        player_velo = [-1, 0]
    elif key == curses.KEY_DOWN:
        player_velo = [1, 0]
    elif key == curses.KEY_LEFT:
        player_velo = [0, -1]
    elif key == curses.KEY_RIGHT:
        player_velo = [0, 1]
    
    # Force the delay
    if key != curses.ERR:
        # Sleep how ever long the game is taking,
        # then flush the input buffer to prevent
        # weird getch() call delays.
        curses.napms(game_speed)
        curses.flushinp()

    # Update game timer
    # TODO: Use delta timing to keep this consistent.
    game_ticks += 1 # 1.0 / BASE_DELAY

    # Check if it's a good time to spawn an apple
    if len(game_apples) < MAX_APPLES and (game_ticks + apple_spawntime_offset) % 10 == 0:
        # Generate a y and x that's not in the player and not already in list.
        y = -1
        x = -1

        # So Python doesn't have do-while loops - very convenient...
        while True:
            x = random.randrange(0, GAME_WIDTH)
            y = random.randrange(0, GAME_HEIGHT)
            node = [y, x]
            if not (node in player_tail or node == player_pos_head or node in game_apples):
                break

        # Add the apple to the apple list.
        game_apples.append([y, x])

        # Randomise next apple spawn time offset
        shuffle_spawntime_offset()

    # Game over show the "Press any key to continue screen".
    if game_over:
        # Calculate x position to move it to centre of screen.
        str0 = "Game over"
        str1 = "Press RETURN to continue..."
        posx0 = int((int(GAME_WIDTH * 2) - int(len(str0))) / 2)
        posx1 = int((int(GAME_WIDTH * 2) - int(len(str1))) / 2)
        wnd.addstr(1, posx0, str0, STRATTR_GAMEOVER)
        wnd.addstr(2, posx1, str1, STRATTR_GAMEOVER)

        # Wait until user presses RETURN.
        wnd.timeout(-1)
        k = curses.ERR
        while not is_return_key(k):
            k = wnd.getch()

        # Reset game and goto menu.
        if game_score > score_man.hiscore():
            # New highest score.
            change_screen(SCREEN_NEWHIGHEST)
        else:
            # Reset game and goto menu.
            game_reset()
            change_screen(SCREEN_GAME)

# Loop method for the pause menu.
def game_loop_pause():
    # Global variable usage
    global sel_idx
    global cur_screen

    # Draw header.
    addstr_centred(1, " -- PAUSED -- ", STRATTR_HEADER)

    # Draw buttons
    btn_attrs = [0, 0]
    btn_attrs[sel_idx] = curses.A_STANDOUT
    addstr_centred(3, "Resume", btn_attrs[BTNID_PAUSE_RESUME])
    addstr_centred(4, "Goto Menu", btn_attrs[BTNID_PAUSE_GOTOMENU])

    # Draw tooltip
    addstr_centred(6, BTNDESC_PAUSE[sel_idx], STRATTR_TOOLTIP)

    # Get and check input.
    # (Very similar to menu's stuff, may need to make a method...)
    key = wnd.getch()
    if key == curses.KEY_UP:
        # Key up, decrement selected button index. 
        sel_idx = sel_idx - 1
    elif key == curses.KEY_DOWN:
        # Key down, increment selection
        sel_idx = sel_idx + 1
    elif is_return_key(key):
        # Return key pressed, check what was pressed. (Checks for both CR and LF ASCII codes just in case.)
        if sel_idx == BTNID_PAUSE_RESUME:
            # Play button, switch to game screen.
            change_screen(SCREEN_GAME)
        elif sel_idx == BTNID_PAUSE_GOTOMENU:
            # Quit to menu.
            change_screen(SCREEN_MENU)
            sel_idx = 0

            # Reset game.
            game_reset()
    
    # Wrap selection around from 0 to 1
    sel_idx %= 2

# Draw 'num' amount of scores on the screen at y offset.
def draw_scores(offset, num):
    # Check if scores exist.
    if len(score_man.score_list) == 0:
        addstr_centred(offset, "No records yet...")
        return

    # Draw header.
    addstr_centred(offset, "RANK NAME SCORE     TIME          ")
    rank = 0
    # Iterate through first 10 hi-scores.
    for i in score_man.score_list[0:min(num, len(score_man.score_list))]:
        n = i["name"]
        s = i["score"]
        d = i["date_str"]
        t = i["time_str"]
        addstr_centred(offset + rank + 1, "{}.   {}  {:04d}  {}, {}".format(rank, n, s, d, t))
        rank += 1

# Loop method for the highest-score screen.
def game_loop_hiscore_screen():
    global hsscr_ltr_idx
    global hsscr_name
    global hsscr_name_indices

    # Draw the main text.
    addstr_centred(1, " -- NEW HI-SCORE: {} -- ".format(game_score), STRATTR_HEADER)
    addstr_centred(2, "Enter {}-digit alphanumeric name below:".format(HISCORE_NAME_LEN))

    # Draw the input area
    xpos = int((int(scrdims[1]) - HISCORE_NAME_LEN) / 2)
    wnd.addstr(3, xpos, "".join(hsscr_name))
    wnd.addstr(3, xpos + hsscr_ltr_idx, hsscr_name[hsscr_ltr_idx], curses.A_STANDOUT)

    # Draw the hi-scores.
    addstr_centred(5, "-- RANKINGS --", STRATTR_HEADER)
    draw_scores(7, 10)
    

    # Used in key up/down events. a is either +1 or -1 depending on increment/decrement respectively.
    l_get_char = lambda a : (hsscr_name_indices[hsscr_ltr_idx] + a) % len(HISCORE_VALIDCHARS)
    # Just another shorthand
    l_set_char = lambda : HISCORE_VALIDCHARS[hsscr_name_indices[hsscr_ltr_idx]]
    # Shorthand for increment
    l_incr     = lambda a : (hsscr_ltr_idx + a) % HISCORE_NAME_LEN

    # Get input.
    key = wnd.getch()
    if is_return_key(key):
        # Increase letter index if not last letter.
        if hsscr_ltr_idx < HISCORE_NAME_LEN - 1:
            hsscr_ltr_idx += 1
        else:
            # User is on last letter - switch screens.

            # Add the score to the score manager's list.
            score_man.add_score("".join(hsscr_name), game_score)

            # Reset game and change screens.
            game_reset()
            change_screen(SCREEN_MENU)
    elif key == curses.KEY_UP:
        # Key up, increase letter index.
        hsscr_name_indices[hsscr_ltr_idx] = l_get_char(1)
        hsscr_name[hsscr_ltr_idx] = l_set_char()
    elif key == curses.KEY_DOWN:
        # Key down, decrease letter index.
        hsscr_name_indices[hsscr_ltr_idx] = l_get_char(-1)
        hsscr_name[hsscr_ltr_idx] = l_set_char()
    elif key == curses.KEY_LEFT or key == curses.KEY_BACKSPACE:
        # Decrement letter idx.
        hsscr_ltr_idx = l_incr(-1)
    elif key == curses.KEY_RIGHT:
        hsscr_ltr_idx = l_incr(1)
    elif key in HISCORE_VALIDCHARS_ORDS_LOW or key in HISCORE_VALIDCHARS_ORDS_UP:
        # Key is valid already, just add it to the string..
        hsscr_name[hsscr_ltr_idx] = chr(key).upper()
        if hsscr_ltr_idx < HISCORE_NAME_LEN - 1:
            hsscr_ltr_idx = l_incr(1)

# Loop for the rankings screen.
def game_loop_rankings():
    # Draw all the text. Back btn attribute is always.
    addstr_centred(1, "-- RANKINGS --", STRATTR_HEADER)
    addstr_centred(3, "Press RETURN to go back", curses.A_STANDOUT)
    draw_scores(5, 10)

    # Wait for return key input.
    key = wnd.getch()
    if is_return_key(key):
        change_screen(SCREEN_MENU)

# The main game loop.
def game_loop():
    global game_speed
    global cur_screen
    global wnd

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
    elif cur_screen == SCREEN_NEWHIGHEST:
        # -- Draw the highest score screen. --
        game_loop_hiscore_screen()
    elif cur_screen == SCREEN_RANKINGS:
        # -- Draw the rankings screen. --
        game_loop_rankings()
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

    game_deinitialise()

# Call the main method in a curses TUI wrapper object.
# This allows for cleaner error handling...
wrapper(main)