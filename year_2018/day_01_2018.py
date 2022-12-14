from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2018,1)
test = """""".split("\n")

def parse(data: List[str]) -> Any:
    shifts = []
    for row in data:
        shifts.append(int(row))
    return shifts

@solution_timer(2018,1,1)
def part_one(data: List[str], verbose=False):
    shifts = parse(data)
    return sum(shifts)

@solution_timer(2018,1,2)
def part_two(data: List[str], verbose=False):
    shifts = parse(data)
    reached = set()
    frequency = 0
    reached.add(frequency)
    while True:
        for shift in shifts:
            frequency += shift
            if frequency in reached:
                return frequency
            reached.add(frequency)

if __name__ == "__main__":
    data = read_entire_input(2018,1)
    part_one(data)
    part_two(data)