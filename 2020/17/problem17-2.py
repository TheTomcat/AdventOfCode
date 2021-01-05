from collections import defaultdict

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def make_cube_space():
    inac = lambda : "I"
    cubes = defaultdict(inac)
    cubes['x'] = (0,0)
    cubes['y'] = (0,0)
    cubes['z'] = (0,0)
    cubes['w'] = (0,0)
    return cubes

def process(text):
    cubes = make_cube_space()
    rows = text.split('\n')
    for i, row in enumerate(rows):
        for j, cube in enumerate(row):
            if cube == "#":
                cubes = activate(cubes,i,j,0,0)
    return cubes

def activate(cubes, x, y, z, w):
    cubes[x,y,z,w] = "A"
    cubes = extend(cubes, x, y, z, w)
    return cubes
    
def deactivate(cubes, x, y, z, w):
    cubes[x,y,z] = "I"
    cubes = extend(cubes, x, y, z, w)
    return cubes

def extend(cubes, x, y, z, w):
    cubes['x'] = extend_one(cubes['x'],x)
    cubes['y'] = extend_one(cubes['y'],y)
    cubes['z'] = extend_one(cubes['z'],z)
    cubes['w'] = extend_one(cubes['w'],w)
    return cubes

def extend_one(bounds, new):
    return min(bounds[0],new),max(bounds[1],new)

def iterate_over(cubes):
    for x in range(cubes['x'][0]-1,cubes['x'][1]+2):
        for y in range(cubes['y'][0]-1,cubes['y'][1]+2):
                for z in range(cubes['z'][0]-1,cubes['z'][1]+2):
                    for w in range(cubes['w'][0]-1, cubes['w'][1]+2):
                        yield (x,y,z,w)

def neighbours(x,y,z,w):
    span = [-1,0,1]
    for i in span:
        for j in span:
            for k in span:
                for l in span:
                    if i==j==k==l==0:
                        continue
                    yield x+i,y+j,z+k,w+l

def size(cubes):
    xs = cubes['x'][1] - cubes['x'][0]+1
    ys = cubes['y'][1] - cubes['y'][0]+1
    zs = cubes['z'][1] - cubes['z'][0]+1
    ws = cubes['w'][1] - cubes['w'][0]+1
    return xs,ys,zs,ws

def step(cubes):
    new_cubes = make_cube_space()
    for position in iterate_over(cubes):
        num_active_neighbours = 0
        for neighbour in neighbours(*position):
            if cubes[neighbour] == "A":
                num_active_neighbours += 1
        if cubes[position] == "A":
            if num_active_neighbours in [2,3]:
                new_cubes = activate(new_cubes,*position)
            else:
                new_cubes = deactivate(new_cubes, *position)
        elif cubes[position] == "I":
            if num_active_neighbours == 3:
                new_cubes = activate(new_cubes, *position)
    return new_cubes

# def printme(cubes):
#     xs,ys,zs = size(cubes)
#     for z in range(cubes['z'][0],cubes['z'][1]+1):
#         print(f'z={z}')
#         row = '.'*xs
#         layer = [row]*ys
#         for x,y in iterate_over(cubes,z=z):

#         print()
#     rows = '.'*xs
#     layer = '\n'.join([rows]*ys)
#     space = 

def count(cubes):
    count = 0
    for position in iterate_over(cubes):
        if cubes[position] == "A":
            count += 1
    return count

test = """.#.
..#
###"""

cubes = process(test)
for i in range(6):
    cubes = step(cubes)
print(cubes)
print(count(cubes))
# cubes = step(cubes)
# print(cubes)
# print(count(cubes))
# cubes = step(cubes)
# print(cubes)
# print(count(cubes))

cubes = process(read_input(17))
for i in range(6):
    cubes = step(cubes)
print(count(cubes))