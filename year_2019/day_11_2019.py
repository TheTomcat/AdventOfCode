from collections import defaultdict
from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,11)

def run_robot(data:List[str], init=0):
    debug = False
    robot = IntCode(data, debug=debug)
    is_white = defaultdict(lambda: 0)
    is_white[(0,0)] = init
    position = (0,0)
    direction = (0,1)

    while not robot.halted:
        colour = robot.run([is_white[position]])
        turn = robot.run([])
        if debug:
            console.print(f"ROBO pos{position}-dir{direction} -> current colour: {is_white[position]} -> {colour}. Turning {turn}")
        is_white[position] = colour
        if turn == 0: # Turn left
            direction = -direction[1], direction[0]
        elif turn == 1:
            direction = direction[1], -direction[0]
        position = position[0] + direction[0], position[1] + direction[1]
        if debug:
            console.print(f"MOVE pos{position}-dir{direction} -> current colour: {is_white[position]}")
    return is_white

@solution_timer(2019,11,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    is_white = run_robot(instructions)
    return len(is_white)

@solution_timer(2019,11,2)
def part_two(data: List[str], verbose=False):
    instructions = parse(data)
    is_white = run_robot(instructions, 1)
    xmin = min(i[0] for i in is_white.keys())
    xmax = max(i[0] for i in is_white.keys())
    ymin = min(i[1] for i in is_white.keys())
    ymax = max(i[1] for i in is_white.keys())
    image = '\n'.join(''.join(chr(9608) if is_white[(i,j)] else ' ' for i in range(xmin, xmax+1)) for j in range(ymax, ymin-1, -1))
    return '\n'+image

if __name__ == "__main__":
    data = read_entire_input(2019,11)
    part_one(data)
    part_two(data)