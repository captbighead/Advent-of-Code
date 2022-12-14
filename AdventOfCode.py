import time
import utilities.aoc_utils as au
import solutions.day1 as d1
import solutions.day2 as d2
import solutions.day3 as d3
import solutions.day4 as d4
import solutions.day5 as d5
import solutions.day6 as d6
import solutions.day7 as d7
import solutions.day8 as d8
import solutions.day9 as d9
import solutions.day10 as d10
import solutions.day11 as d11
import solutions.day12 as d12
import solutions.day13 as d13
import solutions.day14 as d14

solns = [d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11,d12,d13,d14]
lastSoln = len(solns)

print()
print(" "*30, end="")
print("ADVENT OF CODE 2022")
au.printBanner("Welcome to my Advent of Code solutions project! The problems fo"
               f"r Days 1 through {lastSoln} can be accessed by entering the da"
               "y's number when prompted.\n")
while True:
    try:
        cursor = int(input(f"Choose a Solution (1-{lastSoln}; 0 to quit): "))
        if cursor:
            print()
            timer = time.time()
            solns[cursor-1].solve()
            timer = time.time() - timer
            print(f"\n(Completed in {round(timer,2)} seconds)\n")
        else:
            print("\nGoodbye!\n")
            exit(0)
    except (ValueError, IndexError) as err:
        print(err)
        print("Invalid option\n")
        continue