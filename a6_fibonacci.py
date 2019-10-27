# -- -- -- -- -- -- -- -- -- -- -- -- --
# ICT CAT Term 4, 2019
# Category A - Problem 6: Fibonacci Sum (Difficulty: ****)
# https://github.com/mikejzx/py-ictcat
#
# -- -- -- -- -- -- -- -- -- -- -- -- --
# Each new term in the Fibonacci sequence 
# is generated by adding the previous two 
# terms. By starting with 1 and 2, the 
# first 10 terms will be: 
# (0, 1) 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, ... 
# Create a program to find the sum of all 
# the even terms in the Fibonacci sequence 
# below twenty million. 
# -- -- -- -- -- -- -- -- -- -- -- -- --

# Constants
MAXIMUM = 20000000

# Main variables.
prev0 = 1 # The previous number.
prev1 = 0 # The number before the previous.
cur = 1   # The current number.
sum = 0   # The total summed.
term_count = 0 # Number of terms used in sum.

# Repeat until we reach the maximum number.
while cur < MAXIMUM:
    # Some Fibonacci computing...
    cur = prev0 + prev1
    prev1 = prev0
    prev0 = cur

    # Add even values
    if cur % 2 == 0 and cur < MAXIMUM:
        sum += cur
        term_count += 1

# Print the sum. {:,} format puts commas between thousands.
print("Sum of all Fibonacci numbers under {:,}:\n{:,} ({:,} terms.)".format(MAXIMUM, sum, term_count))