from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from util.shared import sgn, window

data = read_entire_input(2022,9)
test = """R 4
U 4
L 3
D 1
R 4
D 1
L 5
R 2""".split("\n")

test2 = """R 5
U 8
L 8
D 3
R 17
D 10
L 25
U 20""".split('\n')

def parse(data: List[str]) -> Any:
    instructions = []
    for instruction in data:
        direction, num = instruction.split(" ")
        num = int(num)
        instructions.append([direction, num])
    return instructions

@solution_timer(2022,9,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    tail_positions = set()
    head_pos = (0,0)
    tail_pos = (0,0)
    tail_positions.add(tail_pos)
    move_dict = {'U':(0,1), 'D':(0,-1), 'L': (-1,0), 'R':(1,0)}
    for direction, n in instructions:
        # move head
        for i in range(n):
            head_pos = tuple(i+j for i,j in zip(head_pos, move_dict[direction]))
            if (abs(head_pos[0] - tail_pos[0]) > 1 or abs(head_pos[1] - tail_pos[1]) > 1):
                x_dir = sgn(head_pos[0] - tail_pos[0])
                y_dir = sgn(head_pos[1] - tail_pos[1])
                tail_pos = tuple(i+j for i,j in zip(tail_pos, (x_dir, y_dir)))
                tail_positions.add(tail_pos)
            # print(head_pos, tail_pos)
    return len(tail_positions)

def render(rope, X, Y):
    for row in range(Y[1],Y[0],-1):
        for col in range(X[0], X[1]):
            if (col, row) in rope:
                print(rope.index((col,row)), end="")
            else:
                print('.', end="")
        if row == 0:
            print(f"  {rope}", end='')
        print()

@solution_timer(2022,9,2)
def part_two(data: List[str], verbose=False):
    instructions = parse(data)
    tail_positions = set()
    rope = [(0,0) for i in range(10)]
    tail_positions.add(rope[-1])
    move_dict = {'U':(0,1), 'D':(0,-1), 'L': (-1,0), 'R':(1,0)}
    for direction, n in instructions:
        # move head
        for i in range(n):
            rope[0] = tuple(i+j for i,j in zip(rope[0], move_dict[direction]))
            for p in range(len(rope)-1):
                a,b = rope[p], rope[p+1]
                # input(f'{p} -> {a}, {b}')
                if (abs(a[0] - b[0]) > 1 or abs(a[1] - b[1]) > 1):
                    x_dir = sgn(a[0] - b[0])
                    y_dir = sgn(a[1] - b[1])
                    rope[p+1] = tuple(i+j for i,j in zip(b, (x_dir, y_dir)))
                #input(f'{p} -> {a}, {b} ==> {rope[p]}, {rope[p+1]} {x_dir} {y_dir}')
            tail_positions.add(rope[-1])
            # print("X")
            #render(rope, (-11,11), (-6,16))
            #input()
            # print(head_pos, tail_pos)
    return len(tail_positions)

if __name__ == "__main__":
    data = read_entire_input(2022,9)
    part_one(data)
    part_two(data)