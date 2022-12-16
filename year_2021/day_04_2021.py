from framework.input_helper import read_entire_input, read_input_by_line
from framework.helpers import solution_timer
from lib.iterators import window, transpose

data = read_entire_input(2021,4)

def parse(data):
    def _split(row):
        return [int(row[i:i+2]) for i in range(0,15,3)] 

    nums = [int(i) for i in data[0].split(",")]
    squares = []
    for i in range(2,len(data),6):
        # try:
        square = [_split(i) for i in data[i:i+5]]
        squares.append(square)
    return nums, squares

def iterate_over_rows(square):
    for row in square:
        yield row
    for col in transpose(square):
        yield col

def call(number, square):
    for y, row in enumerate(square):
        for x,c in enumerate(row):
            if c == number:
                square[y][x] = "X"

def check(square):
    for row in iterate_over_rows(square):
        if all([i == "X" for i in row]):
            return True
    return False

def sum_square(square):
    tot = 0
    for row in square:
        for c in row:
            if c != "X":
                tot += c
    return tot

@solution_timer(2021,4,1)
def part_one(data, verbose=False):
    nums, squares = parse(data)
    for num in nums:
        for i, square in enumerate(squares):
            call(num,square)
            if check(square):
                return sum_square(square)* num

@solution_timer(2021,4,2)
def part_two(data, verbose=False):
    nums, squares = parse(data)
    remove = []
    for num in nums:
        for i, square in enumerate(squares):
            if i in remove:
                continue
            call(num,square)
            if check(square):
                remove.append(i)
                if len(remove) == len(squares):
                    return sum_square(square)* num

