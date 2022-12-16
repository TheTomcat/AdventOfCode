from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from lib.shared import overlap

data = read_entire_input(2022,4)
test = """2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8""".split("\n")

def parse(data: List[str]) -> Any:
    ranges = []
    for line in data:
        a,b = line.split(",")
        ranges.append([[int(i) for i in a.split("-")], [int(i) for i in b.split("-")]])
    return ranges

def intersection_length(range1, range2):
    if range2[0] > range1[1] or range1[0] > range2[1]:
        return 0
    start = max(range1[0], range2[0])
    end = min(range1[1], range2[1])
    return end-start + 1

def range_length(range1):
    return range1[1] - range1[0] + 1

@solution_timer(2022,4,1)
def part_one(data: List[str], verbose=False):
    ranges = parse(data)
    count=0
    for r1, r2 in ranges:
        i = intersection_length(r1,r2)
        if i == range_length(r1) or i == range_length(r2):
            count += 1
    return count

@solution_timer(2022,4,2)
def part_two(data: List[str], verbose=False):
    ranges = parse(data)
    count=0
    for r1, r2 in ranges:
        i = intersection_length(r1,r2)
        if i >= 1:
            count += 1
    return count

if __name__ == "__main__":
    data = read_entire_input(2022,4)
    part_one(data)
    part_two(data)