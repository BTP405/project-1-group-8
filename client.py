"""
Write a program to count the number of vowels in a string.
"""

vowels = ['a','i','u','e','o']
mystring = "big boy bonglous"
counter = 0

for x in mystring:
    if x in vowels:
        counter+=1

print("ur strring got this many vowels: ", counter)