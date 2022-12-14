"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    lines = au.inputFileAsStrings(inputName)
    lines_ex = ["498,4 -> 498,6 -> 496,6","503,4 -> 502,4 -> 502,9 -> 494,9"]
    #lines = lines_ex

    au.printBanner("PART ONE - REGOLITH RESERVOIR: We're in a cave filling with"
                   " sand! In order to know where to stand to not be crushed, w"
                   "e need to be able to simulate the sand as it fills the spac"
                   "e. Assume that the sand will fall into an endless void to p"
                   "rove the model is understood.", 14)


    grid = {(500,0):"+"}
    for ln in lines:
        xys = [tuple(int(xy) for xy in p.split(",")) for p in ln.split(" -> ")]
        for i in range(1, len(xys)):
            p1 = xys[i-1]
            p2 = xys[i]
            if p1[0] == p2[0]:
                miny = min(p1[1], p2[1])
                maxy = max(p1[1], p2[1])
                for y in range(miny, maxy+1):
                    grid[(p1[0],y)] = "#"
            else:
                minx = min(p1[0], p2[0])
                maxx = max(p1[0], p2[0])
                for x in range(minx, maxx+1):
                    grid[(x,p1[1])] = "#"

    # Ask the user if they want to track the falling sand: 
    au.printWrapped(f"There are two modes of operation for this solution. If yo"
                    "u wish to run without visualization, input 0, otherwise, i"
                    "nput a number of sand grains to drop between visualization"
                    " steps.\n")
    grainClock = getVisualizationPreference()


    sandCount = simulateSandfall(grid, grainClock, False)
    print(f"The final amount of grains of sand at rest is {sandCount}")

    au.printBanner("PART TWO - LOOKS LIKE A CLOGGED SOURCE: The sand can no lon"
                   "ger overflow. Assume the cave floor is an infinite plane tw"
                   "o positions below the maximum of the existing grid. How man"
                   "y grains fall until the source is blocked?")
    
    # Prompt for visualization input here, in case the user wants to change 
    # their preference for part 2.
    au.printWrapped(f"As with part one, this has two operation modes. Please in"
                    "dicate your visualization preference for this part:\n")
    au.printWrapped("(Just, be warned, the number could be orders of magnitude "
                    "larger!)\n")
    grainClock = getVisualizationPreference()

    # We don't need to wipe the sand from the previous grid; it's all still 
    # there. The simulation will only count new grains of sand.
    sandCount += simulateSandfall(grid, grainClock, True)   
    print(f"The final amount of grains of sand at rest (when the cave has a flo"
          f"or) is {sandCount}")


def simulateSandfall(grid, visualize=0, hasFloor=False):
    # Record the bounds of the grid for the renderer, and so we know when the 
    # sand falls beyond it
    bounds = {"minX":500, "maxX":500, "minY":0, "maxY":0}
    for xy in grid.keys():
        bounds["minX"] = min(bounds["minX"], xy[0])
        bounds["maxX"] = max(bounds["maxX"], xy[0])
        bounds["minY"] = min(bounds["minY"], xy[1])
        bounds["maxY"] = max(bounds["maxY"], xy[1])
    floorY = bounds["maxY"] + 2 # If we have a floor, this is it's y value

    # Visualize the blank state, if we're visualizing.
    if visualize:
        au.render2DGrid(grid, bounds)
        input()

    # The sand backs up in the event that the cave has a floor. 
    sandCount = 0
    while grid.get((500,0), " ") != "o":    
        sand = (500,0)
        atRest = False
        while not atRest:
            # Project for obstacles, checking in priority order of directly down
            # followed by down and left, and then down and right. After the 
            # first viable path down, we short circuit and continue along it.
            dn = au.vectorAdd(sand, ( 0,1))
            dl = au.vectorAdd(sand, (-1,1))
            dr = au.vectorAdd(sand, ( 1,1))

            # Special case: if we would drop past the lowest point in the known
            # grid, we're actually falling infinitely, which is the end 
            # condition of part one. Break without being at rest:
            if not hasFloor and dn[1] > bounds["maxY"]:
                break

            # Another special case: if the cave is supposed to have a floor, and
            # we are beyond maxY, insert a floor below our falling sand.
            if hasFloor and sand[1] > bounds["maxY"]:
                grid[dn] = "#"
                grid[dl] = "#"
                grid[dr] = "#"
                # Extend the drawing bounds if we've pushed on them with our 
                # sand
                bounds["minX"] = min(bounds["minX"], dl[0])
                bounds["maxX"] = max(bounds["maxX"], dr[0])

            # Use the projections to actually pathfind, and move if possible.
            if grid.get(dn, " ") not in ("o", "#"):
                sand = dn
                continue
            if grid.get(dl, " ") not in ("o", "#"):
                sand = dl
                continue
            if grid.get(dr, " ") not in ("o", "#"):
                sand = dr
                continue

            # If we get here, there was no unobstructed path, so we are now at
            # rest and can stop moving.
            atRest = True

        # If we got out of the loop without being at rest, we have reached a
        # point where all future sand will fall into the endless void. This is 
        # the true end condition (for Part 1)
        if not atRest:
            break

        # Otherwise we are at rest, so place the sand into the grid, and then
        # render it if we want to visualize it.
        grid[sand] = "o"
        sandCount += 1
        if visualize and not sandCount % visualize: # Visualize after n grains
            # bounds["maxY"] is important to the logic operations of both part 1
            # and part 2 (in part 2, we check against it to know when to insert
            # a floor as needed). This means that the logic bounds and the 
            # render bounds need to be different in part 2. 
            renderBounds = bounds.copy()
            if hasFloor: 
                renderBounds["maxY"] = floorY
            au.render2DGrid(grid, renderBounds)
            print("-"*80)
            input()
    
    # We've finished looping. The sandCount shows the grains at rest. 
    if visualize:
        # Copying code is a sin. I'm a sinner.
        renderBounds = bounds.copy()
        if hasFloor: 
            renderBounds["maxY"] = floorY
        au.render2DGrid(grid, renderBounds)
    return sandCount

        
def getVisualizationPreference():
    grainClock = None
    while grainClock is None:
        grainClock = input("Enter your choice [0 = no vis, n = after every nth "
                           "grain]:")
        if not grainClock.isnumeric() or int(grainClock) < 0:
            grainClock = None
        else:
            grainClock = int(grainClock)
    return grainClock

