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
    
    # Let's try and make the banner "line-wrap"
    i = 0
    lines = []
    right = i
    while i*80+80 < len(problem_statement):
        left = i*80
        right = i*80+80
        lines.append(problem_statement[left:right])
        i += 1
    lines.append(problem_statement[right:])
    
    print("\n")
    for line in lines:
        print(line)
    print("\n")

def unitVectors():
    """ Returns list of tuples representing unit vectors for cardinal directions

        If it matters, the vectors are, in order: Up, Right, Down, Left (NEWS)
    """
    return [( 0,-1),( 1, 0),( 0, 1),(-1, 0),]   

def parse2DGrid(gridList, translation=lambda x: x):
    return_map = {}
    for y in range(len(gridList)):
        for x in range(len(gridList[y])):
            return_map[(x,y)] = translation(gridList[y][x])
    return return_map


def vectorAdd(v, u):
    return (v[0] + u[0], v[1] + u[1])

class TreeNode:

    def __init__(self, val, parent=None):
        self.val = val
        self.parent = parent
        self.children = []

    def addChild(self, child):
        self.children.append(child)
        child.parent = self

