from typing import List, Any, Tuple
from collections import deque
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2021,9)
test = """2199943210
3987894921
9856789892
8767896789
9899965678""".split('\n')

def parse(data: List[str]) -> Any:
    height_map = {}
    for y, row in enumerate(data):
        for x, digit in enumerate(row):
            height_map[(x,y)] = int(digit)
    HEIGHT = len(data)
    WIDTH = len(data[0])
    return height_map, WIDTH, HEIGHT

def neighbours(x,y, WIDTH, HEIGHT):
    for dx in [-1,1]:
        if not 0 <= x + dx < WIDTH:
            continue
        yield x+dx, y
    for dy in [-1, 1]:
        if not 0 <= y + dy < HEIGHT:
            continue
        yield x, y+dy

def find_minima(height_map, WIDTH, HEIGHT):
    minima = []
    for x in range(WIDTH):
        for y in range(HEIGHT):
            points = [height_map[(X,Y)] for X,Y in neighbours(x,y,WIDTH,HEIGHT)]
            if height_map[(x,y)] < min(points):
                minima.append((x,y))
    return minima

def flood_fill(height_map, WIDTH, HEIGHT, start):
    basin = [start]
    edges = deque()
    edges.append(start)
    while len(edges) > 0:
        p = edges.popleft()
        for neighbour in neighbours(*p, WIDTH, HEIGHT):
            if neighbour in basin:
                continue
            if height_map[neighbour] > height_map[p] and height_map[neighbour] != 9:
                basin.append(neighbour)
                edges.append(neighbour)
    return basin

@solution_timer(2021,9,1)
def part_one(data: List[str], verbose=False):
    height_map, W, H = parse(data)
    minima = find_minima(height_map, W, H)
    return sum(height_map[i]+1 for i in minima)

@solution_timer(2021,9,2)
def part_two(data: List[str], verbose=False):
    height_map, W, H = parse(data)
    minima = find_minima(height_map, W, H)
    basins = {}
    for minimum in minima:
        basins[minimum] = len(flood_fill(height_map, W, H, minimum))
    x,y,z = sorted(basins.values(),reverse=True)[0:3]
    return x*y*z

if __name__ == "__main__":
    data = read_entire_input(2021,9)
    part_one(data)
    part_two(data)