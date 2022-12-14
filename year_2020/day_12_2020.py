from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,12)

def parse(data):
    return [(i[0], int(i[1:])) for i in data]

test = """F10
N3
F7
R90
F11"""
test1=25
test2=286

def move(ship, action, argument):
    xp, yp, direction = ship
    if action == "N":
        ship = (xp, yp+argument, direction)
    elif action == "S":
        ship = (xp, yp-argument, direction)
    elif action == "E":
        ship = (xp+argument, yp, direction)
    elif action == "W":
        ship = (xp-argument, yp, direction)
    elif action == "L":
        ship = (xp, yp, (direction - argument) % 360)
    elif action == "R":
        ship = (xp, yp, (direction + argument) % 360)
    elif action == "F":
        if direction == 0:
            ship = (xp, yp+argument, direction) 
        if direction == 90:
            ship = (xp+argument, yp, direction)
        if direction == 180:
            ship = (xp, yp-argument, direction)
        if direction == 270:
            ship = (xp-argument, yp, direction)
    return ship

def iterate(ship, commands):
    for command in commands:
        ship = move(ship, *command)
    return ship

@solution_timer(2020,12,1)
def part_one(data, verbose=False):
    commands = parse(data)
    ship = (0,0,90)
    output = iterate(ship, commands)
    return abs(output[0])+abs(output[1])


def move2(ship, waypoint, action, argument):
    xs, ys, ds = ship
    xw, yw, dw = waypoint
    if action == "N":
        waypoint = (xw, yw+argument, dw)
    elif action == "S":
        waypoint = (xw, yw-argument, dw)
    elif action == "E":
        waypoint = (xw+argument, yw, dw)
    elif action == "W":
        waypoint = (xw-argument, yw, dw)
    elif action == "L" or action == "R":
        if action == "L":
            argument = (360 - argument) % 360
        if argument == 0:
            pass
        elif argument == 90:
            waypoint = (yw, -xw, dw)
        elif argument == 180:
            waypoint = (-xw, -yw, dw)
        elif argument == 270:
            waypoint = (-yw, xw, dw)
    elif action == "F":
        ship = (xs+argument*xw, ys+argument*yw, ds)
    return ship, waypoint

def iterate2(ship, waypoint, commands):
    for command in commands:
        ship, waypoint = move2(ship, waypoint, *command)
    return ship

@solution_timer(2020,12,2)
def part_two(data, verbose=False):
    commands = parse(data)
    ship = (0,0,0)
    waypoint = (10,1,0)
    output = iterate2(ship, waypoint, commands)
    return abs(output[0])+abs(output[1])

if __name__ == "__main__":
    data = read_entire_input(2020,12)
    part_one(data)
    part_two(data)