from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,5)
test="""FBFBBFFRLR
BFFFBBFRRR
FFFBBBFRRR
BBFFBBFRLL"""

def parse(data):
    ids = []
    for seat in data:
        row = seat[:7].replace('F','0').replace('B','1')
        row = int(row,base=2)
        col = seat[-3:].replace('R','1').replace('L','0')
        col = int(col, base=2)
        ids.append(row*8+col)
    return ids

def find_missing_seat(ids):
    expected_id = ids[0]
    for seat in ids:
        if seat != expected_id:
            return expected_id
        expected_id+=1

@solution_timer(2020,5,1)
def part_one(data, verbose=False):
    ids = parse(data)
    return max(ids)

@solution_timer(2020,5,2)
def part_two(data, verbose=False):
    ids = parse(data)
    return find_missing_seat(sorted(ids))

if __name__ == "__main__":
    data = read_entire_input(2020,5)
    part_one(data)
    part_two(data)