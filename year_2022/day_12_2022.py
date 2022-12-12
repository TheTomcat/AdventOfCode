from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

from util.shared import render
from util.graph import search, construct_path
from util.console import console

data = read_entire_input(2022,12)
test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split("\n")

def parse(data: List[str]) -> Any:
    heightmap = {}
    for y, row in enumerate(data):
        for x, el in enumerate(row):
            heightmap[(x,y)] = el
            if el == "S":
                start = (x,y)
            if el == "E":
                end = (x,y)
    return heightmap, start, end

def elevation(char):
    elevation = "abcdefghijklmnopqrstuvwxyz"
    if char == "S":
        char = "a"
    if char == "E":
        char = "z"
    return elevation.index(char)

def render_function(path):
    def inner(point, points):
        if point in path:
            return f'[red]{points[point]}[/red]'
        else:
            return f'[green]{points[point]}[/green]'
    return inner

def neighbours1(heightmap):
    def inner(current):
        cur_el = elevation(heightmap[current])
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbour = current[0]+dx, current[1]+dy
            if neighbour not in heightmap:
                continue
            if elevation(heightmap[neighbour]) > cur_el + 1:
                # If the neighbour is greater than 1 higher than our position, we can't go there
                continue
            yield neighbour, 1
    return inner

@solution_timer(2022,12,1)
def part_one(data: List[str], verbose=False):
    heightmap, start, end = parse(data)

    path, end = search(start, neighbours=neighbours1(heightmap), end=lambda x: x==end, depth_first=True)
    
    reconstructed_path = construct_path(path, end)

    if verbose:
        im = render(heightmap, render_function=render_function(reconstructed_path))
        console.print(im)

    return len(reconstructed_path)-1

def neighbours2(heightmap):
    def inner(current):
        cur_el = elevation(heightmap[current])
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbour = current[0]+dx, current[1]+dy
            if neighbour not in heightmap:
                continue
            if elevation(heightmap[neighbour]) + 1 < cur_el:
                # If the neighbour is less than 1 lower than our position, we can't backtrack to this position
                continue
            yield neighbour, 1
    return inner

@solution_timer(2022,12,2)
def part_two(data: List[str], verbose=False):
    heightmap, _, start = parse(data)

    path, end = search(start, neighbours=neighbours2(heightmap), end=lambda x: elevation(heightmap[x])==0, depth_first=True)
    
    reconstructed_path = construct_path(path, end)

    if verbose:
        im = render(heightmap, render_function=render_function(reconstructed_path))
        console.print(im)

    return len(reconstructed_path)-1

if __name__ == "__main__":
    data = read_entire_input(2022,12)
    part_one(data)
    part_two(data)