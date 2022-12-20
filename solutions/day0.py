import utilities.aoc_utils as au

def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    lines = au.inputFileAsStrings(inputName)
    lines_ex = ["Test data", "Examples"]   # Example data goes here
    
    # Data parser goes here
    
    # Choosing to comment/uncomment this line is how we switch between the test
    # input and the actual input. 
    lines = lines_ex

    au.printBanner("This is a really long paragraph to describe the problem. I "
                   "could include generic lorem ipsum, but why make it easy? Sc"
                   "rew Dolores and her est! ...I'm just kidding, of course. Is"
                   " this over eighty characters yet? Man I really hope so.", 0)
    
    # The actual solution goes here.
    for i in lines:
        print(i)


