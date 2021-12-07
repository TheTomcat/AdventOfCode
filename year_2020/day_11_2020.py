from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,11)

def parse(data):
    seats=[]
    for row in data:
        row.replace("L","#")
        seats.append(row)
    return seats

EMPTY = "L"
FLOOR = "."
OCCUP = "#"

ngb = [(1,1),(1,0),(1,-1),
       (0,1),(0,-1),
       (-1,1),(-1,0),(-1,-1)]

def within(x,y,xmax,ymax):
    return 0<=x<xmax and 0<=y<ymax

def neighbours(xp, yp, xmax, ymax):
    for x,y in ngb:
        if within(x+xp, y+yp, xmax, ymax):
            yield x, y

def iterate(data):
    newdata = [[i for i in row] for row in data]
    changed = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            count=0
            if data[y][x] == EMPTY:
                for dx, dy in neighbours(x,y,len(data[y]),len(data)):
                    if data[y+dy][x+dx] == OCCUP:
                        count += 1
                if count == 0:
                    newdata[y][x] = OCCUP
                    changed += 1
            elif data[y][x] == OCCUP:
                for dx, dy in neighbours(x,y,len(data[y]),len(data)):
                    if data[y+dy][x+dx] == OCCUP:
                        count += 1
                if count >= 4:
                    newdata[y][x] = EMPTY
                    changed += 1
    return newdata, changed

def run(data, iterator):
    i=0
    while True:
        newdata,changed = iterator(data)
        if data == newdata:
            return newdata
        data = newdata
        # print(i,changed)
        i=i+1

def count_filled(data):
    count=0
    for row in data:
        for col in row:
            if col == OCCUP:
                count += 1

    return count

@solution_timer(2020,11,1)
def part_one(data):
    seats = parse(data)
    full = run(seats, iterate)
    return count_filled(full)

def iterate2(data):
    newdata = [[i for i in row] for row in data]
    changed = 0
    for y in range(len(data)):
        for x in range(len(data[y])):
            count=0
            if data[y][x] == EMPTY:
                for dx, dy in neighbours(x,y,len(data[y]),len(data)):
                    scl = 1
                    while within(x+scl*dx, y+scl*dy, len(data[y]), len(data)):
                        nx = x + scl * dx
                        ny = y + scl * dy
                        #print(nx,ny)
                        if data[ny][nx] == FLOOR:
                            scl+=1
                            continue
                        elif data[ny][nx] == OCCUP:
                            count += 1
                            break  
                        else: 
                            break
                        scl+=1
                if count == 0:
                    newdata[y][x] = OCCUP
                    changed += 1
            elif data[y][x] == OCCUP:
                for dx, dy in neighbours(x,y,len(data[y]),len(data)):
                    scl = 1
                    while within(x+scl*dx, y+scl*dy, len(data[y]), len(data)):
                        nx = x + scl * dx
                        ny = y + scl * dy
                        if data[ny][nx] == FLOOR:
                            scl+=1
                            continue
                        elif data[ny][nx] == OCCUP:
                            count += 1
                            break  
                        else: 
                            break
                        scl+=1
                if count >= 5:
                    newdata[y][x] = EMPTY
                    changed += 1
    return newdata, changed

@solution_timer(2020,11,2)
def part_two(data):
    seats = parse(data)
    full = run(seats, iterate2)
    return count_filled(full)

if __name__ == "__main__":
    data = read_entire_input(2020,11)
    part_one(data)
    part_two(data)