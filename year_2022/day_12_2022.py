from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

from util.shared import render
from util.graph import search, construct_path
from util.console import console

data = read_entire_input(2022,12)
test = """Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi""".split("\n")

def parse(data: List[str]) -> Any:
    heightmap = {}
    for y, row in enumerate(data):
        for x, el in enumerate(row):
            heightmap[(x,y)] = el
            if el == "S":
                start = (x,y)
            if el == "E":
                end = (x,y)
    return heightmap, start, end

def elevation(char):
    elevation = "abcdefghijklmnopqrstuvwxyz"
    if char == "S":
        char = "a"
    if char == "E":
        char = "z"
    return elevation.index(char)

def render_(hm, reconstructed_path):
    from util.console import console
    xmin = min(i[0] for i in hm)
    xmax = max(i[0] for i in hm)
    ymin = min(i[1] for i in hm)
    ymax = max(i[1] for i in hm)
    for y in range(ymin, ymax+1):
        for x in range(xmin, xmax+1):
            if (x,y) in reconstructed_path:
                console.print(f'[red]{hm[(x,y)]}[/red]', end="")
            else:
                console.print(f'[green]{hm[(x,y)]}[/green]', end="")
        console.print("")

def render_function(path):
    def inner(point, points):
        if point in path:
            return f'[red]{points[point]}[/red]'
        else:
            return f'[green]{points[point]}[/green]'
    return inner

# def h(a,b):
#     return abs(a[0]-b[0])+abs(a[1]-b[1])

# def neighbours(heightmap, move_condition):
#     def inner(current):
#         cur_el = elevation(heightmap[current])
#         for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
#             neighbour = current[0]+dx, current[1]+dy
#             if neighbour not in heightmap:
#                 continue
#             if move_condition(cur_el, neighbour):
#                 continue
#             yield neighbour, 1
#     return inner
    
# def find_path(heightmap, start, end_condition, move_condition):
#     """Pathfinder
#     heightmap: Dict[(coord)] -> 'abcdef...'
#     start: the start coord
#     end_condition: Function that evaluates to true when we can quit
#     move_condition: f(current_elevation, neighbour_coordinate) -> true if we can move here """
#     frontier = PriorityQueue()
#     frontier.put(start, 0)
#     cost_so_far = {}
#     cost_so_far[start] = 0
#     path = dict()
#     path[start] = None

#     while not frontier.is_empty():
#         current = frontier.get()
#         if end_condition(current):
#             break
#         cur_el = elevation(heightmap[current])
#         for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
#             neighbour = current[0]+dx, current[1]+dy
#             if neighbour not in heightmap:
#                 continue
#             if move_condition(cur_el, neighbour):
#                 continue
#             new_cost = cost_so_far[current] + 1
#             if neighbour not in cost_so_far or new_cost < cost_so_far[neighbour]:
#                 cost_so_far[neighbour] = new_cost
#                 priority = new_cost
#                 frontier.put(neighbour, priority)
#                 path[neighbour] = current
#     return path, start, current

# def reconstruct_path(path, start, end):
#     current = end
#     reconstructed_path = []
#     while current != start:
#         reconstructed_path.append(current)
#         current = path[current]
#     reconstructed_path.append(start)
#     reconstructed_path.reverse()
#     return reconstructed_path

def neighbours1(heightmap):
    def inner(current):
        cur_el = elevation(heightmap[current])
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbour = current[0]+dx, current[1]+dy
            if neighbour not in heightmap:
                continue
            if elevation(heightmap[neighbour]) > cur_el + 1:
                continue
            yield neighbour, 1
    return inner

@solution_timer(2022,12,1)
def part_one(data: List[str], verbose=False):
    heightmap, start, end = parse(data)

    path, end = search(start, neighbours=neighbours1(heightmap), end=lambda x: x==end, depth_first=True)
    
    reconstructed_path = construct_path(path, end)

    if verbose:
        im = render(heightmap, render_function=render_function(reconstructed_path))
        console.print(im)

    return len(reconstructed_path)-1

def neighbours2(heightmap):
    def inner(current):
        cur_el = elevation(heightmap[current])
        for dx, dy in [(0,1),(1,0),(0,-1),(-1,0)]:
            neighbour = current[0]+dx, current[1]+dy
            if neighbour not in heightmap:
                continue
            if elevation(heightmap[neighbour]) + 1 < cur_el:
                continue
            yield neighbour, 1
    return inner

@solution_timer(2022,12,2)
def part_two(data: List[str], verbose=False):
    heightmap, _, start = parse(data)

    path, end = search(start, neighbours=neighbours2(heightmap), end=lambda x: elevation(heightmap[x])==0, depth_first=True)
    
    reconstructed_path = construct_path(path, end)

    if verbose:
        im = render(heightmap, render_function=render_function(reconstructed_path))
        console.print(im)

    return len(reconstructed_path)-1

if __name__ == "__main__":
    data = read_entire_input(2022,12)
    part_one(data)
    part_two(data)