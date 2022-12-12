from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

import re
from collections import deque

data = read_entire_input(2022,5)

positions = [1,5,9]

def parse(data: List[str]) -> Any:
    stacks = [deque() for i in range(9)]
    instructions = []
    regex = re.compile(r'move (\d+) from (\d+) to (\d+)')
    for line in data:
        if line.startswith('['):
            crates = line[1::4]
            for stack, crate in zip(stacks, crates):
                if crate != ' ':
                    stack.appendleft(crate)
        elif line.startswith('m'):
            instructions.append( [int(i) for i in regex.match(line).groups()])
    return [list(i) for i in stacks], instructions

def move9000(stacks, instruction):
    n, start, end = instruction
    for _ in range(n):
        if len(stacks[start-1]) == 0:
            return #stacks
        stacks[end-1].append(stacks[start-1].pop())
    #return stacks

def move9001(stacks, instruction):
    n, start, end = instruction
    if len(stacks[start-1]) == 0:
        return #stacks
    N = min(n, len(stacks[start-1]))
    temp = stacks[start-1][-N:]
    stacks[start-1][-N:] = []
    stacks[end-1].extend(temp)
    

@solution_timer(2022,5,1)
def part_one(data: List[str], verbose=False):
    stacks, instructions = parse(data)
    for instruction in instructions:
        move9000(stacks, instruction)
    return ''.join([i[-1] for i in stacks])

@solution_timer(2022,5,2)
def part_two(data: List[str], verbose=False):
    stacks, instructions = parse(data)
    for instruction in instructions:
        move9001(stacks, instruction)
    return ''.join([i[-1] for i in stacks])

if __name__ == "__main__":
    data = read_entire_input(2022,5)
    part_one(data)
    part_two(data)