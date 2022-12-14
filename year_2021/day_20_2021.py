from collections import defaultdict
from itertools import product
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window

data = read_entire_input(2021,20)
test = """..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

#..#.
#....
##..#
..#..
..###""".split('\n')
def parse(data: List[str]) -> Any:
    iea = list(0 if i=='.' else 1 for i in data[0])
    image = defaultdict(bool)
    for r, row in enumerate(data[2:]):
        for c, pixel in enumerate(row):
            if pixel == "#":
                image[(c,r)] = True
    return iea, image

def dim(image):
    x0 = min(i[0] for i in image.keys())
    x1 = max(i[0] for i in image.keys())
    y0 = min(i[1] for i in image.keys())
    y1 = max(i[1] for i in image.keys())
    return (x0,x1),(y0,y1)

def render(image):
    (x0,x1),(y0,y1) = dim(image)
    op = ""
    for y in range(y0,y1+1):
        for x in range(x0,x1+1):
            op = op + ('#' if image[(x,y)] else '.')
        op += '\n'
    return op

def run_iea(iea, image, dfv=False):
    im2 = defaultdict(lambda : dfv)
    (x0,x1),(y0,y1) = dim(image)
    for j in range(y0-1,y1+2):
        for i in range(x0-1,x1+2):
            index = int(''.join(['1' if image[(a+i,b+j)] else '0' for b,a in product([-1,0,1], repeat=2)]), base=2)
            # print(f'{index:10}',end="")
            im2[(i,j)] = True if iea[index] == 1 else False
        # print("")
    return im2

def count_on(image):
    return sum(True if val else False for val in image.values())

@solution_timer(2021,20,1)
def part_one(data: List[str], verbose=False):
    iea, image = parse(data)
    
    im2 = run_iea(iea, image, True)
    im2 = run_iea(iea, im2)
    return count_on(im2)#sum(True if val else False for val in im2.values())

@solution_timer(2021,20,2)
def part_two(data: List[str], verbose=False):
    iea, im2 = parse(data)
    for _ in range(25):
        im2 = run_iea(iea, im2, True)
        im2 = run_iea(iea, im2)
    return count_on(im2)

if __name__ == "__main__":
    data = read_entire_input(2021,20)
    part_one(data)
    part_two(data)