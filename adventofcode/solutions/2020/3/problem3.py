def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        for line in f:
            yield line
        
start = (0,0)
vec = (3,1) # Right 3, Down 1

def split_string_to_grid(rows):
    grid = []
    data = rows.split('\n')
    for line in data:
        grid.append(list(line))
    return grid

def toboggan(data, vec):
    grid = split_string_to_grid(data)
    line_length = len(grid[0])
    x,y=start
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

    print(count)


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

toboggan(test, (1,1))
toboggan(test, (3,1))
toboggan(test, (5,1))
toboggan(test, (7,1))
toboggan(test, (1,2))
data = read_input(3)
f = open('2020/3/input.txt','r')
data = f.read()
f.close()
print(data[:20])
toboggan(data, (1,1))
toboggan(data, (3,1))
toboggan(data, (5,1))
toboggan(data, (7,1))
toboggan(data, (1,2))