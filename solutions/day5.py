"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = []
    with open(inputName) as f:
        input = [line[:-1] for line in f]
    #input = ["    [D]     ",
    #         "[N] [C]     ",
    #         "[Z] [M] [P] ",
    #         " 1   2   3        ","","move 1 from 2 to 1",
    #         "move 3 from 1 to 3","move 2 from 2 to 1","move 1 from 1 to 2"]


    au.printBanner("PART ONE - SUPPLY STACKS: Stacks of crates within the camp "
                   "need to be reorganized according to a list of instructions "
                   "from the elves. Follow those instructions and then output t"
                   "he ids of the crates at the top of each stack.", 5)
    
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

    au.printBanner("PART TWO - EFFICIENCY: In the previous reorganization we ha"
                   "d to move a single crate at a time, inverting the order of "
                   "the moved crates in each operation. For part two, we found "
                   "a new mode for the crane that could pick up multiple cranes"
                   " at once, preserving their order. Following the same set of"
                   " instructions on the same starting set of crates, output th"
                   "e tops of the stacks now, after moving all of them at once."
                   "")    


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