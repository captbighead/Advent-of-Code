"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    sacks = au.inputFileAsStrings(inputName)
    sacks_ex = ["vJrwpWtwJgWrhcsFMMfFFhFp","jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL",
                "PmmdzqPrVvPwwTWBwg","wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn",
                "ttgJtRGJQctTZtZT","CrZsJsPPZsGzwwsLwLmpwMDw"]
    #sacks = sacks_ex

    au.printBanner("PART ONE - RUCKSACK REORGANIZATION: The elves rucksacks hav"
                   "e been packed incorrectly, and now we need to reorganize it"
                   " for them. For part one, we need to find the items that app"
                   "ear in both compartments of their rucksacks, and then find "
                   "their priority. And then somehow, giving the sum of those p"
                   "riorities is helpful.", 3)

    sumPriority = 0
    for s in sacks:
        sL = s[:len(s)//2]
        sR = s[len(s)//2:]
        for char in sL:
            if sR.find(char) >= 0:  # Save on writing a loop, use a str method
                # Below: a in ASCII is 97, so to make it 1, we subtract 96.
                # Similarly, A is 65, so we subtract 38 to get 27
                sumPriority += ord(char) - (96 if char.islower() else 38)
                break

    print(f"The priority of the items the elves need to shuffle in their own ba"
          f"gs is {sumPriority}.")

    au.printBanner("PART TWO - FIND THE BADGES: The elves need to find their gr"
                   "oup's safety badges. Amongst every group of three consecuti"
                   "ve bags, there's an identical item that the three share. Th"
                   "at item is the badge for that group. Find the sum of all of"
                   " the badges' priorities.")

    sumPriority = 0
    for i in range(0,len(sacks),3):
        lCommon = min(len(sacks[i]), len(sacks[i+1]), len(sacks[i+2]))
        for l in range(lCommon):
            if sacks[i][l] in sacks[i+1] and sacks[i][l] in sacks[i+2]:
                char = sacks[i][l]
                sumPriority += ord(char) - (96 if char.islower() else 38)
                break

    print(f"The priority of the elves' badges is {sumPriority}.")



