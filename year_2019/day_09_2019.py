from typing import List, Any, Tuple
from collections import defaultdict
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from framework.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,9)

@solution_timer(2019,9,1)
def part_one(data: List[str], verbose=False):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([1])

@solution_timer(2019,9,2)
def part_two(data: List[str], verbose=False):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([2])

if __name__ == "__main__":
    data = read_entire_input(2019,9)
    part_one(data)
    part_two(data)