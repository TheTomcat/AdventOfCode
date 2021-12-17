from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import sgn
import re, math
data = read_entire_input(2021,17)

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
    return state[1] + (state[4] * (state[4]+1))/2

def will_be_in_box(state, bbox):
    x,y,vx,vy = state
    xmin,xmax,ymin,ymax = bbox
    j1 = (2*vx-1)/2 + math.sqrt((1-2*vx)**2-4*xmin)/2
    j2 = (2*vx-1)/2 +math.sqrt((1-2*vx)**2-4*xmax)/2
    if abs(j1-j2) < 1:
        return False
    maxh = max_height(state)

    
@solution_timer(2021,17,1)
def part_one(data: List[str]):
    bbox = parse(data)
    o = []
    for vx in range(0,30):
        for vy in range(0,100):
            maxh = max_height((0,0,vx,vy))

            # print(vx,vy, end="")
    #         state = (0,0,vx,vy)
    #         maxh = -100
    #         while not any(passed(state, bbox)):
    #             # print(".",end="")
    #             maxh = max(maxh, state[1])
    #             state = step(state)
    #             if within(state, bbox):
    #                 o.append(maxh)
    #         # print()
    # return max(o)

@solution_timer(2021,17,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,17)
    part_one(data)
    part_two(data)