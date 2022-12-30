import math
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

import re

from lib.graph.Graph import Graph

data = read_entire_input(2022,22)
test = """        ...#
        .#..
        #...
        ....
...#.......#
........#...
..#....#....
..........#.
        ...#....
        .....#..
        .#......
        ......#.

10R5L5R10L4R5L5
""".split("\n")

UP = (0,-1)
DOWN = (0,1)
LEFT = (-1,0)
RIGHT = (1,0)
F = {
    RIGHT:0, DOWN:1, LEFT:2, UP: 3
}

def parse(data: List[str]) -> Any:
    cells = {}    
    start = None
    for y, row in enumerate(data):
        if row and row[0] not in '.# ':
            break
        for x, cell in enumerate(row):
            if cell == ".":
                if start is None:
                    start = (x,y)
                cells[(x,y)] = '.'
            elif cell == "#":
                cells[(x,y)] = '#'
    for row in reversed(data[::-1]):
        if row and row[0].isdigit():
            elements = re.split('([LR])', row)
            break
    instructions = []
    for instruction in elements:
        instructions.append(int(instruction) if instruction.isdigit() else instruction)
    return cells, instructions, start, (x, y)

def move(instruction, position, facing, cells, cube_wrap=False):
    match instruction:
        case "L" | "R":
            # print(f"Turning {instruction}, ", end="")
            if instruction == "R":
                facing = -facing[1], facing[0]
            elif instruction == "L":
                facing = facing[1], -facing[0]
            # print(f"facing {facing}")
        case int(instruction):
            for i in range(instruction):
                nx, ny = position[0]+facing[0], position[1]+facing[1]
                if (nx,ny) in cells:
                    if cells[(nx,ny)] == ".":
                        position = nx,ny
                        # print(f"Moving {facing} to {position}")
                    elif cells[(nx,ny)] == "#":
                        # print("Hit a wall")
                        break
                else:
                    # print(f"Attempted moving to ({nx}, {ny}) Looping around... {position}")
                    if cube_wrap:
                        position, facing = cube_wrap(cells, position, facing)
                    else:
                        position = loop_around(cells, position, facing)
                    # print("asdf"

    return position, facing

def loop_around(cells, position, facing):
    backwards = -facing[0], -facing[1]
    x,y = position
    while (x,y) in cells and cells[(x,y)] != " ":
        x,y = x+backwards[0],y+backwards[1]
        # print(f" - ({x},{y})", end="")
    x,y = x-backwards[0], y-backwards[1] # One too far, take a step backwards
    if cells[(x,y)] == "#":
        # print(" - hit a wall!")
        return position
    # print()
    return (x,y)

@solution_timer(2022,22,1)
def part_one(data: List[str], verbose=False):
    cells, instructions, position, dim = parse(data)
    facing = RIGHT
    for instruction in instructions:
        position, facing = move(instruction, position, facing, cells)
    return 1000*(position[1]+1) + 4 * (position[0] + 1) + F[facing]

def convert_to_cube_map(cells, dim):
    side_length = int(math.sqrt(len(cells)/6))
    faces = {}
    for Y in range(dim[1]//side_length):
        for X in range(dim[0]//side_length):
            faces[(X,Y)] = {}
            for y in range(side_length):
                for x in range(side_length):
                    nx,ny = (X*side_length + x, Y*side_length+y)
                    if (nx,ny) in cells:
                        faces[(X,Y)][(x,y)] = cells[(nx,ny)]
    return faces

@solution_timer(2022,22,2)
def part_two(data: List[str], verbose=False):
    cells, instructions, position, dim = parse(data)
    side_length = math.sqrt(len(cells)/6)
    cube_map = Graph.from_adjacency_list({'A':['F','E','D','B'], })
    facing = RIGHT
    for instruction in instructions:
        position, facing = move(instruction, position, facing, cells)
    return 1000*(position[1]+1) + 4 * (position[0] + 1) + F[facing]

if __name__ == "__main__":
    data = read_entire_input(2022,22)
    part_one(data)
    part_two(data)