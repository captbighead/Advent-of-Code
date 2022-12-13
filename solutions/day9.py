"""
Solution Template for Advent of Code Solutions.
"""
import utilities.aoc_utils as au
import time
import os

def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    instrs = au.inputFileAsStrings(inputName)
    #instrs = ["R 4","U 4","L 3","D 1","R 4","D 1","L 5","R 2"]
    #instrs = ["R 5","U 8","L 8","D 3","R 17","D 10","L 25","U 20"]

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - ROPE BRIDGE: <Simulate a rope moving around and "
                   "report where the tail of the rope ended up.>", 9)
    
    uvs = au.unitVectors()
    dirMap = {"U":uvs[0], "R":uvs[1], "D":uvs[2], "L":uvs[3]}

    # In this generic template, we're just going to parrot the input file.
    directions = []
    for ln in instrs:
        hVec = dirMap[ln.split(" ")[0]]
        stps = int(ln.split(" ")[1])
        directions.append((hVec, stps))

    def needsToMove(tail, head):
        maxY = max(head[1], tail[1])
        minY = min(head[1], tail[1])
        maxX = max(head[0], tail[0])
        minX = min(head[0], tail[0])
        return maxY - minY > 1 or maxX - minX > 1



    head = (0,0)
    oldHead = head              
    tail = head              
    tailTracker = {(0,0):True}
    for d in directions:
        for step in range(d[1]):
            oldHead = head
            head = au.vectorAdd(head, d[0])
            if needsToMove(tail, head):
                # I tried to derive the calc for following, and while doing that
                # I realized that the position the tail ends up in is just the 
                # position the head used to be in
                tail = oldHead
                tailTracker[tail] = True

    print(f"The tail was in {len(tailTracker)} distinct positions.")

    au.printBanner(f"PART TWO - OKAY BUT WHAT IF A REAL ROPE THO: <Do it again "
                   "but with a longer rope.>")

    def whereToMove(tail, head):
        # A longer rope means that each knot no longer goes directly to the 
        # space the knot in front of it went. We need to be more robust. Darn.
        
        # Three Shapes: 
        # 
        # . . .    . . H    . . H 
        # T . H    T . .    . . . 
        # . . .    . . .    T . . 



        minX = min(tail[0], head[0])
        maxX = max(tail[0], head[0])
        minY = min(tail[1], head[1])
        maxY = max(tail[1], head[1])
        
        if maxX == minX + 2:
            newX = minX + 1
        elif maxX == minX + 1:
            newX = head[0]
        elif maxX == minX:
            newX = maxX

        if maxY == minY + 2:
            newY = minY + 1
        elif maxY == minY + 1:
            newY = head[1]
        elif maxY == minY:
            newY = maxY

        return (newX, newY)


    # Convention: rope[i][0] is the position of the knot. Rope[i][1] is the last
    # position of this knot. 
    rope = [(0,0) for i in range(10)]
    tailTracker = {(0,0):True}
    for d in directions:
        for step in range(d[1]):
            rope[0] = au.vectorAdd(rope[0], d[0])   # Move to new position

            # Move remaining knots based on the knot in front of them: 
            for k in range(1, len(rope)):
                knotT = rope[k]
                knotH = rope[k-1]
                if needsToMove(knotT, knotH):
                    rope[k] = whereToMove(knotT, knotH)
            tailTracker[rope[-1]] = True
            
    print(f"The tail was in {len(tailTracker)} distinct positions.")






