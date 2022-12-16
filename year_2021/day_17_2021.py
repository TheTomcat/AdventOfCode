from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.shared import sgn
import re, math
data = read_entire_input(2021,17)
test = ["target area: x=20..30, y=-10..-5"]

def parse(data: List[str]) -> Any:
    m = re.match(r'target area: x=(-?\d+)..(-?\d+), y=(-?\d+)..(-?\d+)',data[0])
    return [int(i) for i in m.groups()]

def step(state):
    x,y,vx,vy = state
    x += vx
    y += vy
    vx -= sgn(vx)
    vy -= 1
    return (x,y,vx,vy)

def within(state,bbox):
    x,y,_,_ = state
    xmin, xmax = sorted(bbox[:2])
    ymin, ymax = sorted(bbox[2:])
    return xmin <= x <= xmax, ymin <= y <= ymax

def passed(state,bbox):
    x,y,vx,vy = state
    xmin, xmax, ymin, ymax = bbox
    # undershotx
    undershotx = vx == 0 and not within(state, bbox)[0]
    # overshotx 
    overshotx = abs(x) >  max(abs(xmin), abs(xmax))
    # ybelow
    overshoty = abs(y) > max(abs(ymin), abs(ymax)) and y < 0
    return undershotx , overshotx , overshoty

def max_height(state):
    return state[1] + (state[3] * (state[3]+1))/2 if state[3]>0 else 0

def max_dist(state):
    return state[2]*(state[2]-1)/2

def en_route(state, bbox):
    x,y,vx,_ = state
    xmin,xmax, ymin,ymax = bbox
    return (sgn(vx) == sgn(xmax - x) or (vx==0 and xmin <= x <= xmax)) and y >= ymin

def will_be_in_box(state, bbox):
    x,y,vx,vy = state
    xmin,xmax,ymin,ymax = bbox
    j1 = (2*vx-1)/2 + math.sqrt((1-2*vx)**2-4*xmin)/2
    j2 = (2*vx-1)/2 +math.sqrt((1-2*vx)**2-4*xmax)/2
    if abs(j1-j2) < 1:
        return False
    maxh = max_height(state)

@solution_timer(2021,17,1)
def part_one(data: List[str], verbose=False):
    bbox = parse(data)
    vx0 = int(math.sqrt(2*bbox[0]))+1
    for vy in range(200,0,-1):
        for vx in range(vx0,30):
            state = (0,0,vx,vy)
            maxh = max_height((0,0,vx,vy))
            while not any(passed(state, bbox)):
                state = step(state)
                if all(within(state, bbox)):
                    return maxh#, vx, vy

@solution_timer(2021,17,2)
def part_two(data: List[str], verbose=False):
    bbox = parse(data)
    vx0 = int(math.sqrt(2*bbox[0]))+1
    c=set()
    for vx in range(vx0, bbox[1]+1):
        for vy in range(min(bbox[2:])-1,200):
            state = (0,0,vx,vy)
            while en_route(state, bbox):
                state = step(state)
                if all(within(state, bbox)):
                    c.add((vx,vy))
    return len(c)
    
if __name__ == "__main__":
    data = read_entire_input(2021,17)
    part_one(data)
    part_two(data)