"""
Solution Template for Advent of Code Solutions.
"""
import time
import utilities.aoc_utils as au

def solve():

    print("Whoops! Started a re-try of this one but didn't finish it yet. Lemme"
          " just reroute ya here...")
    solve_orig()
    return

    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    sensor_readings = au.inputFileAsStrings(inputName)
    sr_ex = ["Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
             "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
             "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
             "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
             "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
             "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
             "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
             "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
             "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
             "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
             "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
             "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
             "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
             "Sensor at x=20, y=1: closest beacon is at x=15, y=3"]
    
    # Different benchmarks for the example and the actual problem. 
    y_check = 2000000
    y_check_ex = 10
    y_part_2 = 4000000
    y_part_2_ex = 20

    # The now-standard commentable lines that switch between running for the 
    # example and for the output. 
    #sensor_readings = sr_ex
    #y_check = y_check_ex
    #y_part_2 = y_part_2_ex

    au.printBanner("PART ONE - BEACON EXCLUSION ZONE: <Given a list of sensors "
                   "and the closest beacons to them (via manhattan distance), o"
                   "utput the number of spaces on y=2,000,000 that cannot possi"
                   "bly contain a beacon.>", 15)
    
    # Bog-standard string processing.
    sensors = []
    for ln in sensor_readings:
        ln = ln.replace("Sensor at ", "").replace(" closest beacon is at ", "")
        ln = ln.replace("x=", "").replace(" y=","").split(":")
        sens = tuple([int(xy) for xy in ln[0].split(",")])
        beac = tuple([int(xy) for xy in ln[1].split(",")])
        sensors.append(Sensor(sens, beac))
        



class Sensor:

    def __init__(self, xy, bxy):
        self.xy = xy
        self.beacon = xy
        mr = au.manhattanDistance(xy, bxy)
        self.mr = mr
        cs = [au.vectorAdd(xy, (v[0]*mr, v[1]*mr)) for v in au.unitVectors()]
        self.corners = cs



def solve_orig():
    inputName = __name__.replace("solutions.","inputs\\") + ".txt"
    sensor_readings = au.inputFileAsStrings(inputName)
    sr_ex = ["Sensor at x=2, y=18: closest beacon is at x=-2, y=15",
             "Sensor at x=9, y=16: closest beacon is at x=10, y=16",
             "Sensor at x=13, y=2: closest beacon is at x=15, y=3",
             "Sensor at x=12, y=14: closest beacon is at x=10, y=16",
             "Sensor at x=10, y=20: closest beacon is at x=10, y=16",
             "Sensor at x=14, y=17: closest beacon is at x=10, y=16",
             "Sensor at x=8, y=7: closest beacon is at x=2, y=10",
             "Sensor at x=2, y=0: closest beacon is at x=2, y=10",
             "Sensor at x=0, y=11: closest beacon is at x=2, y=10",
             "Sensor at x=20, y=14: closest beacon is at x=25, y=17",
             "Sensor at x=17, y=20: closest beacon is at x=21, y=22",
             "Sensor at x=16, y=7: closest beacon is at x=15, y=3",
             "Sensor at x=14, y=3: closest beacon is at x=15, y=3",
             "Sensor at x=20, y=1: closest beacon is at x=15, y=3"]
    
    # Different benchmarks for the example and the actual problem. 
    y_check = 2000000
    y_check_ex = 10
    y_part_2 = 4000000
    y_part_2_ex = 20

    # The now-standard commentable lines that switch between running for the 
    # example and for the output. 
    #sensor_readings = sr_ex
    #y_check = y_check_ex
    #y_part_2 = y_part_2_ex

    au.printBanner("PART ONE - BEACON EXCLUSION ZONE: <Given a list of sensors "
                   "and the closest beacons to them (via manhattan distance), o"
                   "utput the number of spaces on y=2,000,000 that cannot possi"
                   "bly contain a beacon.>", 15)
    
    # Bog-standard string processing. 
    closest = {}
    beacons = []
    sensors = []
    bounds = None
    for ln in sensor_readings:
        ln = ln.replace("Sensor at ", "").replace(" closest beacon is at ", "")
        ln = ln.replace("x=", "").replace(" y=","").split(":")
        sens = tuple([int(xy) for xy in ln[0].split(",")])
        beac = tuple([int(xy) for xy in ln[1].split(",")])
        closest[sens] = beac
        sensors.append(sens)
        # A beacon can be seen by multiple sensors. Only count it once. 
        if beac not in beacons:     
            beacons.append(beac)

        # We also need to keep track of the bounds of the grid we're making. The
        # furthest possible spaces that need to be checked for any given sensor
        # are the spaces along the cardinal directions from the sensor, with 
        # magnitudes equal to the Manhattan distance from the sensor to its 
        # beacon
        dist = au.manhattanDistance(sens, beac)
        furthest = [(v[0] * dist, v[1] * dist) for v in au.unitVectors()]
        furthest = [au.vectorAdd(sens, v) for v in furthest]
        furthest_bounds = {}
        furthest_bounds["minX"] = min([v[0] for v in furthest])
        furthest_bounds["maxX"] = max([v[0] for v in furthest])
        furthest_bounds["minY"] = min([v[1] for v in furthest])
        furthest_bounds["maxY"] = max([v[1] for v in furthest])


        # Keep a running tab on the bounds of the grid we're making. 
        if bounds is None:
            bounds = furthest_bounds
        bounds["minX"] = min(bounds["minX"], furthest_bounds["minX"])
        bounds["maxX"] = max(bounds["maxX"], furthest_bounds["maxX"])
        bounds["minY"] = min(bounds["minY"], furthest_bounds["minY"])
        bounds["maxY"] = max(bounds["maxY"], furthest_bounds["maxY"])

    # Now for the actual part one solution:
    #
    # Note: Even just iterating within the bounds of minX:maxX where y=y_check
    # is infeasible as a solution. In the actual solution, this works out to be
    # roughly 166,000,000 checks that it has to do. 
    #
    # That's too many checks. 
    #
    # Instead, we'll calculate the coverage of x that each sensor provides, and
    # use that to find the area covered. 
    y_visible = []
    for s in sensors:
        b = closest[s]
        dist = au.manhattanDistance(s, b)

        # We need to find the points on y where the 'manhattan radius' <= y
        yComponent = au.manhattanDistance(s, (s[0], y_check))
        if yComponent > dist:   # We don't even reach y with this sensor
            continue
        # The distance along x we can travel from (s[0], y_check) while still
        # being in range of s.
        xComponent = dist - yComponent

        # The minimum and maximum x values covered by this sensor at y_check!
        seg = (s[0] - xComponent, s[0] + xComponent)    
        y_visible.append(seg)

    # Now that we know which segments of y are covered by our sensors, we need
    # to check them for overlap to avoid double counting:
    segs = sorted(y_visible, key=lambda x: x[0])
    cleanPass = False
    while not cleanPass:
        cleanPass = True
        i = 1
        while i < len(segs):
            # We know that segs[i] starts later than or equal to when segs[i-1] 
            # starts. So if segs[i][0] <= segs[i-1][1] the two can be merged.
            if segs[i][0] <= segs[i-1][1]:
                # Our sort doesn't guarantee that the y values get progressively
                # higher, so if we merge, grab the biggest y we from the pair
                merge = (segs[i-1][0], max(segs[i-1][1], segs[i][1]))
                segs[i-1] = merge
                segs.remove(segs[i])
                cleanPass = False
                i -= 1  # Decrement so that we check this i again
            i += 1

    # Now we check if any beacons or sensors are directly within the portions of
    # the line that the sensors see:
    equipmentSeen = 0
    for b in beacons:
        if b[1] != y_check:
            continue
        for seg in segs:
            if b[0] >= seg[0] and b[0] <= seg[1]:
                equipmentSeen += 1
                break
    for s in sensors:
        if s[1] != y_check:
            continue
        for seg in segs:
            if s[0] >= seg[0] and s[0] <= seg[1]:
                equipmentSeen += 1
                break

    total_seen = sum([seg[1]-seg[0]+1 for seg in segs])
    total_seen -= equipmentSeen

    au.printWrapped(f"The number of positions on the y={y_check} row that were "
                    "visible to at least one sensor and have no equipment is "
                    f"{total_seen}")

    au.printBanner("PART TWO - NEGATIVE SPACE: <Now, we need to find the"
                   " only space in the rectanlge bounded (by 0,0) and (4000000,"
                   "4000000) that the beacon can be in.>")

    # Okay, using that last solution as inspiration: What if we created an array
    # of all y values, and instead of calculating the x coverage for each beacon
    # and then merging them all, we merge each beacon's coverage into the list
    # as we go?
    #
    # 4 million is a lot of lines to do iterations over though. And we'd have to
    # iterate over 4 million lines 25 times (so 100,000,000 operations at least)

    coverage = {i:[] for i in range(y_part_2+1)}
    sInd = 1
    grid = {}
    for s in sensors:
        profiler = time.time()
        dist = au.manhattanDistance(s, closest[s])
        xComp = 0   # The distance along the x axis that is in range from y.
        # Look along all y's we cover partially and add our contribution
        for y in range(s[1]-dist, s[1]+dist+1):
            # If we've fully covered the current y already, skip it. 
            if coverage.get(y, None) is None:
                xComp += 1 if y < s[1] else -1  # But don't forget xComp
                continue

            # Otherwise, update this y's coverage with our current coverage.
            thisCoverage = (max(s[0]-xComp,0), min(s[0]+xComp, y_part_2))
            combine(coverage[y], thisCoverage, y_part_2)

            # If coverage is now complete on this y, remove it to save time (?)
            if coverage[y] == [(0,y_part_2)]:
                coverage.pop(y)
        
            # The x component gets bigger towards y=s[1], then shrinks again
            xComp += 1 if y < s[1] else -1

        # For my own edification, to track performance as we go because I don't 
        # trust this algorithm.
        profiler = time.time() - profiler
        print(f"It took {round(profiler,3)} seconds to process coverage for the"
              f" sensor {sInd}.")
        sInd += 1

    # If I did this right, there's only a single index left in coverage, and the
    # space between it's two elements should be our beacon:
    au.printWrapped("\nOoooh boy. Moment of truth. There should only be one ind"
                    "ex in the coverage matrix now. The actual number of indice"
                    f"s is: {len(coverage)}.\n")
    input("Continue? (If that didn't say 1, bail, because I failed)")
    final_coverage = [c for c in coverage.values() if c != []][0]
    print(f"The coverage list is: {final_coverage}\n")
    final_x = final_coverage[0][1]+1
    final_y = [y for y in coverage.keys() if coverage[y] != []][0]
    print(f"That would mean that the beacon is at: {(final_x, final_y)}\n")
    freq = final_x * 4000000 + final_y    
    print(f"Which means the tuning frequency is {freq}")



def combine(seglist, seg, bound):
    # If there's nothing to merge with, fahgedaboudit
    if not len(seglist):
        seglist.append(seg)
        return
    # Also, if it's full, fahgedaboudit then, too
    if seglist == [(0,bound)]:
        return


    # Attempts to add the segment into the list. If the segment overlaps with 
    # one or more segments in the list, it's integrated with them.
    i = 0
    wasInserted = False
    while i < len(seglist):
        merger = [seglist[i][0], seglist[i][1], seg[0], seg[1]]
        merger = sorted(merger)

        if seglist[i][0] > seg[1]:
            # This segment doesn't overlap, and should occur after our new seg 
            # in the list
            seglist.insert(i, seg)
            wasInserted = True
            break

        # If the middle pieces are equal then we know that the segments were 
        # either contiguous, or one was a singleton contained within the
        # other. Either way it's a merge
        midEq = merger[1] == merger[2] or merger[2] == merger[1] + 1
        if seg in [(merger[0],merger[1]), (merger[2],merger[3])] and not midEq:
            # If we get here, we weren't overlapped/sharing elements, so we know
            # that the segment has nothing in common with seglist[i]
            i += 1
            continue
        else:
            # In all other cases, there's at least some overlap, so we merge.
            # Remove the old one, replace the piece we're adding to the list, 
            # and keep i as the same value; it now points to the next segment
            seglist.pop(i)
            seg = (merger[0], merger[3])
    
    # If we're still holding onto the segment, it belongs at the end of the 
    # current version of the list. 
    if not wasInserted:
        seglist.append(seg)

    



    


