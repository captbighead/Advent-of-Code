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
    valves_to_turn = []
    for n in nodes:
        if node_pressure[n] > 0:
            valves_to_turn.append(n)

    activeVariants = []
    for v in valves_to_turn:
        todo = valves_to_turn.copy()
        todo.remove(v)
        activeVariants.append(Variant("AA",v,todo,{},routes))
    
    successfulVariants = []
    for t in range(1,31):
        print(f"\rSimulating minute {t}", end="")
        variants_to_purge = []
        variants_this_tick = []
        for av in activeVariants:
            newVariants = av.act(t)
            if newVariants is not None:
                variants_this_tick.extend(newVariants)
            if av.goal is None and len(av.todo_list) != 0:
                variants_to_purge.append(av)
            if av.goal is None and len(av.todo_list) == 0:
                successfulVariants.append(av)
                variants_to_purge.append(av)
        activeVariants.extend(variants_this_tick)
        while len(variants_to_purge):
            vtp = variants_to_purge.pop(0)
            activeVariants.remove(vtp)
    print()


    bestPressure = 0
    bestVariant = None
    for v in successfulVariants:
        v.pressure = 0
        for t in range(1,31):
            if v.log.get(t, False) and v.log[t] == "Turned Valve":
                v.pressure += (30-t) * node_pressure[v.log[t-1][9:]]
            if v.pressure > bestPressure:
                bestVariant = v
                bestPressure = v.pressure

    print(f"The best pressure achievable is {bestPressure}. It was achieved wit"
          "h the following steps:\n")
    for t in range(1,31):
        logmsg = bestVariant.log.get(t,"")
        if logmsg == "":
            break
        print(f"Minute {t}: {logmsg}")


class Variant:

    def __init__(self, location, goal, todo_list, log, map):
        self.todo_list = todo_list
        self.location = location
        self.map = map
        self.goal = goal
        self.log = log


    def haveKids(self):
        kids = []
        for n in self.todo_list:
            cGoal = n
            cTodo = self.todo_list.copy()
            cTodo.remove(n)
            cLog = self.log.copy()
            kids.append(Variant(self.location, cGoal, cTodo, cLog, self.map))
        return kids


    def act(self, t):
        # We have performed our purpose in this world, and now shall perish
        if self.goal is None:
            return None

        # If we reached our goal, we spawn our possible children, and then sit
        # content, knowing we've done all we can for the cause.
        if self.location == self.goal:
            self.goal = None
            self.log[t] = "Turned Valve"
            
            if len(self.todo_list):
                return self.haveKids()
            else:
                return None
        
        # If we get here, we're moving towards our goal:
        self.location = self.map[(self.location, self.goal)][1]
        self.log[t] = "Moved to " + self.location
        return None
        



            



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


