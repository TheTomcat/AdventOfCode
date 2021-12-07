def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

# ship = (xp, yp, dir)

def process(text):
    dirs = text.split('\n')
    commands = [(i[0], int(i[1:])) for i in dirs]
    return commands

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

test = """F10
N3
F7
R90
F11"""

ship = (0,0,90)

def iterate(ship, commands):
    for command in commands:
        ship = move(ship, *command)
    return ship

# print(iterate(ship, process(test)))
commands = process(read_input(12))
output = iterate(ship, commands)
print(abs(output[0])+abs(output[1]))

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
    # print(f"Ship: {ship[0]},{ship[1]}")
    # print(f"Wayp: {waypoint[0]},{waypoint[1]}")
    for command in commands:
        # print(f"Command {command}")
        ship, waypoint = move2(ship, waypoint, *command)
        # print(ship, waypoint)
    return ship

# commands = process(test)

ship = (0,0,0)
waypoint = (10,1,0)
output = iterate2(ship, waypoint, commands)
print(abs(output[0])+abs(output[1]))