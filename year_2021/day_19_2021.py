from typing import List, Any, Tuple
from collections import namedtuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,19)

class Point:
    def __init__(self, A, B, C):
        self.A = A
        self.B = B
        self.C = C

    def pos(self, tform):
        p = self.A, self.B, self.C
        return 



def parse(data: List[str]) -> Any:
    return data

@solution_timer(2021,19,1)
def part_one(data: List[str]):
    _ = parse(data)

    return False

@solution_timer(2021,19,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,19)
    part_one(data)
    part_two(data)