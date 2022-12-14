from typing import List, Any, Tuple
from collections import deque
from itertools import product
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from framework.console import console

data = read_entire_input(2021,11)
test = """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""".split("\n")

def parse(data: List[str]) -> Any:
    return {(x,y):int(energy) for y, row in enumerate(data) for x,energy in enumerate(row)}, len(data[0]), len(data)

def neighbours(x,y,w,h):
    for dx,dy in product([-1,0,1], repeat=2):
        if 0 <= x+dx < w and 0 <= y+dy < h and not (dx == 0 and dy == 0):
            yield x+dx, y+dy

def pprint(octopuses, w, h):
    for i in range(w):
        for j in range(h):
            v = octopuses[(j,i)]
            console.print(f"[red]9" if v == 9 else (f'[green]{v}' if v > 0 else '[white]0'),end="")
        print("")

def flash(octopuses, octopus, W, H):
    for neighbour in neighbours(*octopus, W, H):
        octopuses[neighbour] += 1
    return octopuses

def step(octopuses,W,H):
    increment = {}
    for octopus, energy in octopuses.items():
        octopuses[octopus] += 1
    # Find the ones that have 10 and then set to zero, store these in refractory and don't let them flash or increment again this round

    to_flash = [octopus for octopus, energy in octopuses.items() if energy > 9]
    flashing = True
    already_evaluated = []
    while flashing:
        flashing = False
        for octopus in to_flash:
            if octopus in already_evaluated:
                continue
            octopuses = flash(octopuses, octopus, W,H)
            already_evaluated.append(octopus)
            flashing = True
        to_flash = [octopus for octopus, energy in octopuses.items() if energy > 9 and octopus not in already_evaluated]
    octopuses = {octopus:energy if energy <= 9 else 0 for octopus, energy in octopuses.items()}
    return octopuses    

@solution_timer(2021,11,1)
def part_one(data: List[str], verbose=False):
    octopuses, W, H = parse(data)
    flashes = 0
    for _ in range(100):
        octopuses = step(octopuses, W, H)
        flashes += sum(1 for energy in octopuses.values() if energy == 0)
    return flashes

@solution_timer(2021,11,2)
def part_two(data: List[str], verbose=False):
    octopuses, W, H = parse(data)
    i = 0
    while True:
        octopuses = step(octopuses, W, H)
        i += 1
        flashes = sum(1 for energy in octopuses.values() if energy == 0)
        if flashes == W*H:
            return i
        

if __name__ == "__main__":
    data = read_entire_input(2021,11)
    part_one(data)
    part_two(data)