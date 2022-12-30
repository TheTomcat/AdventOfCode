from collections import defaultdict
from enum import Enum
from typing import List, Any, Set, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.shared import render

data = read_entire_input(2022,23)
test = """..............
..............
.......#......
.....###.#....
...#...#.#....
....#...##....
...#.###......
...##.#.##....
....#..#......
..............
..............
..............""".split("\n")

test2 = """.....
..##.
..#..
.....
..##.
.....""".split("\n")

class Direction(Enum):
    N = (0,-1)
    NW = (-1,-1)
    W = (-1,0)
    SW = (-1,1)
    S = (0,1)
    SE = (1,1)
    E = (1,0)
    NE = (1,-1)
    def __getitem__(self, s):
        return self.value[s]

def parse(data: List[str]) -> Any:
    elves = set()
    for y, row in enumerate(data):
        for x,space in enumerate(row):
            if space == "#":
                elves.add((x,y))
    return elves, (len(data[0]), len(data))

rules = [
    (Direction.N, (7, 0, 1)),
    (Direction.S, (3, 4, 5)),
    (Direction.W, (5, 6, 7)),
    (Direction.E, (1, 2, 3)),
]

all_directions = (Direction.N, Direction.NE, Direction.E, Direction.SE, Direction.S, Direction.SW, Direction.W, Direction.NW)

def move_all(elves: Set, i=0):
    # step 1, calculate movements
    #elf_move = False
    planned_movements = defaultdict(list) # NEW: FROM
    # collisions = set()

    for elf in elves:
        adjacent = [(elf[0]+c[0], elf[1]+c[1]) in elves for c in all_directions]
        # print(f"Examining elf at {elf}", end="")
        if not any(adjacent):
            # print(f"No adjacent elves at all! Add me directly to the new elves")
            continue
        # print(f"Looking ", end="")        
        for planned_direction, checked_direction_indices in rules[i%4:]+rules[:i%4]:
                # Do nothing
            # print(f"{planned_direction} ", end=" ")
            if not any(j for i,j in enumerate(adjacent) if i in checked_direction_indices): # If any of the checked dirs is vacant
                
                planned_end_point = (elf[0]+planned_direction[0], elf[1]+planned_direction[1]) # Plan to move me in that direction
                planned_movements[planned_end_point].append(elf)
                # print(f"Moving to {planned_end_point}")
                break
            # print(f"No adjacent elves at all! Add me directly to the new elves") 

    for end_point, elves_to_move in planned_movements.items():
        if len(elves_to_move) == 1:
            elves.remove(elves_to_move[0])
            elves.add(end_point)
            #elf_move = True
        # else:
        #     for elf in elves_to_move:
        #         new_elves.add(elf)
    return len(planned_movements) == 0


def calculate_bbox(elves):
    xmin = min(i[0] for i in elves)
    xmax = max(i[0] for i in elves)
    ymin = min(i[1] for i in elves)
    ymax = max(i[1] for i in elves)
    return (xmin, xmax), (ymin, ymax)
        
@solution_timer(2022,23,1)
def part_one(data: List[str], verbose=False):
    elves, dim = parse(data)
    for i in range(10):
        # print(render(elves, render_function=("#",".")))
        # input("DONE")
        # elves = 
        move_all(elves, i)
    (xmin, xmax), (ymin, ymax) = calculate_bbox(elves)
    return (xmax-xmin+1) * (ymax-ymin+1) - len(elves)

@solution_timer(2022,23,2)
def part_two(data: List[str], verbose=False):
    elves, dim = parse(data)

    i=0
    while True:
        i+=1
        # print(render(elves, render_function=("#",".")))
        # input("DONE")
        # new_elves = 
        if move_all(elves, i):
        # if new_elves == elves:
            return i
        # elves = new_elves

if __name__ == "__main__":
    data = read_entire_input(2022,23)
    part_one(data)
    part_two(data)




# def move_all(elves, i=0):
#     # step 1, calculate movements
#     #elf_move = False
#     planned_movements = defaultdict(list) # NEW: FROM
#     # collisions = set()
#     new_elves = set()

#     for elf in elves:
#         adjacent = [(elf[0]+c[0], elf[1]+c[1]) in elves for c in all_directions]
#         # print(f"Examining elf at {elf}", end="")
#         if not any(adjacent):
#             new_elves.add(elf)
#             # print(f"No adjacent elves at all! Add me directly to the new elves")
#             continue
#         # print(f"Looking ", end="")        
#         for planned_direction, checked_direction_indices in rules[i%4:]+rules[:i%4]:
#                 # Do nothing
#             # print(f"{planned_direction} ", end=" ")
#             if not any(j for i,j in enumerate(adjacent) if i in checked_direction_indices): # If any of the checked dirs is vacant
                
#                 planned_end_point = (elf[0]+planned_direction[0], elf[1]+planned_direction[1]) # Plan to move me in that direction
#                 planned_movements[planned_end_point].append(elf)
#                 # print(f"Moving to {planned_end_point}")
#                 break
#         else:
#             new_elves.add(elf)   
#             # print(f"No adjacent elves at all! Add me directly to the new elves") 
            
#     for end_point, elves_to_move in planned_movements.items():
#         if len(elves_to_move) == 1:
#             new_elves.add(end_point)
#             #elf_move = True
#         else:
#             for elf in elves_to_move:
#                 new_elves.add(elf)
#     return new_elves