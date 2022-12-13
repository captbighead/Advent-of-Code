"""
Solution Template for Advent of Code Solutions.
"""

import utilities.aoc_utils as au
import types

def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    monkey_defs = au.inputFileAsStrings(inputName)
    monkey_defs1 = [
                    "Monkey 0:"                         ,
                    "Starting items: 79, 98"            ,
                    "Operation: new = old * 19"         ,
                    "Test: divisible by 23"             ,
                    "If true: throw to monkey 2"        ,
                    "If false: throw to monkey 3"       ,
                    ""                                  ,
                    "Monkey 1:"                         ,
                    "Starting items: 54, 65, 75, 74"    ,
                    "Operation: new = old + 6"          ,
                    "Test: divisible by 19"             ,
                    "If true: throw to monkey 2"        ,
                    "If false: throw to monkey 0"       ,
                    ""                                  ,
                    "Monkey 2:"                         ,
                    "Starting items: 79, 60, 97"        ,
                    "Operation: new = old * old"        ,
                    "Test: divisible by 13"             ,
                    "If true: throw to monkey 1"        ,
                    "If false: throw to monkey 3"       ,
                    ""                                  ,
                    "Monkey 3:"                         ,
                    "Starting items: 74"                ,
                    "Operation: new = old + 3"          ,
                    "Test: divisible by 17"             ,
                    "If true: throw to monkey 0"        ,
                    "If false: throw to monkey 1"       
                    ]
    #monkey_defs = monkey_defs1
    
    class Monkey:

        def __init__(self, index, items, op, opTerm, divTerm, mt, mf):
            self.index = index
            self.items = items
            self.inspections = 0
            self.op = op
            self.opTerm = opTerm
            self.divTerm = divTerm
            self.mt = mt
            self.mf = mf
        
        def activate(self, monkeyList):
            while len(self.items):
                self.inspections += 1
                item = self.items.pop(0)
                actualTerm = item if self.opTerm is None else self.opTerm
                if self.op == "*":
                    item *= actualTerm
                else:
                    item += actualTerm
                item = self.worryDecay(item)
                target = self.mt if item % self.divTerm == 0 else self.mf
                monkeyList[target].catch(item)

        def catch(self, item):
            self.items.append(item)

        def worryDecay(self, item):
            return item // 3

        def __str__(self):
            return f"Monkey {self.index}: {self.inspections} inspections"

    def initMonkeys(defns):
        monkeyList = []
        index = 0

        while index < len(defns):
            mInd = int(defns[index].replace("Monkey ", "").replace(":", ""))
            mItems = defns[index+1].replace("Starting items: ", "")
            mItems = [int(i) for i in mItems.split(", ")]
            mOp = defns[index+2][21]
            mTerm = defns[index+2].replace("Operation: new = old ", "")[2:]
            mTerm = None if mTerm == "old" else int(mTerm)
            mDiv = int(defns[index+3].replace("Test: divisible by ", ""))
            mT = int(defns[index+4].replace("If true: throw to monkey ",""))
            mF = int(defns[index+5].replace("If false: throw to monkey ",""))
            monkeyList.append(Monkey(mInd, mItems, mOp, mTerm, mDiv, mT, mF))
            index += 7
        return monkeyList

    monkeys = initMonkeys(monkey_defs)
    for i in range(20):
        for m in monkeys:
            m.activate(monkeys)
    print(f"== After {i} rounds ==")
    for m in monkeys:
        print(m)
    print()

    monkeys = sorted(monkeys, key=lambda m: m.inspections)
    mb = monkeys[-1].inspections * monkeys[-2].inspections
    print(f"According to the infallible Monkey Business formula, the amount of "
          f"monkey business was {mb}")

    # Reinstantiate the monkeys from the input file (nothing carries over)
    monkeys = initMonkeys(monkey_defs)

    # We can't use the same worry decay method anymore. The numbers are going to
    # get big, but we need to still be able to operate on them in a reasonable 
    # time frame, and they need to resolve as they would have if we weren't 
    # causing decay. 

    # So, for all mDiv, num % mDiv needs to be the same number. I think if we 
    # take the product of each of the monkeys' div terms, and subtract it from
    # the item numbers until it's less than that term, we'll keep the same mod
    # values for each monkey. 
    prod = 1
    for m in monkeys:
        prod *= m.divTerm
    
    # So we're using the 'prod' as we would a tare on a scale... ish
    def worryDecay_2(self, item):
        return item % self.tare

    # Give every monkey the same tare and the new decay function.
    for m in monkeys:
        m.tare = prod
        m.worryDecay = types.MethodType(worryDecay_2, m)

    # Now we just activate each monkey in sequence 10,000 times!
    for i in range(10000):
        for m in monkeys:
            m.activate(monkeys)

        # Print at the key checkpoints from the example to check our work.
        if i in (0, 19, 999, 9999):
            print(f"== After {i} rounds ==")
            for m in monkeys:
                print(m)
            print()
    
    monkeys = sorted(monkeys, key=lambda m: m.inspections)
    mb = monkeys[-1].inspections * monkeys[-2].inspections
    print(f"According to the infallible Monkey Business formula, the amount of "
          f"monkey business was {mb}")