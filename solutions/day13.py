"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    packets = au.inputFileAsStrings(inputName)
    packets1 = [
                "[1,1,3,1,1]                ",
                "[1,1,5,1,1]                ",
                "                           ",
                "[[1],[2,3,4]]              ",
                "[[1],4]                    ",
                "                           ",
                "[9]                        ",
                "[[8,7,6]]                  ",
                "                           ",
                "[[4,4],4,4]                ",
                "[[4,4],4,4,4]              ",
                "                           ",
                "[7,7,7,7]                  ",
                "[7,7,7]                    ",
                "                           ",
                "[]                         ",
                "[3]                        ",
                "                           ",
                "[[[]]]                     ",
                "[[]]                       ",
                "                           ",
                "[1,[2,[3,[4,[5,6,7]]]],8,9]",
                "[1,[2,[3,[4,[5,6,0]]]],8,9]"
    ]
    packets1 = [s.strip() for s in packets1]
    #packets = packets1

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - DISTRESS SIGNAL", 13)
    
    def parse(s):   # Recursively turns a packet string into its underlying code
        # Base Case 1 - s is a numeric string (an int):
        if s.isnumeric():
            return int(s)
        # Base Case 2 - s is an empty list:
        if s == "[]":
            return []

        # Custom splitting Code:
        s = s[1:len(s)-1]   # Strip the outer pieces of the list 
        depth = 0
        curr = ""
        sList = []
        for c in s:
            # Track if comma is a nested list or not
            if c == "[":
                depth += 1
            elif c == "]":
                depth -= 1

            # If it's a comma and not nested, then this token is done
            if c == "," and depth == 0:
                sList.append(curr)
                curr = ""
            else:
                curr += c
        sList.append(curr)
        sList = sList
        retList = [parse(s1) for s1 in sList]
        return retList

    def ordered(l, r):
        if type(l) != type(r):
            if type(l) is int:
                l = [l]
            else:
                r = [r]
        if type(l) is int:
            return l < r if l != r else None
        
        ruling = None
        l_shorter = len(l) < len(r)
        i = 0
        while i < min(len(l), len(r)):
            ruling = ordered(l[i], r[i])
            if ruling is not None: 
                return ruling
            i += 1
        if ruling is None:
            return l_shorter if len(l) != len(r) else None





    # In this generic template, we're just going to parrot the input file.
    ordered_indices = 0
    i = 0
    for i in range((len(packets)+1)//3):

        # Rules: 
        #
        #   Values are l[v] and r[v]
        #
        #       - If both values are integers, right order is if l[v] < r[v]
        #       - If both are lists, right order is if len(l[v]) < len(r[v])
        #       - If one is a list, and the other an int, convert int into list
        l = parse(packets[i*3])
        r = parse(packets[i*3+1])
        ordered_indices += (i+1) if ordered(l,r) else 0

    print(f"Through the powers of recursion, we've found that {ordered_indices}"
          " pairs of packets are ordered!")

    au.printBanner("PART TWO - SORT IT ALL: <Now we sort the whole list>")

    packets.append("[[2]]")
    packets.append("[[6]]")
    ps = []
    for p in packets:
        if p == "":
            continue
        ps.append(parse(p))
    packets = ps

    # Insertion Sort is *fine* for a list of this size. Otherwise we'd need to 
    # find a deterministic indexing function for the packets that we could sort
    # them with. 
    i = 1
    while i < len(packets):
        j = i
        while not ordered(packets[j-1], packets[j]) and j >= 1:
            buffer = packets[j]
            packets[j] = packets[j-1]
            packets[j-1] = buffer
            j -= 1
        i += 1

    decoder_key = (packets.index([[2]])+1) * (packets.index([[6]])+1)
    print(f"The decoder key is {decoder_key}")
            



