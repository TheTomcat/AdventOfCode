from typing import List
from collections import defaultdict

from framework.console import console
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2021,5)

test = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2""".split("\n")

def parse(data):
    vents = []
    for row in data:
        coords = row.replace(" -> ",",").split(",")
        vents.append([int(i) for i in coords])
    return vents

def horizontal(line):
    return line[1] == line[3]

def vertical(line):
    return line[0]==line[2]

def diagonal(line):
    return abs(line[0]-line[2]) == abs(line[1]-line[3])

def step_over(line, includ_diags=False):
    if horizontal(line):
        # vary x
        x1,x2 = sorted([line[0],line[2]])
        for x in range(x1,x2+1):
            yield x, line[1]
    elif vertical(line):
        y1,y2 = sorted([line[1],line[3]])
        for y in range(y1,y2+1):
            yield line[0],y
    elif diagonal(line) and includ_diags:
        p1, p2 = line[0:2],line[2:4]
        p1, p2 = sorted((p1,p2), key=lambda x: x[0])
        direction = 1 if p2[1] - p1[1] > 0 else -1
        length = p2[0]-p1[0] + 1
        for i in range(length):
            yield p1[0]+i, p1[1]+i*direction

@solution_timer(2021,5,1)
def part_one(data, verbose=False):
    lines = parse(data)
    grid = defaultdict(int)
    for line in lines:
        if horizontal(line):
            x1,x2 = sorted([line[0], line[2]])
            for x in range(x1, x2+1):
                grid[(x,line[1])] += 1
        elif vertical(line):
            y1,y2 = sorted([line[1], line[3]])
            for y in range(y1,y2+1):
                grid[(line[0],y)] += 1
    return sum([1 for i in grid.values() if i > 1])

@solution_timer(2021,5,2)
def part_two(data, verbose=False):
    lines = parse(data)
    grid = defaultdict(int)
    for line in lines:
        if horizontal(line) or vertical(line) or diagonal(line):
            for point in step_over(line, includ_diags=True):
                grid[point] += 1
    return sum([1 for i in grid.values() if i > 1])

if __name__ == "__main__":
    data = read_entire_input(2021,5)
    part_one(data)
    part_two(data)
