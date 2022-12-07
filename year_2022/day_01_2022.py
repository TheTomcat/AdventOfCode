from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2022,1)

def parse(data: List[str]) -> Any:
    data = '+'.join(data).split('++')
    return data

@solution_timer(2022,1,1)
def part_one(data: List[str]):
    calories = parse(data)
    totals = []
    for elf in calories:
        totals.append(eval(elf))
    return max(totals)

@solution_timer(2022,1,2)
def part_two(data: List[str]):
    calories = parse(data)
    totals = []
    for elf in calories:
        totals.append(eval(elf))
    return sum(sorted(totals, reverse=True)[:3])

if __name__ == "__main__":
    data = read_entire_input(2022,1)
    part_one(data)
    part_two(data)