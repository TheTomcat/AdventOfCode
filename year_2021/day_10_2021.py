from typing import List, Any, Tuple
from collections import deque
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from year_2021.day_08_2021 import read_output


data = read_entire_input(2021,10)

def parse(data: List[str]) -> Any:
    return [list(i) for i in data]

class IncompleteLineError(Exception):
    pass
class CorruptedLineError(Exception):
    pass

def read_instructions(chunk: List[str]):
    """Return code and then extra data.
     -> Corrupted line: 1, corrupted character
     -> Incomplete line: 2, expected characters
     -> Valid line: 0, None"""
    pairs = {"<":">", "[":"]", "{":"}", "(":")"}
    instructions = deque()
    for instruction in chunk:
        if instruction in pairs:
            instructions.append(instruction)
        else:
            expected = pairs[instructions.pop()]
            if instruction != expected:
                return 1, instruction
                #raise CorruptedLineError(f"Expected {expected} but found {instruction} instead")
    if len(instructions) > 0:
        return 2, [pairs[i] for i in instructions]
    return 0




@solution_timer(2021,10,1)
def part_one(data: List[str], verbose=False):
    chunks = parse(data)
    total = 0
    points = {")":3, "]":57, "}":1197,">":25137}
    for chunk in chunks:
        return_code, char = read_instructions(chunk)
        if return_code == 1:
            total += points[char]
    return total

@solution_timer(2021,10,2)
def part_two(data: List[str], verbose=False):
    chunks = parse(data)
    points = {")":1, "]":2, "}":3,">":4}
    scores = []
    for chunk in chunks:
        return_code, chars = read_instructions(chunk)
        if return_code == 2:
            i_score = 0
            while len(chars) > 0:
                i_score *= 5
                i_score += points[chars.pop()]
            scores.append(i_score)
    scores = sorted(scores)
    return scores[len(scores)//2]

if __name__ == "__main__":
    data = read_entire_input(2021,10)
    part_one(data)
    part_two(data)