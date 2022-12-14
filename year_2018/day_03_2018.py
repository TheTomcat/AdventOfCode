from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

import re
from collections import Counter

data = read_entire_input(2018,3)
test = """#1 @ 1,3: 4x4
#2 @ 3,1: 4x4
#3 @ 5,5: 2x2""".split("\n")

def parse(data: List[str]) -> Any:
    regex = r'#(\d+)\s@\s(\d+),(\d+):\s(\d+)x(\d+)'
    expression = re.compile(regex)
    claims = {}
    for claim in data:
        iden, x, y, w, h = expression.match(claim).groups()
        claims[int(iden)] = (int(x), int(y), int(w), int(h))
    return claims

@solution_timer(2018,3,1)
def part_one(data: List[str], verbose=False):
    claims = parse(data)
    fabric = Counter()
    for iden, (x,y,w,h) in claims.items():
        for i in range(x,x+w):
            for j in range(y, y+h):
                fabric[(i,j)] += 1
    return len([x for x in fabric.values() if x >= 2])

@solution_timer(2018,3,2)
def part_two(data: List[str], verbose=False):
    claims = parse(data)
    fabric = dict()
    possibilities = dict()
    for iden, (x,y,w,h) in claims.items():
        possibilities[iden] = True
        for i in range(x,x+w):
            for j in range(y, y+h):
                if (i,j) in fabric:
                    possibilities[fabric[(i,j)]]=False
                    possibilities[iden]=False
                    fabric[(i,j)] = 'X'
                else:
                    fabric[(i,j)] = iden
    return [iden for iden in possibilities if possibilities[iden]][0]

if __name__ == "__main__":
    data = read_entire_input(2018,3)
    part_one(data)
    part_two(data)