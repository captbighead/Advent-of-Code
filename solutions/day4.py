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
        """ Finds if two doubles intersect, and classifies them with an int.

        The output is 0 when there is no overlap, 1 when there's partial overlap
        and 2 when it's fully overlapped. 
        """
        # Overarching strategy, inspired by the SQL Gaps/Islands solution: put
        # all values from both doubles into an ordered list, and compare the 
        # tuples to the meta-information gleaned by that list.
        all = [s1[0],s1[1],s2[0],s2[1]] 
        all = sorted(all)

        # If either tuple matches a tuple made from the edges of the list, that
        # tuple fully encloses the other. 
        if s1 == (all[0], all[3]) or s2 == (all[0], all[3]):
            return 2
        # If either tuple occupies two non-adjacent spaces in the quadruple, 
        # then that tuple starts or ends between the values of the other. 
        if s1 == (all[0], all[2]) or s2 == (all[0], all[2]):
            return 1
        # If it hasn't returned already there's no overlap
        return 0

        
    au.printBanner("PART ONE - CAMP CLEANUP: The elves have sectored off parts "
                   "of the camp for cleaning, but they didn't do it very effici"
                   "ently. For the first part of this problem, we need to find "
                   "the elves whose assignments fully overlap with their partne"
                   "r elf's assignment (IE: If one elf is cleaning up sectors 1"
                   " through 4, and their partner is cleaning 2 through 3, then"
                   " both elves have been assigned to sectors 2 and 3, and sinc"
                   "e the latter elf's whole assignment is those two sectors, h"
                   "is assignment fully overlaps with his buddy's).", 4)

    # Spoiler alert: Part Two is going to ask for partial overlaps. 
    fully = 0
    partial = 0
    for s in sectors:
        s1 = tuple(int(a) for a in s.split(",")[0].split("-"))
        s2 = tuple(int(a) for a in s.split(",")[1].split("-"))
        overlap_index = sectorOverlap(s1,s2)
        if overlap_index == 2:
            fully += 1
        if overlap_index > 0:   # Fun fact, I forgot partials included fulls
            partial += 1        # in the first draft!

    print(f"The number of sections that fully overlapped was {fully}.")

    au.printBanner("PART TWO - ANY OVERLAP: The more general case would be to d"
                   "etermine if the pairs assignments have any overlap at all. "
                   "Find out that number (remember that the previous counted pa"
                   "irs are a subset of this set of counted pairs!)")

    print(f"The number of sections that partially overlapped was {partial}.")

