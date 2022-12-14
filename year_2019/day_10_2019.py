import math
from typing import List, Any, Tuple
from math import gcd
from collections import defaultdict
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2019,10)

def parse(data: List[str]) -> Any:
    asteroids = []
    for i, row in enumerate(data):
        for j, x in enumerate(row):
            if x == "#":
                asteroids.append((j,i))
    return asteroids

def sgn(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    else:
        return 0

def dist_to_station(station):
    return lambda x: (station[0]-x[0])**2 + (station[1]-x[1])**2

def get_gradient(p, q):
    dx = p[0]-q[0]
    dy = p[1]-q[1]
    if dx == 0 or dy==0:
        return (sgn(dx),sgn(dy))
    G = abs(gcd(dx,dy))
    return (int(dx/G), int(dy/G))

def count_visible_asteroids(station_location, asteroids):
    gradients = defaultdict(list)
    for asteroid in asteroids:
        if station_location == asteroid:
            continue
        g = get_gradient(asteroid, station_location)
        gradients[g].append(asteroid)
    return gradients

def compute_station_locations(asteroids):
    output = []
    for station_location in asteroids:
        visible = count_visible_asteroids(station_location, asteroids)
        output.append((station_location, len(visible)))
    return output

def build_asteroid_map(station_locations, data):
    output = [['.' for pos in row] for row in data]
    for (x,y), asteroids in station_locations:
        output[y][x] = asteroids
    return output

def big_laser(station, asteroids):
    destroyed = []
    gradients = count_visible_asteroids(station, asteroids)
    
    ordered_gradients = sorted(gradients.keys(), key=lambda x: math.atan2(-x[0],x[1]))
    if (0,-1) in ordered_gradients:
        ordered_gradients.remove((0,-1))
        ordered_gradients = [(0,-1)] + ordered_gradients
    
    active = True
    while active:
        active=False
        for gradient in ordered_gradients:
            gradients[gradient].sort(key=dist_to_station(station))
            if len(gradients[gradient])>0:
                dest = gradients[gradient].pop(0)
                destroyed.append(dest)
                active=True
    return destroyed

@solution_timer(2019,10,1)
def part_one(data: List[str], verbose=False):
    asteroids = parse(data)
    output = compute_station_locations(asteroids)
    return max(output, key=lambda x: x[1])

@solution_timer(2019,10,2)
def part_two(data: List[str], verbose=False):
    asteroids = parse(data)
    output = compute_station_locations(asteroids)
    station = max(output, key=lambda x: x[1])[0]
    destroyed = big_laser(station, asteroids)
    return destroyed[199][0]*100+destroyed[199][1]
if __name__ == "__main__":
    data = read_entire_input(2019,10)
    part_one(data)
    part_two(data)

test = """.#....#####...#..
##...##.#####..##
##...#...#.#####.
..#.....#...###..
..#.#.....#....##""".split("\n")
p = (3,8)