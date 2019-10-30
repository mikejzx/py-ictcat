# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category A - Problem 10: Caesar Cipher (Difficulty: ***)
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# This is a basic implementation of a 
# Caesar cipher.
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Encrypt the provided string by shifting
# all letters by the offset/key parameter.
def caesar_encrypt(data, key):
    output = ""
    for char in data:
        # Get ASCII value, subtract 0x41 or 0x61 depending on whether it is capital or lowercase.
        asc = ord(char)

        # Check whether it is lowercase by seeing if it is in range of the lowercase ASCII codes.
        lowercase = asc > 0x60 and asc < (0x61 + 26)
        uppercase = asc > 0x40 and asc < (0x41 + 26)

        # The character isn't in the alphabet, so we will just
        # append it as normal.
        if lowercase == False and uppercase == False:
            output += char
            continue;

        # Compute the new value
        v = 0x61 if lowercase else 0x41
        asc = ((asc - v + key) % 26) + v

        # Concatenate the new ASCII code.
        output += chr(asc)
    return output

# Decrypt the provided string by shifting the letters
# using the key in reverse.
def caesar_decrypt(data, key):
    return caesar_encrypt(data, -key)

print("-- -- Caesar Cipher -- --")

# Ask user for mode.
inp = input("Type 'e' for encryption, 'd' for decryption.\n")
while len(inp) < 1 or not (inp == "e" or inp == "d"):
    inp = input("Invalid input. (e)ncrypt or (d)ecrypt?\n");

# Ask client for data
encrypting = inp == "e"
action = "encrypt" if encrypting else "decrypt"
data = input("Enter the data you wish to " + action + ".\n")
while len(data) < 1:
    data = input("Please provide a string to " + action + "\n")

# Ask for key. Loop until valid input.
while True:
    try:
        key = int(input("Enter the cipher key. (must be signed integer)" + ".\n"))
    except:
        print("Invalid key provided. Must be a signed integer.\n")
        continue
    break

# Change process based on mode selected.
if encrypting:
    # Encrypt the string.
    print("Encrypted with key offset of", key)
    print("Encrypted string: ", caesar_encrypt(data, key))
else:
    # Decrypt the string.
    print("Decrypted with key offset of", key)
    print("Decrypted string: ", caesar_decrypt(data, key))