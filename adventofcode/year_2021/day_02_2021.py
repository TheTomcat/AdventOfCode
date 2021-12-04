

HORIZONTAL = 0
DEPTH = 1
AIM = 2

with open("2021/2/input.txt","r") as f:
    position = [0,0]
    for line in f:
        direction, amount = line.split(' ')
        amount = int(amount)
        if direction == "forward":
            position[HORIZONTAL] += amount
        elif direction == "up":
            position[DEPTH] -= amount
        elif direction == "down":
            position[DEPTH] += amount

print(position[0]*position[1])

with open("2021/2/input.txt","r") as f:
    position = [0, 0, 0]
    for line in f:
        direction, amount = line.split(' ')
        amount = int(amount)
        if direction == "forward":
            position[HORIZONTAL] += amount
            position[DEPTH] += position[AIM]*amount
        elif direction == "up":
            position[AIM] -= amount
        elif direction == "down":
            position[AIM] += amount

print(position[0]*position[1])