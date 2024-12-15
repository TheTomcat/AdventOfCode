import math
from typing import List, Any, Tuple
from framework.helpers import solution_timer, solution_profiler
from framework.input_helper import read_entire_input

from itertools import product

from lib.graph.pathfinding import search

data = read_entire_input(2022,18)
test = """2,2,2
1,2,2
3,2,2
2,1,2
2,3,2
2,2,1
2,2,3
2,2,4
2,2,6
1,2,5
3,2,5
2,1,5
2,3,5""".split("\n")

def parse(data: List[str]) -> Any:
    obsidian = []
    for line in data:
        x,y,z = line.split(",")
        obsidian.append((int(x),int(y),int(z)))
    return set(obsidian) # Returning as a set makes the part two time from 1400ms to 40ms. Amazing 

def get_bbox(obsidian):
    x0,x1,y0,y1,z0,z1 = math.inf,0,math.inf,0,math.inf,0
    for x,y,z in obsidian:
        x0 = min(x0, x)
        y0 = min(y0, y)
        z0 = min(z0, z)
        x1 = max(x1, x)
        y1 = max(y1, y)
        z1 = max(z1, z)
    return (x0,x1),(y0,y1),(z0,z1)

@solution_timer(2022,18,1)
def part_one(data: List[str], verbose=False):
    obsidian = parse(data)
    # bbox = get_bbox(obsidian)
    # X = bbox[0][1]-bbox[0][0]+1
    # Y = bbox[1][1]-bbox[1][0]+1
    # Z = bbox[2][1]-bbox[2][0]+1
    # return (X*Y+Y*Z+Z*X)*2
    count=0
    for x,y,z in obsidian:
        for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            if (x+dx, y+dy, z+dz) not in obsidian:
                count += 1
    return count

@solution_timer(2022,18,2)
def part_two(data: List[str], verbose=False):
    obsidian = parse(data)
    count=0
    bbox = get_bbox(obsidian)
    start = (bbox[0][0]-1, bbox[1][0]-1, bbox[2][0]-1)
    in_range = lambda x,y,z: bbox[0][0]-1 <= x <= bbox[0][1]+1 and bbox[1][0]-1 <= y <= bbox[1][1]+1 and bbox[2][0]-1 <= z <= bbox[2][1]+1
    adj = lambda p: (((p[0]+dx,p[1]+dy,p[2]+dz),0 )for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)] if (p[0]+dx,p[1]+dy,p[2]+dz) not in obsidian and in_range(p[0]+dx, p[1]+dy, p[2]+dz))
    BFS, _ = search(start, adj)
    for x,y,z in obsidian:      
        for dx,dy,dz in [(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]:
            if (x+dx, y+dy, z+dz) not in obsidian and (x+dx, y+dy, z+dz) in BFS:
                count += 1
    return count

if __name__ == "__main__":
    data = read_entire_input(2022,18)
    part_one(data)
    part_two(data)