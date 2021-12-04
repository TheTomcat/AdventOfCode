from typing import DefaultDict, List, Union
from collections import defaultdict, deque
from itertools import islice
from adventofcode.util.input_helper import read_entire_input

transpose = lambda l: list(map(list, zip(*l)))
def quad(p):
    "return the quadrant of p"
    if p[0] == 0 or p[1] == 0:
        return None
    return (1 if p[0] > 0 else -1, 1 if p[1] > 0 else -1)
def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

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
    
    def ids(self):
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

def build_tiles_from_input(raw_input):
    tiles = {}
    length = len(raw_input)
    for i in range(0, length, 12):
        # Read the tile ID
        tile_id = int(raw_input[i].split(" ")[1][:-1])
        t = Tile(tile_id, raw_input[i+1:i+11])
        # print(tile_id)
        tiles[tile_id]=t
    return tiles

def index_tiles_by_edge(tiles):
    index = defaultdict(list)
    for tile_id, tile in tiles.items():
        for id in tile.ids().values():
            index[id].append(tile)
    return index

class Map():
    def __init__(self, available_tiles: "List[Tile]" = []):
        self.tiles = {}
        self.available_tiles = available_tiles
        self.open_edges = deque()
    def fetch_tile_by_id(self, id):
        return list(filter(lambda x: id in x.ids(), self.available_tiles))
    def place_first_tile(self):
        self.tiles[(0,0)] = self.available_tiles.pop(0)
        print(f"Tile {self.tiles[(0,0)]} inserted at (0,0) - {self.tiles[(0,0)].ids()}")
        ids = self.tiles[(0,0)].ids()
        self.open_edges.append(((0,0),(0,1),ids[0]))
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
        
        print(f"Attempting to match side with edge_id {edge_id} at {new_pos}")
        # Grab the tile matching this id, if one exists
        tile = self.fetch_tile_by_id(edge_id)
        if len(tile) == 0:
            print("didn't find one")
            return None
        tile = tile[0]
        print(f"Found a tile, id {tile} ({tile.ids()})")
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
        print(f"Applying transformation {mapping[cardinal[dir]][matching_tile_border_direction]}")
        self.tiles[new_pos] = tile
        new_ids = tile.ids()
        print(f"Now {new_ids[cardinal[dir]+4]} should match {edge_id}")
        # Add the new edges
        if dir != (0,1):
            self.open_edges.append((new_pos, (0,-1), new_ids[3]))
        if dir != (1,0):
            self.open_edges.append((new_pos, (-1,0), new_ids[2]))
        if dir != (-1,0):
            self.open_edges.append((new_pos, (1,0), new_ids[0]))
        if dir != (0,-1):
            self.open_edges.append((new_pos, (0,1), new_ids[1]))
        print(f"Tile placed {tile.id}@{new_pos} matching id {edge_id}")
        return tile
    
    def place_all_tiles(self, start_with=None):
        # tile_edge_index = index_tiles_by_edge(self.available_tiles)
        # if start_with is None:
        #     start_with = self.available_tiles[0].id

        while len(self.available_tiles) > 0:
            self.place_tile()
            # p=input()
    def knit(self):
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

class SpiralIterator:
    def __init__(self, initial_direction=(0,1), CCW = True):
        self.pos = (0,0)
        self.dir = tuple(i for i in initial_direction)
        self.idir = tuple(i for i in initial_direction)
        self.rotate_CCW = CCW
        self._CCW = {a:b for a,b in window([(0,1),(1,0),(0,-1),(-1,0),(0,1)])}
        self._CW =  {b:a for a,b in window([(0,1),(1,0),(0,-1),(-1,0),(0,1)])}
        self.side_length = 1
        self.prev_side_length = None
        self.side_step = 0
    def _rotate(self):
        if self.rotate_CCW:
            self.dir = self._CCW[self.dir]
        else:
            self.dir = self._CW[self.dir]
    def step(self):
        self.prev_pos = tuple(i for i in self.pos)
        self.pos = self.pos[0] + self.dir[0], self.pos[1] + self.dir[1]
        self.side_step += 1
    def rotate(self):
        if self.side_step == self.side_length:
            self._rotate()
            self.side_step = 0
            if self.side_length == self.prev_side_length:
                self.side_length += 1
            else:
                self.prev_side_length = self.side_length
    def __next__(self):
        output = self.pos, self.dir
        self.step() 
        self.rotate()
        return output

    def __iter__(self):
        return self


tiles = build_tiles_from_input(read_entire_input(2020,20))
tile_list = [tile for tile in tiles.values()]
m = Map(tile_list)
print(len(m.available_tiles))
m.place_first_tile()
m.place_all_tiles()
# k = m.knit()
# with open('output.txt','w') as f:
#     for line in k:
#         f.write(line)
# print(m.tiles)
# print(m.open_edges)
# print(len(m.available_tiles))