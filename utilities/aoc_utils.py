def inputFileAsStrings(filename):
    """ Provided a file name, will convert it into a list of strings.
    """
    input = []
    with open(filename) as f:
        input = [line.strip() for line in f]
    return input


def printBanner(problem_statement, day_num=-1):
    if day_num != -1:
        leadSpace = " " if day_num < 10 else ""
        print(" "*35, end="")
        print("-"*10)
        print(" "*35, end="")
        print(f"| DAY {leadSpace}{day_num} |")
        print(" "*35, end="")
        print("-"*10)
    else:
        print("-"*80)
    
    print("\n")
    printWrapped(problem_statement)
    print("\n")


def printWrapped(s):
    # Let's try and make the banner "line-wrap"
    i = 0
    lines = []
    right = i
    while i*80+80 < len(s):
        left = i*80
        right = i*80+80
        lines.append(s[left:right])
        i += 1
    lines.append(s[right:])
    for line in lines:
        print(line)


def render2DGrid(grid, bounds=None, whitespace=" "):
    # Find the bounds of the grid's co-ordinate system if not provided.
    minX = [k for k in grid.keys()][0][0] if bounds is None else bounds["minX"]
    maxX = [k for k in grid.keys()][0][0] if bounds is None else bounds["maxX"]
    minY = [k for k in grid.keys()][0][1] if bounds is None else bounds["minY"]
    maxY = [k for k in grid.keys()][0][1] if bounds is None else bounds["maxY"]
    if bounds is None:
        for xy in grid.keys():
            minX = min(minX, xy[0])
            minY = min(minY, xy[1])
            maxX = max(maxX, xy[0])
            maxY = max(maxY, xy[1])

    for y in range(minY, maxY+1):
        for x in range(minX, maxX+1):
            print(grid.get((x,y), whitespace), end="")
        print()



def unitVectors():
    """ Returns list of tuples representing unit vectors for cardinal directions

        If it matters, the vectors are, in order: Up, Right, Down, Left (NEWS)
    """
    return [( 0,-1),( 1, 0),( 0, 1),(-1, 0)]   


def parse2DGrid(gridList, translation=lambda x: x):
    return_map = {}
    for y in range(len(gridList)):
        for x in range(len(gridList[y])):
            return_map[(x,y)] = translation(gridList[y][x])
    return return_map


def vectorAdd(v, u):
    return (v[0] + u[0], v[1] + u[1])


def manhattanDistance(xy1, xy2):
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])


class TreeNode:

    def __init__(self, val, parent=None):
        self.val = val
        self.parent = parent
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

