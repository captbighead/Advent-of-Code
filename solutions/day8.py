"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
   
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)
    #input = ["30373","25512","65332","33549","35390"]

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - TREETOP TREE HOUSE: <Find all the trees visible "
                   "from at least one (orthogonal) angle", 8)

    tree_map = {}
    for y in range(len(input)):
        for x in range(len(input[y])):
            tree_map[(x,y)] = int(input[y][x])

    maxY = len(input)
    maxX = len(input[0])
    visibleCount = 0
    for x in range(1, maxX-1):   # We only need to check inner trees
        for y in range(1, maxY-1):
            thisTree = tree_map[(x,y)]
            uvs = au.unitVectors()
            visibility = {uv:True for uv in uvs}
            for uv in uvs:
                cursor = au.vectorAdd((x,y), uv)
                while tree_map.get(cursor, -1) != -1:
                    treeHidden = tree_map[cursor] >= thisTree
                    visibility[uv] = visibility[uv] and not treeHidden
                    cursor = au.vectorAdd(cursor, uv)
            if True in visibility.values():
                visibleCount += 1

    visibleCount += maxX * 2 + maxY * 2 - 4
    
    print(f"Of {len(tree_map)} trees, {visibleCount} are visible from outside t"
          "he grid.")

    au.printBanner("PART TWO - BUT FORGET ALL THAT: <Find the 'scenic score' of"
                   " the tree with the largest 'scenic score' (the produc of th"
                   "e number of trees visible to it from each direction)")

    def scenicScore(xy):
        if xy == (2,3):
            print("Break")

        height = tree_map[xy]
        uvs = au.unitVectors()
        visibility = {uv:0 for uv in uvs}
        for uv in uvs:
            cursor = xy
            visibility[uv] = 1
            cursor = au.vectorAdd(cursor, uv)
            while tree_map.get(au.vectorAdd(cursor, uv), -1) != -1 and \
                tree_map[cursor] < height:
                    visibility[uv] += 1
                    cursor = au.vectorAdd(cursor, uv)
        prod = 1
        for v in visibility.values():
            prod *= v
        return prod

    maxScore = 1
    for x in range(1, maxX-1):          # Edge trees have scores of 0
        for y in range(1, maxY-1):
            maxScore = max(maxScore, scenicScore((x,y)))

    print(f"The maximum scenic score for trees in the set is {maxScore}")
            
