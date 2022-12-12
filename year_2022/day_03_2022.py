from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

from util.shared import grouper

data = read_entire_input(2022,3)
test = """vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw""".split('\n')

priority = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'

def parse(data: List[str]) -> Any:
    return data

@solution_timer(2022,3,1)
def part_one(data: List[str], verbose=False):
    rucksacks = parse(data)
    priorities = 0
    for compartments in rucksacks:
        n = len(compartments)//2
        A = compartments[:n]
        B = compartments[n:]
        items = set(A) & set(B)
        for item in items:
            priorities += priority.index(item) + 1
    return priorities

@solution_timer(2022,3,2)
def part_two(data: List[str], verbose=False):
    rucksacks = parse(data)
    priorities = 0
    for a,b,c in grouper(3, rucksacks):
        key = set(a) & set(b) & set(c)
        for el in key:
            priorities += priority.index(el) + 1
    return priorities

if __name__ == "__main__":
    data = read_entire_input(2022,3)
    part_one(data)
    part_two(data)