from collections import deque
import math
from typing import Dict, List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import PriorityQueue

data = read_entire_input(2019,18)

def parse(data: List[str]) -> Any:
    points = {}
    landmarks = {}
    for r, row in enumerate(data):
        for c, val in enumerate(row):
            if val == "@":
                start = (c,r)
            elif val.isalpha():
                landmarks[(c,r)] = val
                landmarks[val]=(c,r)
            points[(c,r)] = val
    return points, landmarks, start

def dim(points):
    return max(p[0] for p in points), max(p[1] for p in points)

# def build_graph(points, landmarks, start):
#     W,H = dim(points)
#     frontier = PriorityQueue()
#     frontier.put(start, 0)
#     targets = {}
#     while not frontier.empty():
#         c = frontier.get()
#         for n in neighbours(*c, W,H):
            

def flood_fill(points, targets, start):
    W, H = dim(points)
    frontier = deque()
    frontier.append((start, 0))
    visited = []
    while frontier:
        node, cost = frontier.popleft()
        visited.append(node)
        for neighbour in neighbours(*node):
            pass


def neighbours(x,y,W,H):
    if x > 0:
        yield x-1, y
    if x < W:
        yield x+1, y
    if y > 0:
        yield x, y-1
    if y < H:
        yield x, y+1

def cost(from_point, to_point, points: Dict[tuple, str], visited):
    if points[to_point] == ".":
        return 1
    if points[to_point].isupper():
        if points[to_point] in visited:
            return 1
        else:
            return math.inf

@solution_timer(2019,18,1)
def part_one(data: List[str]):
    _ = parse(data)

    return False

@solution_timer(2019,18,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2019,18)
    part_one(data)
    part_two(data)