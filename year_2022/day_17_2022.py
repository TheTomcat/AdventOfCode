from typing import List, Any, Tuple
from framework.helpers import solution_timer, solution_profiler
from framework.input_helper import read_entire_input

from itertools import cycle

from lib.shared import render

from tqdm import trange

data = read_entire_input(2022,17)
test = """>>><<><>><<<>><>>><<<>>><<<><<<>><>><<>>""".split("\n")

def parse(data: List[str]) -> Any:
    directions = []
    for row in data:
        for char in row:
            directions.append(char)
    return directions

rocks = [
    [(0,0),(1,0),(2,0),(3,0)],
    [(1,0),(0,1),(1,1),(2,1),(1,2)],
    [(0,0),(1,0),(2,0),(2,1),(2,2)],
    [(0,0),(0,1),(0,2),(0,3)],
    [(0,0),(0,1),(1,0),(1,1)]
]

next_rock = cycle(rocks)

directions = {
    ">":(1,0),
    "<":(-1,0)
}

def render(space, height):
    for y in range(height + 2, -1, -1):
        print("|", end="")
        for x in range(0,7):
            print('.' if (x,y) not in space else '#', end="")
        print("|")
    print('+-------+')

@solution_timer(2022,17,1)
def part_one(data: List[str], verbose=False):
    jets = parse(data)
    next_jet = cycle(iter(jets))
    space = {}

    num_rocks = 2022
    height = -1
    for i in range(num_rocks):
        init_x, init_y = 2, height+4
        rock = [(i+init_x,j+init_y) for i,j in next(next_rock)]
        # print(f"dropping rock {i}: {rock}")
        while True:
            jet = next(next_jet)
            move = directions[jet]
            test_pos = [(i+move[0],j+move[1]) for i,j in rock]
            # print(f"moving {jet} - {test_pos}")
            if all((x,y) not in space and 0 <= x <= 6  for x,y in test_pos):
                rock = test_pos
            # render(space, height)
            # input()
            move = (0,-1)
            test_pos = [(i+move[0],j+move[1]) for i,j in rock]
            # print(f"falling: {test_pos}")
            if all((x,y) not in space and y >= 0 for x,y in test_pos):
                rock = test_pos
            else:
                # print("settled")
                for x,y in rock:
                    space[(x,y)] = i
                    height = max(height, y)
                break
            # render(space, height)
            # input()
    return height+1

@solution_profiler(2022,17,2)
def part_two(data: List[str], verbose=False):
    jets = parse(data)
    next_jet = cycle(iter(jets))
    space = {}

    num_rocks = 1000000
    height = -1
    for i in trange(num_rocks):
        init_x, init_y = 2, height+4
        rock = [(i+init_x,j+init_y) for i,j in next(next_rock)]
        # print(f"dropping rock {i}: {rock}")
        while True:
            jet = next(next_jet)
            move = directions[jet]
            test_pos = [(i+move[0],j+move[1]) for i,j in rock]
            # print(f"moving {jet} - {test_pos}")
            if all((x,y) not in space and 0 <= x <= 6  for x,y in test_pos):
                rock = test_pos
            # render(space, height)
            # input()
            move = (0,-1)
            test_pos = [(i+move[0],j+move[1]) for i,j in rock]
            # print(f"falling: {test_pos}")
            if all((x,y) not in space and y >= 0 for x,y in test_pos):
                rock = test_pos
            else:
                # print("settled")
                for x,y in rock:
                    space[(x,y)] = i
                    height = max(height, y)
                break
            # render(space, height)
            # input()
    return height+1

if __name__ == "__main__":
    data = read_entire_input(2022,17)
    part_one(data)
    part_two(data)