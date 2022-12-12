from typing import Callable, List, Any, Set, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,13)
test = """6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5""".split("\n")
def parse(data: List[str]) -> Any:
    points = set()
    folds = []
    for row in data:
        if row == "":
            continue
        p = row.split(",")
        if len(p)==2:
            points.add((int(p[0]), int(p[1])))
        else:
            d, x = p[0].split('=')
            folds.append((d[-1], int(x)))
    return points, folds

def fold(points: Set, fold_line: Callable):
    new_points = set()
    for point in points:
        new_points.add(fold_line(point))
    return new_points

def x_fold(xval):
    def fold(point):
        if point[0] < xval:
            return point
        else:
            return 2*xval-point[0], point[1]
    return fold

def y_fold(yval):
    def fold(point):
        if point[1] < yval:
            return point
        else:
            return point[0], 2*yval-point[1]
    return fold

def render(points):
    xmin = min(i[0] for i in points)
    xmax = max(i[0] for i in points)
    ymin = min(i[1] for i in points)
    ymax = max(i[1] for i in points)
    image = '\n'.join(''.join(chr(9608) if (i,j) in points else ' ' for i in range(xmin, xmax+1)) for j in range(ymin, ymax+1))
    return image

@solution_timer(2021,13,1)
def part_one(data: List[str], verbose=False):
    points, folds = parse(data)
    v, a = folds[0]
    if v == 'x':
        f = x_fold(a)
    else:
        f = y_fold(a)
    points = fold(points, f)
    return len(points)

@solution_timer(2021,13,2)
def part_two(data: List[str], verbose=False):
    points, folds = parse(data)
    for instruction in folds:
        v, a = instruction
        if v == 'x':
            f = x_fold(a)
        else:
            f = y_fold(a)
        points = fold(points, f)
    return '\n'+render(points)

if __name__ == "__main__":
    data = read_entire_input(2021,13)
    part_one(data)
    part_two(data)