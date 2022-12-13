"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    input = au.inputFileAsStrings(inputName)

    au.printBanner("PART 1 - ROCK PAPER SCISSORS: In order to cheat at Rock, Pa"
                   "per, Scissors and get the tent spot closest to the snacks ("
                   "is this going to be the real theme of the season?) we need "
                   "to cheat at Rock, Paper, Scissors. We're given a 'strategy'"
                   " guide that will show us winning just the right amount of g"
                   "ames as to not be suspicious, and we need to find what our "
                   "overall score would be if we were to use that guide (appare"
                   "ntly winning with scissors is more prestigious!)", 2)
    
    beats = {1:3, 2:1, 3:2}         # Input x, y is what x 'beats'
    loses = {3:1, 1:2, 2:3}         # Input x, y is what x 'loses to'
    opp_LU = {"A":1, "B":2, "C":3}  # Rock, Paper, Scissors
    you_LU = {"X":1, "Y":2, "Z":3}  # Rock, Paper, Scissors/Lose, Draw, Win
    rounds = []
    for i in input:
        rounds.append((opp_LU[i[0]], you_LU[i[2]]))

    def scoreRound(r):
        if r[0] == r[1]:
            return 3
        elif r[0] == beats[r[1]]:   # IE: if opponent's pick is what yours beats
            return 6
        else:
            return 0


    def scoreGame(rs):
        myScore = 0
        for round in rs:
            myScore += round[1] + scoreRound(round)
        return myScore


    print(f"After using the strategy guide, I'd score {scoreGame(rounds)} pts")
        
    au.printBanner("PART 2 - UM, ACTUALLY: It turns out our assumption of how t"
                   "o read the guide was incorrect! Where before, we thought X "
                   "= Rock, Y = Paper, and Z = Scissors, it was actually X = Lo"
                   "se, Y = Draw, Z = Win (which makes much more sense).")

    # We don't need to adjust our inputed list at all here, just add a filter to
    # re-interpret it and turn it into the pairs such that we can reuse our 
    # score game function
    def calledShot(r):
        # What does r[1]' need to be to match the outcome prescribed by r[1]?
        if r[1] == 1:   # We need to lose
            return (r[0], beats[r[0]])
        elif r[1] == 2: # We need to tie
            return (r[0], r[0])
        elif r[1] == 3: # We need to win
            return (r[0], loses[r[0]])


    rounds = [calledShot(r) for r in rounds]
    print(f"After using the guide *correctly*, I'd score {scoreGame(rounds)} pt"
          "s")