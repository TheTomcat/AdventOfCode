from collections import defaultdict

from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2020,17)

def make_cube_space(four_d=False):
    inac = lambda : "I"
    cubes = defaultdict(inac)
    cubes['x'] = (0,0)
    cubes['y'] = (0,0)
    cubes['z'] = (0,0)
    if four_d:
        cubes['w'] = (0,0)
    return cubes

def parse(data, four_d=False):
    cubes = make_cube_space(four_d)
    for i, row in enumerate(data):
        for j, cube in enumerate(row):
            if cube == "#":
                if is_four_d(cubes):
                    cubes = activate(cubes,i,j,0,0)    
                else:
                    cubes = activate(cubes,i,j,0)
    return cubes

def is_four_d(cubes):
    return 'w' in cubes

def activate(cubes, x, y, z, w=None):
    if w is not None:
        cubes[x,y,z,w] = "A"
    else:
        cubes[x,y,z] = "A"
    cubes = extend(cubes, x, y, z, w)
    return cubes

def deactivate(cubes, x, y, z, w=None):
    if w is not None:
        cubes[x,y,z,w] = "I"
    else:
        cubes[x,y,z] = "I"
    cubes = extend(cubes, x, y, z, w)
    return cubes

def extend(cubes, x, y, z, w=None):
    cubes['x'] = extend_one(cubes['x'],x)
    cubes['y'] = extend_one(cubes['y'],y)
    cubes['z'] = extend_one(cubes['z'],z)
    if w is not None:
        cubes['w'] = extend_one(cubes['w'],w)
    return cubes

def extend_one(bounds, new):
    return min(bounds[0],new),max(bounds[1],new)

def iterate_over(cubes, z=None):
    for x in range(cubes['x'][0]-1,cubes['x'][1]+2):
        for y in range(cubes['y'][0]-1,cubes['y'][1]+2):
            for z in range(cubes['z'][0]-1,cubes['z'][1]+2):
                if is_four_d(cubes):
                    for w in range(cubes['w'][0]-1, cubes['w'][1]+2):
                        yield (x,y,z,w)
                else:
                    yield (x,y,z)

def neighbours(x,y,z,w=None):
    span = [-1,0,1]
    for i in span:
        for j in span:
            for k in span:
                if w is None:    
                    if i==j==k==0:
                        continue
                    yield x+i,y+j,z+k
                else:
                    for l in span:
                        if i==j==k==l==0:
                            continue
                        yield x+i,y+j,z+k,w+l

# def size(cubes):
#     xs = cubes['x'][1] - cubes['x'][0]+1
#     ys = cubes['y'][1] - cubes['y'][0]+1
#     zs = cubes['z'][1] - cubes['z'][0]+1
#     if is_four_d(cubes):
#         ws = cubes['w'][1] - cubes['w'][0]+1
#         return xs,ys,zs,ws
#     return xs,ys,zs

def step(cubes):
    new_cubes = make_cube_space(is_four_d(cubes))
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

def count(cubes):
    count = 0
    for position in iterate_over(cubes):
        if cubes[position] == "A":
            count += 1
    return count

@solution_timer(2020,17,1)
def part_one(data, verbose=False):
    cubes = parse(data)
    for i in range(6):
        cubes = step(cubes)
    return count(cubes)

@solution_timer(2020,17,2)
def part_two(data, verbose=False):
    cubes = parse(data, True)
    for i in range(6):
        cubes = step(cubes)
    return count(cubes)

if __name__ == "__main__":
    data = read_entire_input(2020,17)
    part_one(data)
    part_two(data)