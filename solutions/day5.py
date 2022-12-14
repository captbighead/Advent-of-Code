"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = []
    with open(inputName) as f:
        input = [line[:-1] for line in f]
    #input = ["    [D]     ",
    #         "[N] [C]     ",
    #         "[Z] [M] [P] ",
    #         " 1   2   3        ","","move 1 from 2 to 1",
    #         "move 3 from 1 to 3","move 2 from 2 to 1","move 1 from 1 to 2"]


    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - SUPPLY STACKS: <Rearrange the original stacks an"
                   "d output the top barrels on each stack.>", 5)
    
    # Determined from Visual inspection:
    totalStacks = 9 
    #totalStacks = 3 

    # Build the stacks. They are sparse, but evenly spaced. 
    stacks = [[],[],[],[],[],[],[],[],[]]
    #stacks = [[],[],[]]
    instructions = []
    buildingStacks = True
    for l in input:
        if buildingStacks:
            if l.startswith(" 1 "):
                buildingStacks = False
                continue
            for i in range(totalStacks):
                thisCrate = l[i*4:i*4+4]
                if thisCrate[1] == " ":
                    continue
                else:
                    stacks[i].append(thisCrate[1])
        else:
            if l == "":
                continue
            l = l.replace("move ", "").replace(" fr", "").replace("m ", "")\
                .replace(" t", "").replace("o ", "o")
            instructions.append([int(n)-1 for n in l.split("o")])
            instructions[-1][0] += 1

    for stack in stacks:
        stack.reverse()

    # instructions are: num Move operations, source index in stacks, dest index
    # in stacks.
    for inst in instructions:
        numOps = inst[0]
        src = inst[1]
        dest = inst[2]
        for ops in range(numOps):
            stacks[dest].append(stacks[src].pop())

    print(f"The crates on the top of the stacks spell out: ", end="")
    for s in stacks:
        print(f"{s[-1]}", end="")
    print()

    au.printBanner("PART TWO - EFFICIENCY: <Rearrange the original stacks and o"
                   "utput the top barrels on each stack. You can move multiples"
                   " at once now>")    


    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = []
    with open(inputName) as f:
        input = [line[:-1] for line in f]
    #input = ["    [D]     ",
    #         "[N] [C]     ",
    #         "[Z] [M] [P] ",
    #         " 1   2   3        ","","move 1 from 2 to 1",
    #         "move 3 from 1 to 3","move 2 from 2 to 1","move 1 from 1 to 2"]
        
    # Determined from Visual inspection:
    totalStacks = 9 
    #totalStacks = 3 

    # Build the stacks. They are sparse, but evenly spaced. 
    stacks = [[],[],[],[],[],[],[],[],[]]
    #stacks = [[],[],[]]
    instructions = []
    buildingStacks = True
    for l in input:
        if buildingStacks:
            if l.startswith(" 1 "):
                buildingStacks = False
                continue
            for i in range(totalStacks):
                thisCrate = l[i*4:i*4+4]
                if thisCrate[1] == " ":
                    continue
                else:
                    stacks[i].append(thisCrate[1])
        else:
            if l == "":
                continue
            l = l.replace("move ", "").replace(" fr", "").replace("m ", "")\
                .replace(" t", "").replace("o ", "o")
            instructions.append([int(n)-1 for n in l.split("o")])
            instructions[-1][0] += 1

    for stack in stacks:
        stack.reverse()

    # instructions are: num Move operations, source index in stacks, dest index 
    # in stacks.
    for inst in instructions:
        numOps = inst[0]
        src = inst[1]
        dest = inst[2]
        moved = []
        for ops in range(numOps):
            moved.append(stacks[src].pop())
        moved.reverse()
        stacks[dest].extend(moved)

    print(f"The crates on the top of the stacks spell out: ", end="")
    for s in stacks:
        print(f"{s[-1]}", end="")
    print()