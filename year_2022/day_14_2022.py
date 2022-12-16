from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from framework.console import console

from lib.iterators import window, sgn

data = read_entire_input(2022,14)
test = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9""".split("\n")

def parse(data: List[str]) -> Any:
    wall_vertices = []
    for wall in data:
        seq = wall.split(" -> ")
        wall_vertices.append([[int(i) for i in x.split(',')] for x in seq])
    return wall_vertices

def one_direction(start, finish):
    x0, y0 = start
    x1, y1 = finish
    if x0==x1:
        for y in range(y0,y1,sgn(y1-y0)):
            yield x0, y
    elif y0==y1:
        for x in range(x0,x1,sgn(x1-x0)):
            yield x, y0
    else:
        raise IndexError

def build_walls(wall_vertices):
    walls = []
    for wall in wall_vertices:
        walls.append([(x,y) for start, finish in window(wall) for x,y in one_direction(start, finish)])
        walls[-1].append(tuple(wall[-1]))
    return walls

def find_extrema(wall_vertices):
    xmin, ymin, xmax, ymax = 500, 0, 500, 0
    for walls in wall_vertices:
        for x,y in walls:            
            xmin = min(xmin, x)
            ymin = min(ymin, y)
            xmax = max(xmax, x)
            ymax = max(ymax, y)
    return (xmin, xmax), (ymin, ymax)

class Rockface:
    def __init__(self, wall_vertices, origin):
        walls = build_walls(wall_vertices)
        self.X, self.Y = find_extrema(wall_vertices)
        self.space = {(x,y):'#' for wall in walls for x,y in wall}
        self.origin = origin
        self.space[origin] = '+'
        self.mrd = (500,0)
    def drop(self):
        x,y = self.origin
        while self.X[0] <= x <= self.X[1] and self.Y[0] <= y <= self.Y[1]:
            #print(f'({x},{y}) -> [{self.X} , {self.Y}]')
            for dx,dy in [(0,1),(-1,1), (1,1)]:
                if (x+dx, y+dy) not in self.space: # If this square is empty
                    x += dx
                    y += dy
                    break
            else:
                self.space[(x,y)] = "o"
                self.mrd = (x,y)
                return x,y
                # settle
        else:
            return False
    def drop_all(self):
        c = 0
        while d := self.drop():
            c += 1
            if d == self.origin:
                return c
        return c
    def add_floor(self, depth=2):
        y = self.Y[1]+depth
        floorX0 = 500 - y - 2
        floorX1 = 500 + y + 2
        for x in range(floorX0, floorX1):
            self.space[(x,y)] = "#"
        self.X = (floorX0, floorX1)
        self.Y = (0, y)

    def render(self):
        for y in range(self.Y[0], self.Y[1]+1):
            for x in range(self.X[0], self.X[1]+1):
                if (x,y) in self.space:
                    v = self.space[(x,y)]
                    c = 'grey'
                    if (x,y) == self.mrd:
                        c = 'blue'
                    elif v == 'o':
                        c='yellow'  
                    elif v=='+':
                        c = 'green'
                    else:
                        c = 'red'
                    console.print(f'[{c}]{v}[/{c}]', end='')
                else:
                    console.print('.', end='')
            print()


@solution_timer(2022,14,1)
def part_one(data: List[str], verbose=False):
    wall_vertices = parse(data)
    origin = (500,0)
    R = Rockface(wall_vertices, origin)
    
    sand = R.drop_all()
    if verbose:
        R.render()
    return sand

@solution_timer(2022,14,2)
def part_two(data: List[str], verbose=False):
    wall_vertices = parse(data)
    origin = (500,0)
    R = Rockface(wall_vertices, origin)
    R.add_floor()
    sand = R.drop_all()
    if verbose:
        R.render()
    return sand

if __name__ == "__main__":
    data = read_entire_input(2022,14)
    part_one(data)
    part_two(data)