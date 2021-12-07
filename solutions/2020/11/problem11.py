def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    data = text.split('\n')
    data = [list(i) for i in data]
    return data

text = read_input(11)
text = text.replace('L','#')
data = process(text)

ngb = [(1,1),(1,0),(1,-1),
       (0,1),(0,-1),
       (-1,1),(-1,0),(-1,-1)]

def neighbours(xp, yp, xmax, ymax):
    for x,y in ngb:
        if within(x+xp, y+yp, xmax, ymax):
            yield x, y

def within(x,y,xmax,ymax):
    return 0<=x<xmax and 0<=y<ymax

EMPTY = "L"
FLOOR = "."
OCCUP = "#"

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

def run(data):
    i=0
    while True:
        newdata,changed = iterate2(data)
        if data == newdata:
            return newdata
        data = newdata
        print(i,changed)
        i=i+1

def count_filled(data):
    count=0
    for row in data:
        for col in row:
            if col == OCCUP:
                count += 1

    return count

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

# test="""L.LL.LL.LL
# LLLLLLL.LL
# L.L.L..L..
# LLLL.LL.LL
# L.LL.LL.LL
# L.LLLLL.LL
# ..L.L.....
# LLLLLLLLLL
# L.LLLLLL.L
# L.LLLLL.LL"""
# data = process(test)
full = run(data)
print(count_filled(full))