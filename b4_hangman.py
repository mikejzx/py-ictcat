# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category B - Problem 4: Hangman
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# This is a simple Hangman game designed
# for use in the terminal. The user
# can input either a letter, or guess
# an the entire word.
# The word given is (by default) retrieved
# from an online word list. Alternatively,
# the user can pass in a custom word list
# as the first command-line argument.
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# This specific program uses a word list
#    from the following GitHub repository:
# https://github.com/first20hours/google-10000-english/blob/master/
# And this specific file:
# https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Imports
import sys    # For command-line arguments vector. (sys.argv)
import random # For rand
from urllib.request import urlopen # Used to download word list.

# Global variables.
wordlist_local    = False # Flag of whether the user passed a custom word list.
wordlist_file_url = "https://raw.githubusercontent.com/first20hours/google-10000-english/master/google-10000-english-no-swears.txt"
wordlist_data     = []
word_selected     = ""

# Constants
HEALTH_DECREMENT  = 100.0 / 8.0 # We allow 8 mistakes.

# Downloads the word list.
# * wordlist_dl_url -> A string containing the URL of the wordlist file.
def wordlist_download(wordlist_dl_url):
    # urlopen will download the file from the URL.
    wordlist_file = urlopen(wordlist_dl_url)

    # Add each line to the wordlist list.
    for line in wordlist_file:
        # We need to strip first 2 characters, and last three, as the
        # file's lines are in the form: b'<WORD HERE>\n'
        wordlist_data.append(str(line)[2:-3]) 

# Read a local wordlist file.
# * wordlist_file_path -> The path of the file to read.
def wordlist_readlocal(wordlist_file_path):
    # Read the local file given the path.
    wordlist_file = open(wordlist_file_path, "rt")

    # Add each line to the wordlist list.
    for line in wordlist_file:
        wordlist_data.append(str(line).strip("\n"))

# Select a random word from the word list.
def word_rand_select():
    # We try 15 times until we get a word long enough.
    for i in range(0, 15):
        # Generate a random index between zero and wordlist size.
        w = wordlist_data[random.randrange(0, len(wordlist_data))]

        # Check if length is less than 3. If it is, try again.
        if len(w) < 3:
            continue
            
        # Else just return our word.
        return w.lower()

# The main method. This is called once when the program is executed.
# * args -> The command-line arguments passed into the program 
def main_func(args):
    print("-- -- Hangman -- --")

    # First we retrieve a word list.
    wordlist_local = len(args) > 1
    if not wordlist_local:
        print("  (Downloading word list, please wait...)")

        # Download the word list.
        wordlist_download(wordlist_file_url)
        wordlist_local = False
    else:
        print("  (Using local word list.)")

        # Read a local file.
        wordlist_readlocal(args[1])
        wordlist_local = True

    # Main game loop. Run every single round.
    round_idx = 0
    while True:
        print("\n-- -- Hangman Round", round_idx, "-- --")

        # Select a random word.
        word_selected = word_rand_select()
        print("The computer has chosen a word. Type a letter you think is in the word.")

        # Set the guessed word to blanks.
        word_totalguessed = ["_"] * len(word_selected)

        # All letters that are not in the word.
        word_excludes = []

        # User's health
        health = 100

        # Check if the "guessed" string contains an underscore. If it
        #   doesn't then the user found all the letters.
        # If it does then the user still has letters to find so we keep running.
        lost = False
        while "_" in word_totalguessed:
            print("  [Found] :", "".join(word_totalguessed))
            if len(word_excludes) > 0:
                print("  [Doesn't contain]: " + ", ".join(word_excludes))
            print("  [Health]:", health)

            # Get the user's input.
            inp_string = str(input())
            while len(inp_string) < 1:
                inp_string = str(input("Enter a letter.\n"))
            # Check if user guessed entire word correctly.
            if inp_string == word_totalguessed:
                lost = False
                break;
            # We will just use the first char.
            char_guessed = inp_string.lower()[0]

            # Whether the letter is in the word.
            ltr_in_word = char_guessed in word_selected  
            if ltr_in_word:
                # Iterate over the word, and replace the "guessed" 
                #   string's underscores with the letter.
                ltr_idx = -1
                for ltr in word_selected:
                    ltr_idx += 1
                    if not ltr == char_guessed:
                        # Not this letter, skip to next iteration.
                        continue
                    # Set the guessed string at this index to this letter.
                    word_totalguessed[ltr_idx] = char_guessed
            else:
                # Add to known letters that aren't in the word.
                if not char_guessed in word_excludes:
                    word_excludes.append(char_guessed)
                
                # Decrement health.
                health -= HEALTH_DECREMENT
                if health <= 0:
                    lost = True
                    break
        if not lost:
            print("Congratulations, you guessed all letters of the word '" + word_selected + "' with ", health, "% health remaining.")
        else:
            print("You lose. The word was '" + word_selected + "'.")

        # Ask user what to do next.
        # 's' is the message to show - it is only shown once.
        # 'exit_flag' determines whether the program will exit or not.
        s = "Type 'p' to play again, 'x' to exit.\n"
        exit_flag = False
        while True:
            exitcode = input(s)[0]
            s = ""
            if exitcode == 'x':
                return;
            if exitcode == 'p':
                break
            print("Invalid response.")

        # Update round counter.
        round_idx += 1


# Call the main method
main_func(sys.argv)