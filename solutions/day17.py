import utilities.aoc_utils as au

def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    lines = au.inputFileAsStrings(inputName)
    lines_ex = [">>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>"]
    
    # Comment below switches between example and actual input
    lines = lines_ex
    render_each_stone = True
    
    # Custom iterable class to get the next instruction from the gust list.
    class Gust:
        
        def __init__(self, gust):
            self.p = 0
            self.gust = gust
        
        
        def __iter__(self):
            self.p = 0
            return self
        
        
        def __next__(self):
            if self.p == len(self.gust):
                self.p = 0
            ret = (-1, 0) if self.gust[self.p] == "<" else (1,0)
            self.p += 1
            return ret 
        
        
        def next(self):
            return self.__next__()
        
        
    # Custom iterable class to get the next shape from the shape list.
    class Stone:
        
        def __init__(self):
            self.p = 0
            self.shapes = [
                [(2,-3),(3,-3),(4,-3),(5,-3)],
                [(3,-5),(2,-4),(3,-4),(4,-4),(3,-3)],
                [(2,-3),(3,-3),(4,-3),(4,-4),(4,-5)],
                [(2,-3),(2,-4),(2,-5),(2,-6)],
                [(2,-3),(3,-3),(2,-4),(3,-4)]
            ]
        
        
        def __iter__(self):
            self.p = 0
            return self
        
        
        def __next__(self):
            if self.p == len(self.shapes):
                self.p = 0
            ret = self.shapes[self.p]
            self.p += 1
            return ret 
        
        
        def next(self):
            return self.__next__()
    
    
    au.printBanner("PART ONE - PYROCLASTIC FLOW: <Find out the height of the Te"
                   "tris-y tower after 2022 blocks have been dropped.>", 17)
    
    # Debugging tools to visualize the stones falling.
    debug_grid = {} # A
    bds = {"minX":0,"maxX":6,"minY":-6,"maxY":0}
    
    rocks = 0
    sGen = Stone()
    gGen = Gust(lines[0])
    grid = [1,1,1,1,1,1,1]  # The y-co-ordinates of column's impassible height
    dwn = (0,1)             # The unit vector for downward movement.
    while rocks < 2022:
        shp = sGen.next()
        flr = min(grid)-1     # The point above which we spawn. Negative == Up
        shp = [au.vectorAdd(xy, (0,flr)) for xy in shp]
        
        settled = False
        minX = min([xy[0] for xy in shp])
        maxX = max([xy[0] for xy in shp])
        minY = min([xy[1] for xy in shp])
        while not settled:
            # Check left to right movement and apply if you can
            lr = gGen.next()
            if lr[0] + minX >= 0 and lr[0] + maxX < 7:
                shp = [au.vectorAdd(lr, xy) for xy in shp]
                minX += lr[0]
                maxX += lr[0]
            
            # Check downward movement and apply if you can, otherwise we settled
            for xy in shp:
                settled = settled or xy[1] + 1 == grid[xy[0]]
            if not settled:
                shp = [au.vectorAdd(dwn, xy) for xy in shp]
            else:
                
                # TODO: WE NEED TO UNDO THE LR move?
                
                
                # Update the record of the impassible layer in each column
                for x in range(len(grid)):
                    ys_at_x = [xy[1] for xy in shp if xy[0] == x]
                    shp_y_at_x = min(ys_at_x) if len(ys_at_x) else grid[x]
                    grid[x] = min(grid[x], shp_y_at_x)
                    
        # Render after fall
        if render_each_stone:
            # Update the grid for rendering.
            bds["minY"] = min(bds["minY"], minY)
            for xy in shp:
                debug_grid[xy] = f"{sGen.p}"
            au.render2DGrid(debug_grid, bds, ".")
            input()
        
        rocks += 1
        