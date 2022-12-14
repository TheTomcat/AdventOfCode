from collections import Counter
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from util.shared import SpiralIterator
from framework.console import console

data = read_entire_input(2018,6)
test = """1, 1
1, 6
8, 3
3, 4
5, 5
8, 9""".split("\n")

def parse(data: List[str]) -> Any:
    coords = []
    W, H = 0,0
    for row in data:
        coords.append(tuple([int(i) for i in row.split(', ')]))
        W = max(W, coords[-1][0])
        H = max(H, coords[-1][1])
    return coords, W, H

def CCW(p1, p2, p3):
	return (p3[1]-p1[1])*(p2[0]-p1[0]) - (p2[1]-p1[1])*(p3[0]-p1[0])


def compute_convex_hull(points):
    hull = []
    points.sort()
    start = points[0]
    hull.append(start)
    
    def get_ordering(p):
        if p[0] == start[0]:
            return float('inf'), -p[1], p[0]
        else:
            return (start[1]-p[1]) / (start[0]-p[0]), -p[1], p[0]

    points.sort(key=get_ordering)
    #print(points)
    for p in points:
        hull.append(p)
        while len(hull) > 2 and CCW(hull[-3], hull[-2], hull[-1]) < 0:
            hull.pop(-2)
    return hull

def md(point1, point2):
    return abs(point1[0]-point2[0]) + abs(point1[1]-point2[1])

@solution_timer(2018,6,1)
def part_one(data: List[str], verbose=False):
    coords,W,H = parse(data)
    hull = compute_convex_hull(coords)
    areas = Counter()

    for y in range(H+1):
        for x in range(W+1):
            distance_to_points = sorted([(md((x,y),point), point) for point in coords])
            if len(distance_to_points) == 1 or distance_to_points[0][0] != distance_to_points[1][0]:
                areas[distance_to_points[0][1]] += 1
    return max(size for point, size in areas.items() if point not in hull)
    
@solution_timer(2018,6,2)
def part_two(data: List[str], verbose=False):
    coords,W,H = parse(data)
    region = 0
    for y in range(H+1):
        for x in range(W+1):
            dist_to_points = sum(md((x,y), point) for point in coords) < 10000
            region += dist_to_points 
    return region

if __name__ == "__main__":
    data = read_entire_input(2018,6)
    part_one(data)
    part_two(data)