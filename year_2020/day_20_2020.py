from typing import Iterator, List, Dict, DefaultDict, Tuple, Union
from operator import mul
from collections import defaultdict, deque
from itertools import accumulate, islice, product

from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import transpose

data = read_entire_input(2020,20)

def parse(data: List[str]) -> Dict[int, "Tile"]:
    tiles = {}
    length = len(data)
    for i in range(0, length, 12):
        # Read the tile ID
        tile_id = int(data[i].split(" ")[1][:-1])
        t = Tile(tile_id, data[i+1:i+11])
        # print(tile_id)
        tiles[tile_id]=t
    return tiles

def quad(p):
    "return the quadrant of p"
    if p[0] == 0 or p[1] == 0:
        return None
    return (1 if p[0] > 0 else -1, 1 if p[1] > 0 else -1)

class Tile(object):
    def __init__(self, id, data=None):
        self.id = id
        self.pixels = []
        if data is not None:
            for row in data:
                new_row  = []
                for col in row:
                    new_row.append(1 if col=="#" else 0)
                self.pixels.append(new_row) 

    def __repr__(self):
        return f"Tile(id={self.id})"
    
    def pprint(self):
        # output = f"{}/{}"
        for row in self.pixels:
            for bit in row:
                output += "#" if bit else "."
            print(output)
            output = ""

    def rot90(self):
        new_tile = Tile(self.id)
        new_pixels = [list(reversed(row)) for row in transpose(self.pixels)]
        new_tile.pixels = new_pixels
        return new_tile
    
    def rot180(self):
        return self.rot90().rot90()
    
    def flipv(self):
        new_tile = Tile(self.id)
        new_tile.pixels = self.pixels[::-1]
        return new_tile
    
    def fliph(self):
        new_tile = Tile(self.id)
        new_tile.pixels = [row[::-1] for row in self.pixels]
        return new_tile
    
    def ids(self) -> List[int]:
        return [
            get_id(self.pixels[0]), # TOP
            get_id([row[-1] for row in self.pixels]), # RIGHT
            get_id(reversed(self.pixels[-1])), # BOTTOM
            get_id(reversed([row[0] for row in self.pixels])), # LEFT
            get_id(reversed(self.pixels[0])),
            get_id(reversed([row[-1] for row in self.pixels])),
            get_id(self.pixels[-1]),
            get_id([row[0] for row in self.pixels])
        ]
    def body(self):
        return [row[1:-1] for row in self.pixels[1:-1]]

def get_id(d: List[Union[str,int]]) -> int:
    return int(''.join(str(i) for i in d),base=2)

def index_tiles_by_edge(tiles: Dict[int, Tile])->DefaultDict[int, List[Tile]]:
    index = defaultdict(list)
    for tile_id, tile in tiles.items():
        for id in tile.ids():
            index[id].append(tile)
    return index

def count_neighbours(tiles: Dict[int, Tile]) -> Dict[int, int]:
    output = {}
    for tile_id, tile in tiles.items():
        neighbours = set()
        for edge_id in tile.ids():
            for tile2_id, tile2 in tiles.items():
                if tile.id == tile2_id:
                    continue
                for edge in tile2.ids():
                    if edge_id == edge:
                        neighbours.add(tile2_id)
        output[tile_id] = len(neighbours)
    return output        

class Map():
    def __init__(self, available_tiles: "List[Tile]" = []):
        self.tiles = {}
        self.available_tiles = available_tiles
        self.open_edges = deque()
    def fetch_tile_by_id(self, id):
        return list(filter(lambda x: id in x.ids(), self.available_tiles))
    def place_first_tile(self):
        self.tiles[(0,0)] = self.available_tiles.pop(0)
        # print(f"Tile {self.tiles[(0,0)]} inserted at (0,0) - {self.tiles[(0,0)].ids()}")
        ids = self.tiles[(0,0)].ids()
        self.open_edges.append(((0,0),(0,1),ids[0])) # Tile position, edge direction, id along that edge
        self.open_edges.append(((0,0),(1,0),ids[1]))
        self.open_edges.append(((0,0),(0,-1),ids[2]))
        self.open_edges.append(((0,0),(-1,0),ids[3]))
    def place_tile(self):
        # Select an edge
        cardinal = {
            (0,1):0,
            (1,0):1,
            (0,-1):2,
            (-1,0):3
        }
        pos, dir, edge_id = self.open_edges.popleft()
        new_pos = pos[0]+dir[0] , pos[1]+dir[1]
        
        # print(f"Attempting to match side with edge_id {edge_id} at {new_pos}")
        # Grab the tile matching this id, if one exists
        tile = self.fetch_tile_by_id(edge_id)
        if len(tile) == 0:
            # print("didn't find one")
            return None
        if len(tile) > 1:
            # print("Found too many")
            raise ValueError("Too many matches")
        tile = tile[0]
        # print(f"Found a tile, id {tile} ({tile.ids()})")
        self.available_tiles.remove(tile)

        new_ids = tile.ids()
        # which ID matches the edge_id?
        matching_tile_border_direction = new_ids.index(edge_id)
        mapping = { # mapping[dir,matching_tile_border_dir]
            0: {
                0:'v',
                1:'rh',
                2:'h',
                3:'rv',
                4:'rr',
                5:'r',
                6:'',
                7:'rrr'
            },
            1: {
                0:'rh',
                1:'h',
                2:'rv',
                3:'v',
                4: 'rrr',
                5: 'rr',
                6:'r',
                7:''
            },
            2: {
                0:'h',
                1:'rv',
                2:'v',
                3:'rh',
                4:'',
                5:'rrr',
                6:'rr',
                7:'r'
            },
            3: {
                3:'h',
                0:'rv',
                1:'v',
                2:'rh',
                5:'',
                6:'rrr',
                7:'rr',
                4:'r'
            }
        }
        for transformation in mapping[cardinal[dir]][matching_tile_border_direction]:
            if transformation == "r":
                tile = tile.rot90()
            if transformation == "h":
                tile = tile.fliph()
            if transformation == "v":
                tile = tile.flipv()
        # print(f"Applying transformation {mapping[cardinal[dir]][matching_tile_border_direction]}")
        if new_pos in self.tiles:
            raise ValueError(f"Uh oh, I already have a tile at {new_pos}")
        self.tiles[new_pos] = tile
        new_ids = tile.ids()
        # print(f"Now {new_ids[cardinal[dir]+4]} should match {edge_id}")
        # Add the new edges
        if dir != (0,1): # UP
            self.open_edges.append((new_pos, (0,-1), new_ids[2])) # Tile position, edge direction, id along that edge
        if dir != (1,0): # 
            self.open_edges.append((new_pos, (-1,0), new_ids[3]))
        if dir != (-1,0):
            self.open_edges.append((new_pos, (1,0), new_ids[1]))
        if dir != (0,-1):
            self.open_edges.append((new_pos, (0,1), new_ids[0]))
        # print(f"Tile placed {tile.id}@{new_pos} matching id {edge_id}")
        return tile
    
    def place_all_tiles(self, start_with=None):
        # tile_edge_index = index_tiles_by_edge(self.available_tiles)
        # if start_with is None:
        #     start_with = self.available_tiles[0].id

        while len(self.available_tiles) > 0:
            self.place_tile()
            # p=input()
    def knit_with_boundaries(self):
        bx, by = self.bounds()
        output = []
        for y in range(by[1],by[0]-1,-1):
            row = ""
            for prow in range(10):
                for x in range(bx[0],bx[1]+1):
                    row += ''.join(['#' if i else '.' for i in self.tiles[(x,y)].pixels[prow]])
                    row += " "
                output.append(row)
                row = ""
            output.append("")
        return output

    def knit(self):
        bx, by = self.bounds()
        output = []
        for y in range(by[1],by[0]-1,-1):
            row = ""
            for prow in range(1,9):
                for x in range(bx[0],bx[1]+1):
                    row += ''.join(['#' if i else '.' for i in self.tiles[(x,y)].pixels[prow][1:-1]])
                output.append(row)
                row = ""
        return output

    def bounds(self):
        keys = list(self.tiles.keys())
        minx, miny, maxx, maxy = 0,0,0,0
        for key in self.tiles.keys():
            if key[0] < minx: 
                minx=key[0]
            if key[0] > maxx:
                maxx=key[0]
            if key[1] < miny: 
                miny=key[1]
            if key[1] > maxy:
                maxy=key[1]
        return (minx, maxx),(miny, maxy)



monster = [
"..................#.",
"#....##....##....###",
".#..#..#..#..#..#..."]

def parse_monster(monster: List[str]) -> List[Tuple[int, int]]:
    "Turn the monster string into a list of coordinates"
    chars = []
    for y, row in enumerate(monster):
        for x, character in enumerate(row):
            if character == "#":
                chars.append((x,y))
    return chars

def rotate_monster(monster: List[Tuple[int, int]]) -> Iterator[Tuple[int, int, list]]:
    "Take the input monster string as defined above then rotate and flip to get all symmetries"
    m90 = [list(reversed(row)) for row in transpose(monster)] 
    m180 = [list(reversed(row)) for row in transpose(m90)] 
    m270 = [list(reversed(row)) for row in transpose(m180)] 
    r = monster[::-1]
    r90 = [list(reversed(row)) for row in transpose(r)] 
    r180 = [list(reversed(row)) for row in transpose(r90)] 
    r270 = [list(reversed(row)) for row in transpose(r180)] 
    yield 21,3,monster # I hardcoded dimensions because I'm lazy
    yield 3,21,m90
    yield 21,3,m180
    yield 3,21,m270
    yield 21,3,r
    yield 3,21,r90
    yield 21,3,r180
    yield 3,21,r270

def build_monster_tiles(original_monster):
    output = []
    for monster in rotate_monster(original_monster):
        output.append((monster[0],monster[1],parse_monster(monster[2])))
    return output

def find_monsters(map, monster):
    tiled = [list(i) for i in map.knit()]
    count = 0
    monsters = build_monster_tiles(monster)
    num_rows = len(tiled)
    num_cols = len(tiled[0])
    for mx, my, monster in monsters:
        for y in range(num_rows - my):
            for x in range(num_cols - mx):
                try:
                    match = all([tiled[y+py][x+px]=="#" for px,py in monster])
                except IndexError as e:
                    print(x,y,px,py)
                    raise e
                if match:
                    count += 1
                    for px, py in monster:
                        tiled[y+py][x+px] = "0"
                # for position_x, position_y in monster:
                #     if tiled[y+position_y][x+position_x] == ".":
    return tiled, count

@solution_timer(2020,20,1)
def part_one(data, verbose=False):
    tiles = parse(data)
    # Old version!!! So sloww
    # neighbours = count_neighbours(tiles)
    # corner_ids = [tile_id for tile_id, count in neighbours.items() if count==2]
    # val = 1
    # for id in corner_ids:
    #     val *= id
    # return val
    # So as it turns out, my solution to part two is much much faster than the one here
    # So whatever. Here's a quicker version.
    tile_list = [tile for tile in tiles.values()]
    m = Map(tile_list)
    m.place_first_tile()
    m.place_all_tiles()
    (minx, maxx),(miny,maxy) = m.bounds()
    return (m.tiles[(minx,miny)].id * 
            m.tiles[(minx,maxy)].id * 
            m.tiles[(maxx,miny)].id * 
            m.tiles[(maxx,maxy)].id)

@solution_timer(2020,20,2)
def part_two(data, verbose=False):
    tiles = parse(data)
    tile_list = [tile for tile in tiles.values()]
    m = Map(tile_list)
    # print(len(m.available_tiles))
    m.place_first_tile()
    m.place_all_tiles()

    tiles, num_monstesr = find_monsters(m, monster)

    count=0
    for row in tiles:
        for col in row:
            if col == "#":
                count += 1
    return count

if __name__ == "__main__":
    data = read_entire_input(2020,20)
    part_one(data)
    part_two(data)