from typing import List, Any, Tuple
import re
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import overlap

data = read_entire_input(2021,22)

def parse(data: List[str]) -> Any:
    output = []
    for row in data:
        m = re.match(r'(on|off) x=(-?\d+)..(-?\d+),y=(-?\d+)..(-?\d+),z=(-?\d+)..(-?\d+)', row)
        i = m.groups()
        output.append((1 if i[0] == 'on' else 0, [int(j) for j in i[1:]]))
    return output

def intersection(bbox1, bbox2):
    """Return the intersection of bounding boxes, or False if no intersection
    """
    xmin1, xmax1, ymin1, ymax1, zmin1, zmax1 = bbox1
    xmin2, xmax2, ymin2, ymax2, zmin2, zmax2 = bbox2
    xol = overlap(xmin1, xmax1, xmin2, xmax2) 
    yol = overlap(ymin1, ymax1, ymin2, ymax2)
    zol = overlap(zmin1, zmax1, zmin2, zmax2)
    if xol and yol and zol:
        return (max(xmin1, xmin2), min(xmax1, xmax2), 
                max(ymin1, ymin2), min(ymax1, ymax2),
                max(zmin1, zmin2), min(zmax1, zmax2))
    return False

def size(bbox):
    xmin, xmax, ymin, ymax, zmin, zmax = bbox
    return (xmax-xmin+1) * (ymax-ymin+1) * (zmax-zmin+1)

def update_state(states: List, instruction):
    onoff, bbox = instruction
    correction = []
    for status, s_bbox in states: # Loop over the current states
        if intersecting_box := intersection(bbox, s_bbox): # If intersection
            correction.append((-status, intersecting_box)) # Cancel out that intersecting box
            # (if the lights are already on!)
    if onoff: # Do the instruction
        states.append(instruction)
    states.extend(correction) # Apply all the corrections
    return states

def count_on(states):
    tot = 0
    for state, bbox in states:
        if state:
            tot += state * size(bbox) # State is either 0 - off, 1 - on, -1 "off = on-turned-off"
    return tot

@solution_timer(2021,22,1)
def part_one(data: List[str], verbose=False):
    boot_instructions = parse(data)
    states = []
    for instruction in boot_instructions[:20]:
        states = update_state(states, instruction)
    return count_on(states)

@solution_timer(2021,22,2)
def part_two(data: List[str], verbose=False):
    boot_instructions = parse(data)
    states = []
    for instruction in boot_instructions:
        states = update_state(states, instruction)
    return count_on(states)

if __name__ == "__main__":
    data = read_entire_input(2021,22)
    part_one(data)
    part_two(data)


# ============================

def loop_over(instruction):
    _, (xmin, xmax, ymin, ymax, zmin, zmax) = instruction
    for x in range(xmin, xmax+1):
        for y in range(ymin, ymax+1):
            for z in range(zmin, zmax+1):
                yield x,y,z

def update_state_brute_force(state, instruction):
    op, (xmin, xmax, ymin, ymax, zmin, zmax) = instruction
    if op == "on":
        for x,y,z in loop_over(instruction):
            state[(x,y,z)] = True
    else:
        for x,y,z in loop_over(instruction):
            if (x,y,z) in state:
                del state[(x,y,z)]
