"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("This is a really long paragraph to describe the problem. I "
                   "could include generic lorem ipsum, but why make it easy? Sc"
                   "rew Dolores and her est! ...I'm just kidding, of course. Is"
                   " this over eighty characters yet? Man I really hope so.", 0)
    
    # In this generic template, we're just going to parrot the input file.
    for i in input:
        print(i)


