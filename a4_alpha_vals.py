# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category A - Problem 4: Alphabet Values (Difficulty: ****)
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# If A = 1, B = 2, C = 3, and so on, we 
# can find the number value of a word. For 
# example “ROBOT” = 18 + 15 + 2 + 15 + 20 = 70. 
# Write a program that prints the number value 
# of an input word. (Hint: ord('A'.lower())-96 = 1).
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Constants
VALID_CHARS = "abcdefghijklmnopqrstuvwxyz"

# Get x's position in the alphabet from 1-26.
def get_alphabet_pos(x):
    # Bit-masking an ASCII value with 0x1F gives us
    # Only the bits we are interested in.
    # In binary it appears: 0001 1111
    # Bit-wise operations are faster to run on 
    # CPU than a subtraction. (Or should be at least...)
    return ord(x) & 0x1F

# Get the alphabet position sum of each character in data.
def get_word_value(data):
    # Compute the sum.
    sum = 0
    for i in data:
        # Check that this letter is in the alphabet.
        if i not in VALID_CHARS:
            # If not, just skip this iteration.
            continue

        # Get the number at this position and add to sum.
        sum += get_alphabet_pos(i)
    return sum

# Get input, compute sum, and print.
print("-- Alphabet Values --")
while True:
    print("Value: ", get_word_value(input("Enter a string you wish to get the value of.\n").lower()))