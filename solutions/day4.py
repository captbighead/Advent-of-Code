"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    sectors = au.inputFileAsStrings(inputName)
    sectors_ex = ["2-4,6-8","2-3,4-5","5-7,7-9","2-8,3-7","6-6,4-6","2-6,4-8"]
    #sectors = sectors_ex

    def sectorOverlap(s1, s2):
        all = [s1[0],s1[1],s2[0],s2[1]]
        all = sorted(all)

        if s1 == (5,7) or s2 == (5,7):
            print()

        # This would be true if s1 fully enveloped s2 or vice versa
        if s1 == (all[0], all[3]) or s2 == (all[0], all[3]):
            return 2
        # If this is true, one starts in the other
        if s1 == (all[0], all[2]) or s2 == (all[0], all[2]):
            return 1
        # If it hasn't returned already there's no overlap
        return 0

        

    au.printBanner("PART ONE - CAMP CLEANUP", 4)
    fully = 0
    partial = 0
    for s in sectors:
        s1 = tuple(int(a) for a in s.split(",")[0].split("-"))
        s2 = tuple(int(a) for a in s.split(",")[1].split("-"))
        overlap_index = sectorOverlap(s1,s2)
        if overlap_index == 2:
            fully += 1
        if overlap_index > 0:
            partial += 1

    print(f"The number of sections that fully overlapped was {fully}.")

    au.printBanner("PART TWO - ANY OVERLAP")

    print(f"The number of sections that partially overlapped was {partial}.")

