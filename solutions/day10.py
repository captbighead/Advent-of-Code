"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    # The default template will read an input file from the inputs folder with
    # the same name as this file.
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    program = au.inputFileAsStrings(inputName)
    program_example = ["addx 15","addx -11","addx 6","addx -3","addx 5",
                       "addx -1","addx -8","addx 13","addx 4","noop","addx -1",
                        "addx 5","addx -1","addx 5","addx -1","addx 5",
                        "addx -1","addx 5","addx -1","addx -35","addx 1",
                        "addx 24","addx -19","addx 1","addx 16","addx -11",
                        "noop","noop","addx 21","addx -15","noop","noop",
                        "addx -3","addx 9","addx 1","addx -3","addx 8","addx 1",
                        "addx 5","noop","noop","noop","noop","noop","addx -36",
                        "noop","addx 1","addx 7","noop","noop","noop","addx 2",
                        "addx 6","noop","noop","noop","noop","noop","addx 1",
                        "noop","noop","addx 7","addx 1","noop","addx -13",
                        "addx 13","addx 7","noop","addx 1","addx -33","noop",
                        "noop","noop","addx 2","noop","noop","noop","addx 8",
                        "noop","addx -1","addx 2","addx 1","noop","addx 17",
                        "addx -9","addx 1","addx 1","addx -3","addx 11","noop",
                        "noop","addx 1","noop","addx 1","noop","noop",
                        "addx -13","addx -19","addx 1","addx 3","addx 26",
                        "addx -30","addx 12","addx -1","addx 3","addx 1","noop",
                        "noop","noop","addx -9","addx 18","addx 1","addx 2",
                        "noop","noop","addx 9","noop","noop","noop","addx -1",
                        "addx 2","addx -37","addx 1","addx 3","noop","addx 15",
                        "addx -21","addx 22","addx -6","addx 1","noop","addx 2",
                        "addx 1","noop","addx -10","noop","noop","addx 20",
                        "addx 1","addx 2","addx 2","addx -6","addx -11","noop",
                        "noop","noop"]
    #program = program_example
    
    # Solve first, then print stuff about it. 
    sumSignals = 0
    crtBuffer = [""]
    t = 0       # Tracks the current cycle. t is for 'tick'
    x = 1       # Tracks the x register
    i = 0       # Tracks the program's instruction
    o = False   # Tracks if we're one tick into an addx instruction
    #while i < len(program):   # The hard-coded dimensions of the output screen
    while t < (40*6):   # The hard-coded dimensions of the output screen
        # We start off in a new cycle.
        t += 1
        op = program[i][0:4]
        opval = int(program[i][5:]) if op == "addx" else 0

        # During the cycle - Update the signal for the part one solution.
        sumSignals += (t * x) if (t-20) % 40 == 0 else 0

        # During the cycle - we draw to the CRT
        p = (t-1) % 40  # Pixel being drawn this cycle. 
        if p == 0:
            crtBuffer.append("")
        crtBuffer[-1] += "#" if p >= x - 1 and p <= x + 1 else " "

        # Once the cycle has completed, 'instantaneously' update x.
        x = (x + opval) if o else x
        i += 1 if op == "noop" or o else 0
        o = op == "addx" and not o

    # Go ahead and create a banner here to explain the problem.
    au.printBanner("PART ONE - CATHODE-RAY TUBE: We have a small program used t"
                   "o interpret a stream of signals. We need to show our model "
                   "for interpreting it works by reporting the signal strengths"
                   " (multiplied by the ticks they occurred on) as a sum.", 10)

    print(f"\nThe sum of the signal strengths is {sumSignals}")
        
    au.printBanner("PART TWO - PRINTSCREEN: Now, implementing a render code to "
                   "work with the signal interpreter, we need to show what the "
                   "device displays to us.")

    # We already did that in the first pass :) 
    for ln in crtBuffer:
        print(ln)


