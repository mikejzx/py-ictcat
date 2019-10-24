# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category A - Problem 12: Pig Latin (Difficulty: ***)
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# Write a program that translates a text 
# to Pig Latin and back. English is 
# translated to Pig Latin by taking the 
# first letter of every word, moving it 
# to the end of the word and adding ‘ay’. 
# “The quick brown fox” 
# becomes 
# “Hetay uickqay rownbay oxfay”.
# -- -- -- -- -- -- -- -- -- -- -- -- --

ALPHABET = "abcdefghijklmnopqrstuvwxyz0123456789"

# Translates an English string of text to
# 'Pig Latin'.
def string_to_piglatin(data):
    # First we find all the words in the string seperated 
    #    by anything except a letter.
    words = []
    output = ""
    last_idx = 0
    idx = 0
    for char in data:
        char_low = char.lower()
        # Whether we are at the end of string
        eos = idx == len(data) - 1
        # If the character isn't a letter, we assume it is a word 
        if char_low not in ALPHABET or eos:
            # End of string we add 1 to the substring end.
            # and remove the char_low appended to end of the string.
            idx_add = 0
            if eos:
                idx_add = 1
                char_low = ""

            # Get the original word from the substring
            word_original = data[last_idx:idx + idx_add]

            # Special case for one-letter words.
            word_len = len(word_original)
            if word_len == 0:
                output += char_low
                idx += 1
                last_idx = idx
                continue
            if word_len == 1:
                uppercase = word_original[0].isupper()
                output += word_original + ("AY" if uppercase else "ay") + char_low

                # Need to update indices.
                last_idx = idx + 1
                idx += 1
                continue

            # The new beginning character's case changes based on the old one.
            char_beg_final = word_original[1]
            if word_original[0].isupper():
                char_beg_final = char_beg_final.upper()
            else:
                char_beg_final = char_beg_final.lower()

            # The new ending character's case depends on the previous letter's.
            char_end_final = word_original[0]
            if word_original[len(word_original) - 1].isupper():
                char_end_final = char_end_final.upper() + "AY"
            else:
                char_end_final = char_end_final.lower() + "ay"

            # The final pig-latin word.
            word_final = char_beg_final + word_original[2:len(word_original)] + char_end_final
            output += word_final + char_low

            # Update index.
            last_idx = idx + 1
        idx += 1
    # Return the translated string.
    return output

print(string_to_piglatin(input("Enter the text you wish to translate into Pig Latin:\n")))