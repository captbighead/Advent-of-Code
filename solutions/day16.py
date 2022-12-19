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
    
    # Bog-standard string parsing
    node_pressure = {}
    node_exits = {}
    nodes = []
    for ln in valve_strs:
        ln = ln.replace("Valve ", "").replace(" has flow rate=",",")
        ln = ln.replace("s", "").replace("; tunnel lead to valve ", "|")
        ln = ln.split("|")
        node = ln[0].split(",")[0]
        nodes.append(node)
        node_pressure[node] = int(ln[0].split(",")[1])
        node_exits[node] = ln[1].split(", ")

    # STRATEGY: 
    #   - Use dijkstra's to map the routes to each node. 
    #   - Find nodes of consequence: nodes whose valves we need to turn
    #   - BFS over nodes, where each decision point is picking a valve to turn
    #       from the remaining valves to turn.

    routes = {}
    i = 0
    for i in range(len(nodes)):
        for j in range(i+1, len(nodes)):
            # Use dijkstra's to get the route in one direction, and then instead
            # of doing the costly algorithm to find out the way back, just copy
            # and flip the list
            ni = nodes[i]
            nj = nodes[j]
            route = dijkstra(ni, nj, node_exits)    
            routes[(ni, nj)] = route
            
            # Copy and flip. Also, remove the tail (routes don't include 
            # themselves)
            route = route.copy()
            route.reverse()
            routes[(nj, ni)] = route

    # The definitive to-do list
    valves_to_turn = set()
    for n in nodes:
        if node_pressure[n] > 0:
            valves_to_turn.add(n)

    # Now for the breadth first search. 
    first = Seeker(valves_to_turn, routes, node_pressure, nodes)
    processed = set([first])
    finished = set()
    queue = [first]
    while len(queue):
        this = queue.pop(0)
        processed.add(this)
        children = this.getChildren(processed)
        this_finished = children == [] or not len(this.todo_list)
        if this_finished:
            finished.add(this)
        else:
            queue.extend(children)

    maxPressure = 0
    maxSeeker = None
    for f in finished:
        if f.pressure > maxPressure:
            maxSeeker = f
            maxPressure = f.pressure

    print(f"The maximum pressure achievable is {maxPressure}.")

    au.printBanner("PART TWO - MULTITHREADING: <Now an elephant can run simulta"
                   "neously to us. What's the maximum pressure we can get if we"
                   " have two of us running at once?>")

    ## OOOOOH SHIT SON
    ## REVELATION: 'Finished' is already a list of full paths of seekers. If we
    ## can iterate over the list and combine them in such a way that one 
    ## represents a distinct path for the human and the other a distinct path 
    ## for the elephants, then we already have our solution, we just add the 
    ## pressures!

    # The following works for the test input, but it doesn't work for the actual
    # input. I think the reason it works for the test data is that it assumes 
    # that amongst the two people, all nodes would be hit. The "HashDisjoints"
    # is supposed to solve that but it doesn't... yet


    comboSpace = []
    hashVals = {}
    for p in processed:
        # Narrow down the search space. >= 4 and todo_list != [] is known for
        # sure. >= 15 is a guess. 
        if p.t >= 4 and p.t <= 21 and p.todo_list != []:  
            comboSpace.append(p)
            hashVals.setdefault(p.todohash, [])
            hashVals[p.todohash].append(p)

    hashDisjoints = {}
    for h in hashVals.keys():
        hashDisjoints[h] = []
        for h2 in hashVals.keys():
            if h & h2 == 0 and h2 != 0:
                hashDisjoints[h].append(h2)

    comboSpace = sorted(comboSpace, key=lambda s:s.pressure)
    comboSpace.reverse()
    comboMax = 0
    print(f"There were {len(comboSpace)} possible paths through the tunnels.")
    for i in range(len(comboSpace)):
        si = comboSpace[i]
        for sj in hashVals.get(si.comphash, []):
            comboMax = max(comboMax, si.pressure2 + sj.pressure2)
        #for dj in hashDisjoints.get(si.comphash,[]):
        #for sj in hashVals.get(dj, []):

    print(f"I think the most pressure you can get with an elephant'"
            f"s help is: {comboMax}")
            





            

    


class Seeker:

    def __init__(self, todo_list, map, valves, nodes, t=30, loc="AA", press=0):
        self.t = t
        self.location = loc
        self.pressure = press
        self.todo_list = todo_list
        self.map = map
        self.valve_lookup = valves
        self.nodes = nodes
        self.completed = set()
        self.pressure2 = 0
        self.todohash = 0
        self.comphash = 0


    def getChildren(self, processed):
        children = []
        for loc in self.todo_list:
            dist = len(self.map[(self.location, loc)])
            # 'dist' is the time in minutes it takes to get to the node *and* 
            # turn the valve.
            ct = self.t - dist   
            if ct < 0:
                # This child has no time, move on
                continue

            # The pressure at this node will be the remaining time after we've 
            # moved there and turned the valve multiplied by the pressure 
            # released from that valve every minute.
            cPress = self.pressure + ct * self.valve_lookup[loc]
            cPress2 = self.pressure2 + (ct-4) * self.valve_lookup[loc]
            cTodo = self.todo_list.copy()
            cTodo.remove(loc)
            cMap = self.map
            cValves = self.valve_lookup
            cIds = self.nodes
            child = Seeker(cTodo, cMap, cValves, cIds, ct, loc, cPress)
            child.completed = self.completed.copy()
            child.completed.add(loc)
            child.updateHashes()
            child.pressure2 = cPress2
            if child not in processed:
                children.append(child)
        return children


    def updateHashes(self):
        self.todohash = 0
        self.comphash = 0
        power = 0
        for n in self.nodes:
            self.todohash += 1 * (2 ** power) if n in self.todo_list else 0
            self.comphash += 1 * (2 ** power) if n in self.completed else 0
            power += 1
            

    def __hash__(self):
        # Needs to be equal to any other hash that has been to the same 
        # locations 
        power = 10 ** (len(self.nodes) + 3)
        ret = self.pressure * power
        power //= 100
        ret += self.t * power
        power //= 10
        for n in self.nodes:
            ret += power if n not in self.todo_list else 0
            power //= 10
        return ret

    def __eq__(self, value):
        t = self.t == value.t                 
        l = self.location == value.location  
        p = self.pressure == value.pressure  
        tl = self.todo_list == value.todo_list  
        return t and l and p and tl
    

           



def dijkstra(orig, dest, path_map):
    """ Returns the shortest path from orig to dest in paths.
    """
    unvisited = set([key for key in path_map.keys()])
    paths = {uv:None for uv in unvisited}
    paths[orig] = []
    visit_queue = [orig]

    while len(visit_queue):
        dist = lambda uv:len(paths[uv]) if paths[uv] is not None else 999999999
        visit_queue = sorted(visit_queue, key=dist)
        current = visit_queue.pop(0)
        unvisited.remove(current)

        if current == dest:
            paths[current].append(dest)
            return paths[current]

        for neighbour in path_map[current]:
            if neighbour in unvisited:
                ourpath = paths[current].copy()
                ourpath.append(current)
                if paths[neighbour] is None or len(ourpath) < len(paths[neighbour]):
                    paths[neighbour] = ourpath
                if neighbour not in visit_queue:
                    visit_queue.append(neighbour)


