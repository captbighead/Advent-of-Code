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
    au.printBanner("PART ONE - NO SPACE LEFT ON DEVICE: <Calculate the sum of t"
                   "he file folders of size at least 100000>", 7)

    # In this generic template, we're just going to parrot the input file.
    currNode = None
    rootNode = None
    lnNum = 0
    for ln in input:
        lnNum += 1

        # If we start with a $ we're in a new command. We're either changing 
        # directories or starting a list in a new directory
        if ln.startswith("$"):
            cmd = ln.replace("$ ", "").split(" ")
            
            if cmd[0] == "ls":
                continue

            # cd / 
            if cmd[1] == "/" and rootNode is None:
                rootNode = au.TreeNode(("/", -1))   # Dirs have '-1' size; sent
            if cmd[1] == "/":
                currNode = rootNode
                continue

            # cd ..
            if cmd[1] == "..":
                currNode = currNode.parent
                continue

            # cd x
            for child in currNode.children:
                if child.val[0] == cmd[1] and child.val[1] == -1:
                    currNode = child

        # If it's not a command, it's a listing of something we've found.
        else:
            name = ln.split(" ")[1]
            size = -1 if ln.split(" ")[0] == "dir" else int(ln.split(" ")[0])
            valTup = (name, size)
            currNode.addChild(au.TreeNode(valTup))

    def size(treenode):
        ret = 0
        if treenode.val[1] == -1:
            for c in treenode.children:
                ret += size(c)
        else:
            ret = treenode.val[1]
        return ret

    dirsList = []
    tocheck = [rootNode]
    while len(tocheck):
        this_dir = tocheck.pop(0)
        dirsList.append((this_dir, size(this_dir)))
        for c in this_dir.children:
            if c.val[1] == -1:
                tocheck.append(c)

    sum = 0
    for d in dirsList:
        if d[1] < 100000:
            sum += d[1]

    print(f"The sum of the file sizes is {sum}")

    au.printBanner("PART TWO - BALETED: <Find the smallest directory that, once"
                   " deleted, frees up at least 30000000 bytes.>")

    systemMax = 70000000
    systemUsed = size(rootNode)
    spaceAvail = systemMax - systemUsed
    spaceNeeded = 30000000

    bigenough = []
    for d in dirsList:
        if spaceAvail + d[1] >= spaceNeeded:
            bigenough.append(d[1])
    bigenough = sorted(bigenough)

    print(f"You can delete a directory of size {bigenough[0]} to clear the need"
          "ed space.")









    


