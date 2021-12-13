from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2019,16)

def parse(data: List[str]) -> Any:
    return data

@solution_timer(2019,16,1)
def part_one(data: List[str]):
    _ = parse(data)

    return False

@solution_timer(2019,16,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2019,16)
    part_one(data)
    part_two(data)