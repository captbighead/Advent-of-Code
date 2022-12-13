"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)

    #input = ["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"]   # Result: 10
    #input = ["nppdvjthqldpwncqszvftbrmjlhg"]        # Result: 6
    #input = ["bvwbjplbgvbhsrlpgdmjqwftvncz"]        # Result: 5
    #input = ["mjqjpqmgbljsphdztnvjfqwrcgsmlb"]      # Result: 7

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - TUNING TROUBLE: <Find the first index in the str"
                   "ing where the preceding 4 characters are distinct>", 6)

    input = input[0]

    def findFirstNDistinct(word, n):
        for i in range(n-1, len(word)):
            s = word[i-(n-1):i+1]
            charSet = set((char for char in s))
            if len(charSet) == n:
                return i+1

    n = 4
    answer = findFirstNDistinct(input, n)
    print(f"After character {answer}, we've found the code: "
          f"{input[answer-n:answer]}")

    au.printBanner("PART TWO - BUT MORE: <Find the first index in the string wh"
                   "ere the preceding 14 characters are distinct>")

    n += 10
    answer = findFirstNDistinct(input, n)
    print(f"After character {answer}, we've found the code: "
          f"{input[answer-n:answer]}")