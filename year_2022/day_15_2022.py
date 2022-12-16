from collections import defaultdict, deque
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

import re
import math
import tqdm

from lib.shared import overlap

data = read_entire_input(2022,15)
test = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3""".split("\n")

def parse(data: List[str]) -> Any:
    pattern = r'Sensor at x=(-*\d+), y=(-*\d+): closest beacon is at x=(-*\d+), y=(-*\d+)'
    matcher = re.compile(pattern)
    sensor_data = []
    #bounds = [math.inf, 0, math.inf, 0]
    for line in data:
        sx,sy,bx,by = [int(i) for i in matcher.search(line).groups()]
        sensor_data.append((sx,sy,bx,by))
        # bounds[0] = min(bounds[0], sx, bx)
        # bounds[1] = max(bounds[1], sx, bx)
        # bounds[2] = min(bounds[2], sy, by)
        # bounds[3] = max(bounds[3], sy, by)
    return sensor_data#, bounds

def d(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

class Range:
    def __init__(self, a, b):
        self.start = min(a,b)
        self.end = max(a,b)
    def __add__(self, other: 'Range'):
        if self.overlap(other):
            return Range(min(self.start, other.start), max(self.end, other.end))
    def overlap(self, other: 'Range'):
        return overlap(self.start, self.end, other.start, other.end)
    def __len__(self):
        return self.end - self.start + 1
    def __repr__(self):
        return f'Range({self.start},{self.end})'

def calculate_range(sensor_data, target_row):
    ranges = []
    #right_x = []
    #low, high = math.inf,0
    for sx,sy,bx,by in sensor_data:
        r = d((sx,sy),(bx,by))
        dy = abs(sy-target_row)
        dx = r - dy
        # print(f"Examining sensor {sx, sy}, {r} away from beacon {bx, by} and a height of {dy} ({dx}). ", end="")
        ranges.append(Range(sx-dx, sx+dx))
        # print(f'{ranges[-1]}')
        #low = min(low, sx-dx)
        #high = max(high, sx+dx)
        #left_x.append(sx-dx)
        #right_x.append(sx+dx)
    return ranges#, low, high # left_x, right_x

def consolidate_ranges(ranges):
    ranges.sort(key=lambda x: x.start)
    ranges = deque(ranges)
    i=0
    while i+1 < len(ranges):
        a = ranges.popleft()
        b = ranges.popleft()
        # print(f'Index {i} - comparing {a} and {b} ->', end="")
        if c:=a+b:
            # print(f" Joining to make {c}", end="")
            ranges.appendleft(c)
        else:
            # print(f" Distinct, leaving alone. ", end="")
            ranges.extendleft([a,b])
            i += 1
        # input()
    return ranges

@solution_timer(2022,15,1)
def part_one(data: List[str], verbose=False):
    sensor_data = parse(data)
    target_row = 2000000
    ranges = calculate_range(sensor_data, target_row)
    beacons = set((x,y) for _,_,x,y in sensor_data if y==target_row)
    num_beacons = len(beacons)#list(filter(lambda sd: sd[1]==target_row, beacons)))
    ranges = consolidate_ranges(ranges)
    return sum(len(r) for r in ranges) - num_beacons

# @solution_timer(2022,15,2, 'brute')
# def part_two(data: List[str], verbose=False):
#     sensor_data = parse(data)
#     for target_row in tqdm.trange(0,4000001):
#         ranges = calculate_range(sensor_data, target_row)
#         #beacons = set((x,y) for _,_,x,y in sensor_data)
#         #num_beacons = len(list(filter(lambda sd: sd[1]==target_row, beacons)))
#         ranges = consolidate_ranges(ranges)
#         if len(ranges) > 1:
#             print(ranges)
    #return sum(len(r) for r in ranges) - num_beacons

def iterate_outside(sx,sy,bx,by,bbox):
    r = d((sx,sy),(bx,by)) + 1
    dy = 0 # sy
    x_start = max(bbox[0], sx-r)
    x_finish = min(bbox[1], sx+r)
    for x in range(x_start, x_finish+1):
        dy = r - abs(x-sx)
        y_top = sy + dy
        if bbox[2] <= y_top <= bbox[3]:
            yield x, y_top
        y_bot = sy - dy
        if bbox[2] <= y_bot <= bbox[3] and y_bot != sy:
            yield x, y_bot # sy + dy
        if x >= sx:
            dy -= 1
        else:
            dy += 1

@solution_timer(2022,15,2)
def part_two(data: List[str], verbose=False):
    sensor_data = parse(data)
    #outside = defaultdict(int)

    data_with_radius = [(sd, d([sd[0],sd[1]],[sd[2],sd[3]])) for sd in sensor_data]

    for sensor in sensor_data:
        if verbose:
            print(sensor)
        for point in iterate_outside(*sensor, (0,4000000,0,4000000)):
            for (sx,sy,bx,by),r in data_with_radius:
                if sensor == (sx,sy,bx,by):
                    continue
                if d(point, (sx,sy)) <= r:
                    break
            else:
                return point[0]*4000000 + point[1]

if __name__ == "__main__":
    data = read_entire_input(2022,15)
    part_one(data)
    part_two(data)