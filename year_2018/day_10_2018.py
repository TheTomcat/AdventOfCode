from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

import re
import math

data = read_entire_input(2018,10)
test = """position=< 9,  1> velocity=< 0,  2>
position=< 7,  0> velocity=<-1,  0>
position=< 3, -2> velocity=<-1,  1>
position=< 6, 10> velocity=<-2, -1>
position=< 2, -4> velocity=< 2,  2>
position=<-6, 10> velocity=< 2, -2>
position=< 1,  8> velocity=< 1, -1>
position=< 1,  7> velocity=< 1,  0>
position=<-3, 11> velocity=< 1, -2>
position=< 7,  6> velocity=<-1, -1>
position=<-2,  3> velocity=< 1,  0>
position=<-4,  3> velocity=< 2,  0>
position=<10, -3> velocity=<-1,  1>
position=< 5, 11> velocity=< 1, -2>
position=< 4,  7> velocity=< 0, -1>
position=< 8, -2> velocity=< 0,  1>
position=<15,  0> velocity=<-2,  0>
position=< 1,  6> velocity=< 1,  0>
position=< 8,  9> velocity=< 0, -1>
position=< 3,  3> velocity=<-1,  1>
position=< 0,  5> velocity=< 0, -1>
position=<-2,  2> velocity=< 2,  0>
position=< 5, -2> velocity=< 1,  2>
position=< 1,  4> velocity=< 2,  1>
position=<-2,  7> velocity=< 2, -2>
position=< 3,  6> velocity=<-1, -1>
position=< 5,  0> velocity=< 1,  0>
position=<-6,  0> velocity=< 2,  0>
position=< 5,  9> velocity=< 1, -2>
position=<14,  7> velocity=<-2,  0>
position=<-3,  6> velocity=< 2, -1>""".split("\n")

def parse(data: List[str]) -> Any:
    pattern = r'position=<\s*(-*\d+),\s+(-*\d+)> velocity=<\s*(-*\d+),\s+(-*\d+)>'
    matcher = re.compile(pattern)
    positions = []
    velocities = []
    for line in data:
        x,y,vx,vy = [int(i) for i in matcher.search(line).groups()]
        positions.append([x,y])
        velocities.append([vx,vy])
    return positions, velocities

def find_bbox(positions):
    xmin,xmax,ymin,ymax = 0,0,0,0
    for x,y in positions:
        xmin = min(xmin, x)
        xmax = max(xmax, x)
        ymin = min(ymin, y)
        ymax = max(ymax, y)
    return xmin,xmax,ymin,ymax

def calculate_area(bbox):
    return (bbox[1]-bbox[0]) * (bbox[3]-bbox[2])

def render(particles, extrema=None):
    if extrema is None:
        extrema = find_bbox(particles)
    xmin,xmax,ymin,ymax = extrema
    print(f"Area: {calculate_area(extrema)}")
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            print('#' if [x,y] in particles else '.', end='')
        print()

def calculate_approx_location(positions, velocities):
# https://web.archive.org/web/20170912055605/http://cal.cs.illinois.edu/~johannes/research/LS_line_intersect.pdf
    # Calculate R = sum(1->K) I - v.vT
    # Calculate q = sum(1->K) (I - V.VT) . x
    
    R = [[0,0],[0,0]] # [[A,B], [C,D]] -> [A,B,C,D]
    q = [[0],[0]]

    from numpy import matrix
    from numpy.linalg import pinv

    for (x,y),(vx,vy) in zip(positions, velocities):
        R[0][0] += 1-vx*vx 
        R[0][1] += - vx*vy
        R[1][0] += - vx*vy
        R[1][1] += 1-vy*vy
        q[0][0] += (1-vx*vx)*x - vx*vy*y
        q[1][0] += (1-vx*vx)*y - vx*vy*x
    
    p = pinv(matrix(R)) @ matrix(q)
    return p[0][0].item(), p[1][0].item()

def calculate_avg_time_to_position(positions, velocities, point):
    Ts = []
    gx,gy = point
    for ((x,y),(vx,vy)) in zip(positions, velocities):
        t = (-x*gx-y*gy) / (vx*gx+vy*gy)
        Ts.append(t)

    return Ts

def step(positions, velocities):
    bbox = [0,0,0,0]
    new_positions = [[0,0] for i in positions]
    for i, ((x,y),(vx,vy)) in enumerate(zip(positions, velocities)):
        new_positions[i][0] = x + vx
        new_positions[i][1] = y + vy
        bbox[0] = min(bbox[0],x)
        bbox[1] = max(bbox[1],x)
        bbox[2] = min(bbox[2],y)
        bbox[3] = max(bbox[3],y)
    return new_positions, bbox

@solution_timer(2018,10,1)
def part_one(data: List[str], verbose=False):
    positions, velocities = parse(data)
    gx, gy = calculate_approx_location(positions, velocities)
    Ts = calculate_avg_time_to_position(positions, velocities, (gx,gy))
    

    # bbox = find_bbox(positions)
    # area = calculate_area(bbox)
    # #new_area = area
    # areas = [area]
    # converging = True
    # while converging:
    #     new_positions, new_bbox = step(positions, velocities)
    #     new_area = calculate_area(new_bbox)
    #     #converging = False
    #     print(f"New Area: {new_area} vs old {area} vs min {areas}")
    #     render(positions)
    #     input()
    #     if new_area <= min(areas):
    #         converging = True
    #         areas.append(new_area)
    #     if not converging:
    #         render(positions)
    #         break
    #     positions = new_positions
    #     area = new_area

        # if verbose:
        #     render(new_positions, new_bbox)
        #     input()

        # if new_area > area:
        #     render(positions, bbox)
        #     break
        # else:
        #     if verbose:
        #         render(new_positions, new_bbox)
        #         input()
        #     positions = new_positions
        #     area = new_area
        #     bbox = new_bbox

        # if area < new_area:
        #     # print(f'area: {new_area} ({area})')
        #     render(positions, bbox)
        #     #input()
        #     break
        # positions = new_positions
        # if verbose:
        #     print(f'area: {new_area}')
        #     render(positions, bbox)
        #     input()
        # area = new_area
        # new_positions, bbox = step(positions, velocities)
        # new_area = calculate_area(bbox)
    return False

@solution_timer(2018,10,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2018,10)
    part_one(data)
    part_two(data)