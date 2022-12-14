"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)

    #input = ["nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"]   # Result: 10
    #input = ["nppdvjthqldpwncqszvftbrmjlhg"]        # Result: 6
    #input = ["bvwbjplbgvbhsrlpgdmjqwftvncz"]        # Result: 5
    #input = ["mjqjpqmgbljsphdztnvjfqwrcgsmlb"]      # Result: 7

    au.printBanner("PART ONE - TUNING TROUBLE: We've finally left the camp! Now"
                   " that we're on the road, we need to be able to communicate "
                   "if (Spoilers: when) things go wrong. To tune our device, we"
                   " need to interpret the input stream and find the first char"
                   "acter recieved such that occurs where it and the preceding "
                   "three characters are all distinct from each other.", 6)
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

    au.printBanner("PART TWO - PART ONE, BUT MORE: Whoopsie! The character we n"
                   "eed to find is the one after it and the previous *13* chara"
                   "cters are distinct from each other. Do it again, but + 10")

    n += 10
    answer = findFirstNDistinct(input, n)
    print(f"After character {answer}, we've found the code: "
          f"{input[answer-n:answer]}")