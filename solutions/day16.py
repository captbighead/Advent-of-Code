import time
import utilities.aoc_utils as au

def solve():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    valve_strs = au.inputFileAsStrings(inputName)
    vs_ex = ["Valve AA has flow rate=0; tunnels lead to valves DD, II, BB",
             "Valve BB has flow rate=13; tunnels lead to valves CC, AA",
             "Valve CC has flow rate=2; tunnels lead to valves DD, BB",
             "Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE",
             "Valve EE has flow rate=3; tunnels lead to valves FF, DD",
             "Valve FF has flow rate=0; tunnels lead to valves EE, GG",
             "Valve GG has flow rate=0; tunnels lead to valves FF, HH",
             "Valve HH has flow rate=22; tunnel leads to valve GG",
             "Valve II has flow rate=0; tunnels lead to valves AA, JJ",
             "Valve JJ has flow rate=21; tunnel leads to valve II"]
    #valve_strs = vs_ex

    au.printBanner("PART ONE - PROBOSCIDEA VOLCANIUM: You're in a volcano with "
                   "a bunch of elephants, for some reason! You need to escape, "
                   "but along the way you need to turn a bunch of valves. Each "
                   "valve takes a minute of time to open, and each tunnel betwe"
                   "en the valves takes a minute to traverse. You need to maxim"
                   "ize the amount of pressure released by the valves over the "
                   "course of your journey, while making it out. Sounds like so"
                   "me travelling salesman shenanigans are about to ensue!", 16)
    
    # Okay, so I really need membership for a given search path to be a very 
    # fast lookup. To do that, I'm futzing with the hash function so that each
    # one can generate as unique of a hash as possible. Hashing the timestamp, 
    # length of the path, and the length of the open valves list is easy enough,
    # but lots of nodes will have identical hashes there. If each node *in* the 
    # path contributed to a hash value that didn't have to be determined by 
    # iterating over the path, though, that would be ideal.
    #
    # If we add up values of the node (multiple times if the node is revisited)
    # and those values were distinct, and prime, then in theory no two paths 
    # should have the same value, so long as the values aren't divisble by the 
    # number of occurrences of any other node (IE: a prime number greater than 
    # the number of occurrences of any node in the list). Since there can be 
    # some 30 nodes, if the list of ids for each starts at 31 and consists of 
    # consecutive primes following that, then the hash should be unique? 
    primes = [31, 37,41,43,47,53,59,61,67,71,73,79,83,89,97,101,103,107,109,113,
              127,131,137,139,149,151,157,163,167,173,179,181,191,193,197,199,
              211,223,227,229,241,251,257,263,269,271,277,281,283,293,307,311,
              313,317,331,337,347,349]
    hash_fn = {}
    for ln in valve_strs:
        hash_fn[ln.replace("Valve ", "")[0:2]] = primes.pop(0)


    # Bog-standard string parsing
    nodes = {}
    paths = {}
    for ln in valve_strs:
        ln = ln.replace("Valve ", "").replace(" has flow rate=",",")
        ln = ln.replace("s", "").replace("; tunnel lead to valve ", "|")
        ln = ln.split("|")
        nodes[ln[0].split(",")[0]] = int(ln[0].split(",")[1])
        paths[ln[0].split(",")[0]] = ln[1].split(", ")

    max_pressure = 0
    max_path = None
    options = bfs_pressureValves(nodes, paths, hash_fn)
    for sp in options:
        if sp.system_pressure > max_pressure:
            max_path = sp

    print(f"The maximum amount of pressure we could release is: {max_pressure}")


class SearchPath:
    """ Just a basic wrapper for the state of the search along this path
    """

    def __init__(self, nodes, paths, hash_fn):
        self.system_pressure = 0
        self.timestamp = 0
        self.path = ["AA"]
        self.nodes = nodes
        self.paths = paths
        self.openvalves = []
        self.hash_fn = hash_fn
        self.hash_from_path = hash_fn["AA"]


    def getChildPaths(self):
        """ Creates child SearchPath objects from actions you could perform
        """
        # If the timestamp is 30, we're actuall done.
        if self.timestamp == 30: 
            return []

        # current state, simplified for reference
        node = self.path[-1]
        childPaths = []
        pressure = self.nodes[node]

        # Only create the open valve option if it makes sense; IE: if it's not
        # already open, and if opening it would add to the system pressure.
        if pressure != 0 and node not in self.openvalves:
            child = self.birth()
            child.timestamp += 1
            child.system_pressure += pressure * (30 - child.timestamp)
            child.openvalves.append(node)
            childPaths.append(child)

        # Create the children generated from moving to each child node.
        for dest in self.paths[self.path[-1]]:
            child = self.birth()
            child.timestamp += 1
            child.path.append(dest)
            child.hash_from_path += self.hash_fn[dest]
            childPaths.append(child)
        
        return childPaths


    def birth(self):
        child = SearchPath(self.nodes, self.paths, self.hash_fn)
        child.system_pressure = self.system_pressure
        child.timestamp = self.timestamp
        child.path = self.path.copy()
        child.hash_from_path = self.hash_from_path
        return child


    def isFinished(self):
        return self.timestamp == 30
            

    def __hash__(self):
        h = self.timestamp * 1000000000 
        h += len(self.path) * 10000000 
        h += len(self.openvalves) * 100000
        h += self.hash_from_path
        return h
    

    def __eq__(self, value):
        ts = self.timestamp == value.timestamp
        sp = self.system_pressure == value.system_pressure
        p = self.path == value.path
        ov = self.openvalves == value.openvalves
        return ts and sp and p and ov


def bfs_pressureValves(nodemap, pathmap, hash_fn):
    updates = 0
    rejects = 0
    time_start = time.time()    # Track progression as we go so I can see if we
                                # are ballooning into infinity

    # Initialize this custom search queue as a pseudo link-list that is also a 
    # hash map so that we can make sure we can check membership speedy-quick
    # while still being able to use it like a queue
    first = SearchPath(nodemap, pathmap, hash_fn)
    first_children = first.getChildPaths()
    search_queue = {first:first_children[0]}
    for i in range(1, len(first_children)):
        search_queue[first_children[i-1]] = first_children[i]

    # Track our complete paths in a hashmap too so we can check membership 
    # speedy-quick
    complete_paths = {}
    discarded_paths = {}

    next = first
    tail = first_children[-1]
    while len(search_queue.keys()):

        # Progress notifications:
        elapsed = time.time() - time_start
        if elapsed > 10:
            updates += 1
            print(f"After {updates*10} seconds, we have {len(search_queue)} nod"
                  f"es in the search queue and {len(complete_paths)} in the com"
                  "pleted paths list.")
            time_start = time.time()

        # Actual BFS
        next = search_queue.pop(next)
        if next.isFinished():
            complete_paths[next] = True
        else:
            discarded_paths[next] = True
            for child in next.getChildPaths():
                # sq: Child is in search queue as key or the tail
                sq = search_queue.get(child, None) is not None or tail == child
                # cp: Child is in the completed paths
                cp = complete_paths.get(child, False)
                # dp: Child is in the discarded paths
                dp = discarded_paths.get(child, False)

                # If child is in none of the lists, we add it to the queue
                if not sq and not cp and not dp:
                    search_queue[tail] = child
                    tail = child
                else:
                    rejects += 1
    return complete_paths




