from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window

data = read_entire_input(2021,1)
def parse(data):
    return [int(i) for i in data]

@solution_timer(2021,1,1)
def part_one(data, verbose=False):
    depths = parse(data)
    prev_depth=0
    inc_count=-1
    for new_depth in depths:
        if new_depth > prev_depth:
            inc_count += 1
        prev_depth = new_depth
    return inc_count

@solution_timer(2021,1,2)
def part_two(data, verbose=False):
    depths = parse(data)
    inc_count = 0
    for a,_,_,d in window(depths, 4):
        if int(a) < int(d):
            inc_count += 1
    return inc_count

if __name__ == "__main__":
    data = read_entire_input(2021,1)
    part_one(data)
    part_two(data)