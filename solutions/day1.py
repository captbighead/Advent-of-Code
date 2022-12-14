"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)

    au.printBanner("PART ONE - CALORIE COUNTING: 2022's Advent of Code takes us"
                   " on a hike through a vast jungle! Our first part of our fir"
                   "st day is all about rationing: we need to take a list of fo"
                   "ods (as their calorie counts) that each elf carries, and re"
                   "port on the total calories the elf with the most food (high"
                   "est sum calories) has.", 1)

    # Build a list (cargo) of the sum totals of what the elfs carry
    cargo = []
    elf_list = []
    for l in input:
        if l == "":
            cargo.append(sum(elf_list))
            elf_list = []
        else:
            elf_list.append(int(l))
    cargo = sorted(cargo)

    # Finding the max and output it. 
    print(f"The elf with the most calories was carrying {cargo[-1]} calories.")

    au.printBanner("PART TWO - CONTINGENCIES: The elves, in their foresight, re"
                   "alized that the top carrier may run out of snacks. To provi"
                   "de a contingency for such a horrible eventuality, they've n"
                   "ow asked for the calories amongst the top three carriers in"
                   "stead.")

    # It was already sorted! That was easy. 
    topThree = cargo[-1] + cargo[-2] + cargo[-3]
    print(f"The three elves with the most calories are carrying a total of "
          f"{topThree} calories.")

