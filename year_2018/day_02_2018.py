from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from collections import Counter

data = read_entire_input(2018,2)
test = """""".split("\n")

def parse(data: List[str]) -> Any:
    return data

@solution_timer(2018,2,1)
def part_one(data: List[str], verbose=False):
    ids = parse(data)
    threes = 0
    twos = 0
    for id in ids:
        counter = Counter(id)
        if 3 in counter.values():
            threes += 1
        if 2 in counter.values():
            twos += 1
    return threes*twos

def d(a,b):
    return sum((i!=j for i,j in zip(a,b)))

@solution_timer(2018,2,2)
def part_two(data: List[str], verbose=False):
    ids = parse(data)
    for i, id1 in enumerate(ids):
        for id2 in ids[i+1:]:
            c = 0
            for a,b in zip(id1,id2):
                if a!=b and c==1:
                    break
                elif a!=b and c==0:
                    c+=1
            else:
                return ''.join(i for i,j in zip(id1, id2) if i==j)
    return False

if __name__ == "__main__":
    data = read_entire_input(2018,2)
    part_one(data)
    part_two(data)