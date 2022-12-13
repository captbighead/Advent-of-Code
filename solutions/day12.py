"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    inputGrid = au.inputFileAsStrings(inputName)
    #inputGrid = ["Sabqponm","abcryxxl","accszExk","acctuvwj","abdefghi"]

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - HILL CLIMBING ALGORITHM: <Find the shortest path"
                   " up a hill from spot S>", 12)
    
    # In this generic template, we're just going to parrot the input file.
    def translate(char):
        val = ord(char)
        if val == 69:
            val = -26   # E becomes -26; it's a special case of 26; ending pos.
        elif val == 83:
            val = -1    # S becomes -1; it's a special case of 1; starting pos.
        else:
           val -= 96    # a becomes 1, b becomes 2, etc...
        return val

        
    elev_map = au.parse2DGrid(inputGrid, translate)
    p1_start = ()
    p2_starts = []
    end = ()
    for k in elev_map.keys():
        if elev_map[k] == -1:
            p1_start = k
            p2_starts.append(k)
            elev_map[k] = 1
        elif elev_map[k] == -26:
            end = k
            elev_map[k] = 26
        elif elev_map[k] == 1:
            p2_starts.append(k)

    def dijkstra(map, start, end):
        # Standard rep for dijkstra's algorithm
        dists = {k:999999 for k in map.keys()}
        dists[start] = 0
        unvisited = set(map.keys())
        visit_queue = [start]

        while len(visit_queue):
            # Pull the node that's closest to the start 
            visit_queue = sorted(visit_queue, key=lambda xy:dists[xy])
            current = visit_queue.pop(0)
            unvisited.remove(current)

            # If we are 'visiting' the end point, this was the closest path to
            # get to it.
            if current == end:
                return dists[current]

            # Check its neighbours; if the neighbour is too high (relatively)
            # then it cannot be reached, so don't consider it.
            ns = []
            for v in au.unitVectors():
                n = au.vectorAdd(current, v)
                # Ensure we only consider a path to a neighbour if the neighbour
                # is no more than one level of elevation above us.
                if n in unvisited and map.get(n, 99) <= map[current] + 1:
                    # If accessing it through this node is faster than the 
                    # current path we've logged for it, record that
                    dists[n] = min(dists[n], dists[current]+1)
                    if n not in visit_queue:
                        visit_queue.append(n)
        
        # If we get here, then there was no path to E.
        return dists[end]

    print(f"The shortest path to the end spot is "
          f"{dijkstra(elev_map, p1_start, end)} steps long")

    au.printBanner("PART TWO - MAKE IT GENERIC: <Find the shortest path from an"
                   "y spot with elevation a.>")

    minPath = 999999
    for start in p2_starts:
        minPath = min(dijkstra(elev_map, start, end), minPath)

    print(f"The shortest path to the end spot from any spot of elevation a is "
          f"{minPath} steps long")
            

                    
        

