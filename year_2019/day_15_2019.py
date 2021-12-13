from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,15)

@solution_timer(2019,15,1)
def part_one(data: List[str]):
    _ = parse(data)

    return False

@solution_timer(2019,15,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2019,15)
    part_one(data)
    part_two(data)