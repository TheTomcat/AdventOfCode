from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,3)
test="""..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#"""
test1=7
test2=336

def parse(data):
    grid = []
    for line in data:
        grid.append(list(line))
    return grid

def toboggan(grid, vec):
    line_length = len(grid[0])
    x,y=(0,0)
    dx,dy = vec
    count = 0
    for y, row in enumerate(grid[::dy]):
        try:
            if row[x] == "#":
                count += 1 
            # print(row, x)
        except Exception as e:
            print(x, y)
            print(row)
            raise e
        x = (x + dx) % (line_length)
    return count

@solution_timer(2020,3,1)
def part_one(data):
    grid = parse(data)
    return toboggan(grid, (3,1))

@solution_timer(2020,3,2)
def part_two(data):
    vecs = [(1,1),(3,1),(5,1),(7,1),(1,2)]
    grid = parse(data)
    total = 1
    for vec in vecs:
        total *= toboggan(grid, vec)
    return total

if __name__ == "__main__":
    data = read_entire_input(2020,3)
    part_one(data)
    part_two(data)