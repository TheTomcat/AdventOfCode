from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window

def parse(data):
    output = []
    for row in data:
        direction, amount = row.split(' ')
        amount = int(amount)
        output.append((direction,amount))
    return output

HORIZONTAL = 0
DEPTH = 1
AIM = 2

@solution_timer(2021,2,1)
def part_one(data, verbose=False):
    data = parse(data)
    position = [0,0]
    for direction, amount in data:
        if direction == "forward":
            position[HORIZONTAL] += amount
        elif direction == "up":
            position[DEPTH] -= amount
        elif direction == "down":
            position[DEPTH] += amount
    return position[0] * position[1]

@solution_timer(2021,2,2)
def part_two(data, verbose=False):
    data = parse(data)
    position = [0, 0, 0]
    for direction,amount in data:
        if direction == "forward":
            position[HORIZONTAL] += amount
            position[DEPTH] += position[AIM]*amount
        elif direction == "up":
            position[AIM] -= amount
        elif direction == "down":
            position[AIM] += amount
    return position[0]*position[1]