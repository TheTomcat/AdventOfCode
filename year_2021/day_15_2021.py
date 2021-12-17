import enum
from typing import List, Any, Tuple, TypeVar, Dict
import math
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console
from util.shared import PriorityQueue


data = read_entire_input(2021,15)
test = """1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581""".split('\n')

def parse(data: List[str]) -> Any:
    return [[int(i) for i in row] for row in data]

def dim(data):
    return len(data[0]), len(data)

def build_graph(risk_grid):
    output = {}
    for r, row in enumerate(risk_grid):
        for c, risk in enumerate(row):
            output[(c,r)] = risk
    return output

def neighbours(x,y,W,H):
    if 0 < x:
        yield x-1, y
    if x < W-1:
        yield x+1, y 
    if 0 < y:
        yield x, y-1
    if y < H-1:
        yield x, y+1

def d(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def a_star(data, start, goal):
    risk = build_graph(data)
    W,H = dim(data)
    frontier = PriorityQueue()
    frontier.put(start, 0)
    came_from: Dict = {}
    cost_so_far: Dict[Tuple[int,int], float] = {}
    came_from[start] = None
    cost_so_far[start] = 0
    while not frontier.empty():
        current = frontier.get()
        #console.print(f"Examining point {current} - ", end="")
        if current == goal:
            break
        for neighbour in neighbours(*current, W, H):
            #console.print(f"[yellow] NGH {neighbour} ({risk[neighbour]}) ", end="")
            new_cost = cost_so_far[current] + risk[neighbour]
            if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
                cost_so_far[neighbour] = new_cost
                priority = new_cost + d(neighbour, goal)
                frontier.put(neighbour, priority)
                came_from[neighbour] = current
        # i = input()
    return came_from, cost_so_far

def expand(risk_grid, factor = 5):
    rg = []
    for rowfactor in range(factor):
        for r, row in enumerate(risk_grid):
            rgr = []
            for colfactor in range(factor):
                for c, risk in enumerate(row):
                    rgr.append((risk + rowfactor + colfactor-1) % 9 + 1)
            rg.append(rgr)
    return rg
    #return [[i for i in row] for row in data]

@solution_timer(2021,15,1)
def part_one(data: List[str]):
    risk_grid = parse(data)
    _, cost = a_star(risk_grid, (0,0), (99,99))
    return cost[(99,99)]

@solution_timer(2021,15,2)
def part_two(data: List[str]):
    risk_grid = parse(data)
    expanded_risk_grid = expand(risk_grid)
    _, cost = a_star(expanded_risk_grid, (0,0), (499,499))
    return cost[(499,499)]

if __name__ == "__main__":
    data = read_entire_input(2021,15)
    part_one(data)
    part_two(data)