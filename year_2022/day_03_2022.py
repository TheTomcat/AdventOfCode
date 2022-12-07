from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2022,3)
test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split('\n')

priority = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parse(data: List[str]) -> Any:
    rucksacks = []
    for line in data:
        n=len(line)
        rucksacks.append([line[:n],line[n:]])
    return rucksacks

@solution_timer(2022,3,1)
def part_one(data: List[str]):
    rucksacks = parse(data)
    for A, B in rucksacks:
        items = set(A) & set(B)
        

    return False

@solution_timer(2022,3,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2022,3)
    part_one(data)
    part_two(data)