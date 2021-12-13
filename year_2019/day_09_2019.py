from typing import List, Any, Tuple
from collections import defaultdict
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,9)

@solution_timer(2019,9,1)
def part_one(data: List[str]):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([1])

@solution_timer(2019,9,2)
def part_two(data: List[str]):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([2])

if __name__ == "__main__":
    data = read_entire_input(2019,9)
    part_one(data)
    part_two(data)