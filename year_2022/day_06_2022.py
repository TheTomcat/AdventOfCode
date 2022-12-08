from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

from util.shared import window

data = read_entire_input(2022,6)

def parse(data: List[str]) -> Any:
    return data

@solution_timer(2022,6,1)
def part_one(data: List[str]):
    datastream = parse(data)[0]
    for i, code in enumerate(window(datastream, n=4)):
        if len(set(code))==4:
            return i+4

@solution_timer(2022,6,2)
def part_two(data: List[str]):
    datastream = parse(data)[0]
    for i, code in enumerate(window(datastream, n=14)):
        if len(set(code))==14:
            return i+14

if __name__ == "__main__":
    data = read_entire_input(2022,6)
    part_one(data)
    part_two(data)