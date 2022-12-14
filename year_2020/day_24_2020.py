from typing import DefaultDict, Iterator, List, Any, Tuple
from collections import defaultdict
from itertools import chain
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window

data = read_entire_input(2020,24)
test="""sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew""".split("\n")

def parse(data: List[str]) -> List[List[str]]:
    directions = []
    for direction in data:
        path = []
        skip=False
        for i, x in enumerate(direction):
            if skip:
                skip=False
                continue
            elif x in 'ew':
                path.append(x)
            elif x in 'ns':
                path.append(x+direction[i+1])
                skip = True
        directions.append(path)
    return directions

def take_step(position: Tuple[int, int], step: str) -> Tuple[int, int]:
    """Takes a single step in a specified direction along a q,r axis (described by Amit Patel here https://www.redblobgames.com/grids/hexagons/#coordinates)

    Args:
        position (Tuple[int, int]): The position to start from 
        step (str, one of ['ne','e','se','sw','w','nw']): The direction along a hex grid in which to travel

    Returns:
        Tuple[int, int]: The final position
    """
    q,r = position
    if step == "ne":
        q += 1
        r -= 1
    elif step == "e":
        q += 1
    elif step == "se":
        r += 1
    elif step == "sw":
        q -= 1
        r += 1
    elif step == "w":
        q -= 1
    elif step == "nw":
        r -= 1
    return q,r

def execute_direction(start: Tuple[int, int], direction: List[str]):
    """Take a direction list (a list of strings of valid steps) and step through them returning the final position

    Args:
        start (Tuple[int, int]): Starting position 
        direction (List[str]): A list of valid steps as described in take_step

    Returns:
        Tuple[int, int]: The final position 
    """
    position = start
    for step in direction:
        position = take_step(position, step)
    return position    

def get_initial_tiles(start: Tuple[int, int], directions: List[List[str]]) -> DefaultDict[Tuple[int, int], bool]:
    """Given a list of directions (a list of lists of strings) execute them all and find out which tiles flip

    Args:
        start (Tuple[int, int]): The start position for each direction
        directions (List[List[str]]): The directions

    Returns:
        DefaultDict[Tuple[int, int], bool]: A dictionary object with keys representing (q,r) coordinates and values corresponding to is_black for a tile at that coordinate
    """
    tiles = defaultdict(lambda: False)
    for direction in directions:
        position = execute_direction(start, direction)
        tiles[position] = not tiles[position]
    return tiles

def hexagonal_neighbours(position: Tuple[int, int]) -> Iterator[Tuple[int, int]]:
    q,r = position
    yield from [(q+1,r-1),(q+1,r),(q,r+1),(q-1,r+1),(q-1,r),(q,r-1)]

def count_black_neighbours(tiles: DefaultDict[Tuple[int, int], bool], position) -> int:
    return sum([neighbour in tiles and tiles[neighbour] for neighbour in hexagonal_neighbours(position)])
    #return sum([tiles[neighbour] for neighbour in hexagonal_neighbours(position)]) 
    # Avoid "peeking" into the defaultdict because this causes a RuntimeError: dictionary changed size during iteration for the (slightly) faster approach

def get_bounds(tiles: DefaultDict[Tuple[int, int], bool]) -> Tuple[Tuple[int,int],Tuple[int,int]]:
    minx, miny, maxx, maxy = 0,0,0,0
    for key in tiles.keys():
        if key[0] < minx: 
            minx=key[0]
        if key[0] > maxx:
            maxx=key[0]
        if key[1] < miny: 
            miny=key[1]
        if key[1] > maxy:
            maxy=key[1]
    return (minx, maxx),(miny, maxy)

def simulate_day(tiles: DefaultDict[Tuple[int, int], bool]) -> DefaultDict[Tuple[int, int], bool]:
    # I iterate over the boundaries of the entire space + 1 so as to catch the neighbours of all black tiles.
    # I could probably iterate over each tile and its neighbours and get a quicker result?
    (qmin, qmax),(rmin,rmax) = get_bounds(tiles)
    to_flip = set()
    for q in range(qmin-1, qmax+2):
        for r in range(rmin-1, rmax+2):
            is_black = tiles[(q,r)]
            black_count = count_black_neighbours(tiles, (q,r))
            if is_black and (black_count==0 or black_count>2):
                to_flip.add((q,r))
            if not is_black and black_count == 2:
                to_flip.add((q,r))
    for q,r in to_flip:
        tiles[(q,r)] = not tiles[(q,r)]
    return tiles

def simulate_day2(tiles: DefaultDict[Tuple[int, int], bool]) -> DefaultDict[Tuple[int, int], bool]:
    to_flip = set()
    for tile in tiles:
        for neighbour in chain(hexagonal_neighbours(tile), [tile]):
            if neighbour in tiles:
                is_black = tiles[neighbour]
            else:
                is_black = False
            black_count = count_black_neighbours(tiles, neighbour)
            if is_black and (black_count==0 or black_count>2):
                to_flip.add(neighbour)
            if not is_black and black_count == 2:
                to_flip.add(neighbour)
    for q,r in to_flip:
        tiles[(q,r)] = not tiles[(q,r)]
    return tiles

@solution_timer(2020,24,1)
def part_one(data: List[str], verbose=False):
    directions = parse(data)
    tiles = get_initial_tiles((0,0), directions)
    return sum([tiles[coord] for coord in tiles])

@solution_timer(2020,24,2)
def part_two(data: List[str], verbose=False):
    directions = parse(data)
    tiles = get_initial_tiles((0,0), directions)
    for _ in range(100):
        tiles = simulate_day2(tiles) # about twice as fast as simulate_day
    return sum([tiles[coord] for coord in tiles])

if __name__ == "__main__":
    data = read_entire_input(2020,24)
    part_one(data)
    part_two(data)