from collections import defaultdict

def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()

def process(text):
    raw_tiles = text.split('\n\n')
    tiles = {}
    for tile in raw_tiles:
        rows = tile.split('\n')
        index = rows[0][5:9]
        data = rows[1:]
        tiles[int(index)] = data
    # output = {}
    # for tile in tiles
    return tiles
N = (0,1)
E = (1,0)
S = (0,-1)
W = (-1,0)
class Tile(object):
    def __init__(self, tile_id, tile):
        self.id = tile_id
        self.data = tile
        self.calculate_borders()
    def __eq__(self, other):
        return self.id == other.id
    def __hash__(self):
        return self.id
    def calculate_borders(self):
        borders = [0] * 8
        N = ['1' if i=="#" else '0' for i in self.data[0]]
        E = ['1' if row[-1]=="#" else '0' for row in self.data]
        S = ['1' if i=="#" else '0' for i in reversed(self.data[-1])]
        W = ['1' if row[0]=="#" else '0' for row in reversed(self.data)]
        for i,b_id in enumerate([N,E,S,W]):
            borders[i]  = int(''.join(b_id),2)
            borders[i+4] = int(''.join(reversed(b_id)),2)
        self.borders= borders
    @property 
    def N(self):
        return self.get_id('N')
    def get_id(self, direction):
        if direction == 'N':
            return int(''.join(['1' if i=="#" else '0' for i in self.data[0]]),2)
        elif direction == 'E':
            return int(''.join(['1' if row[-1]=="#" else '0' for row in self.data]),2)
        elif direction == 'S':
            return int(''.join(['1' if i=="#" else '0' for i in reversed(self.data[-1])]),2)
        elif direction == 'W':
            return int(''.join(['1' if row[0]=="#" else '0' for row in reversed(self.data)]),2)
    def pprint(self, bid=False):
        if bid:
            print(f"       {self.borders[0]}/{self.borders[4]}")
            for i, row in enumerate(self.data):
                if i == 4:
                    print(f" {self.borders[3]:4} " + ''.join(row) + f" {self.borders[1]:4}")
                elif i==5:
                    print(f" {self.borders[7]:4} " + ''.join(row)+ f" {self.borders[5]:4}")
                else:
                    print(" "*6 + ''.join(row))
            print(f"       {self.borders[2]}/{self.borders[6]}")
        else:
            print('\n'.join([''.join(row) for row in self.data]))

    def rotate90(self):
        newdata = [['.' for i in j] for j in self.data] # Lazy, only works for squares
        rowlength = len(self.data[0])
        collength = len(self.data)
        for rowi, row in enumerate(self.data):
            for coli, val in enumerate(row):
                rrowi = rowlength - rowi - 1
                rcoli = collength - coli - 1
                newdata[coli][rrowi] = val
        self.data = newdata
        self.calculate_borders()
    def rotate180(self):
        newdata = [['.' for i in j] for j in self.data] # Lazy, only works for squares
        rowlength = len(self.data[0])
        collength = len(self.data)
        for rowi, row in enumerate(self.data):
            for coli, val in enumerate(row):
                rrowi = rowlength - rowi - 1
                rcoli = collength - coli - 1
                newdata[rrowi][rcoli] = val
        self.data = newdata
        self.calculate_borders()
    def flip_horizontal(self):
        self.data = [[i for i in reversed(row)] for row in self.data]
        self.calculate_borders()
    def flip_vertical(self):
        self.data = [[i for i in row] for row in reversed(self.data)]
        self.calculate_borders()
    def shared_border(self, other):
        # Create a list of the borders that self and other share
        # We don't want to reverse 'self' so only look in the first 4 positions
        borderlist = set(self.borders[:4]).intersection(set(other.borders))
        if len(borderlist)==0:
            return None
        # find a other.border that matches a self.border
        border_id = borderlist.pop()
        return border_id
    def align(self, other):
        self.calculate_borders()
        border_id = self.shared_border(other) # Is there even a match?
        print(f"Matched with id {border_id}")
        if border_id is None:
            return None
        selfpos = self.borders.index(border_id) # Which border in self is the matching one?
        otherpos = other.borders.index(border_id) # Which border in other is the matching one?
        dest = [6,7,4,5,2,3,0,1] # The mapping of indices matching. 
        # 0: up, 1: right, 2: down, 3: left, 4: up,reverse, 5: right,reverse etc...
        destpos = dest[selfpos] # This is where we need otherpos to be
        print(f"My border is: {selfpos}, matching to {otherpos} ({destpos})")
        # calculate the steps needed to modify other so they line up
        do_we_flip = abs(otherpos // 4 - destpos // 4)
        how_far_rotate = (otherpos - destpos) % 4
        print(f"Flip? {do_we_flip}. Rotate? {how_far_rotate}")
        
        if how_far_rotate % 2 == 1: # Ie, 90 or 270 degrees out
            other.rotate90()
        if how_far_rotate >= 2: # ie, 180 or 270 degrees out
            other.rotate180()
        if do_we_flip:
            if destpos % 2:
                other.flip_vertical()
            else:
                other.flip_horizontal()
        
        #return the direction that other should go
        return other, [N,E,S,W][selfpos%4]
        
      
        # self.pprint()
        # other.pprint()

        # if otherpos // 4 == destpos // 4: # That is, we don't need flipping, just rotation
        #     steps = abs(otherpos%4-destpos%4)
        #     if steps >= 2:
        #         other.rotate180()
        #         steps-=2
        #     if steps >= 1:
        #         other.rotate90()
        # else:

        # modify other
        # return the modified other with borders matching

def neighbours(x,y):
    ngb = [(W,"W"),(N,"N"),(E,"E"),(S,"S")]
    for (i,j),direc in ngb:
        yield (x+i,y+j),direc

class Space:
    def __init__(self):
        self.space = {}
    def contains(self, tile):
        for key in self.space:
            if tile.id == self.space[key].id:
                return True
        return False
    def place_initial(self, tile):
        self.space[(0,0)] = tile
    def bounds(self):
        x,y = tuple(zip(*list(self.space.keys())))
        return (min(x),min(y)),(max(x),max(y))
    def pprint(self, border=True):
        (x0,y0),(x1,y1) = self.bounds()
        xsep = " " if border else ""
        for y in range(y0,y1+1):
            for row in range(10):
                for x in range(x0,x1+1):
                    if (x,y) in self.space:
                        tile = self.space[(x,y)]
                        print(''.join(tile.data[row]), end=xsep)
                    else:
                        print(' ' * 10, end=xsep)
                print()
            if border:
                print()
    def sprint(self):
        for key in self.space:
            print(f"{key}: {self.space[key].id}")

    def place_a_tile(self, tiles):
        for tile in tiles:
            print(f"Examining tile {tile.id}")
            if self.contains(tile):# in self.space:
                print(" > already in space")
                continue # Skip any tiles already placed
            for position in self.space:
                target = self.space[position]
                if not target.shared_border(tile):
                    continue
                rottile, d = target.align(tile)
                print(f'd={d}')
                pos = tuple([i+j for i,j in zip(position, d)])
                self.space[pos] = rottile
                return True
        return False
        # for test_tile in tiles:
        #     if test_tile in self.space:
        #         continue
        #     for target_tile_position in self.space:
        #         print(f"Checking {test_tile.id} around {target_tile_position}")
        #         # Try to match this test_tile to the target
        #         target = self.space[target_tile_position]
        #         if not target.shared_border(test_tile):
        #             continue
        #         else:
        #             d = target.align(test_tile)
        #             print(d)
        #             pos = tuple([i+j for i,j in zip(target_tile_position, d)])
        #             self.space[pos] = target
        #             print(f"Match found! {pos}")
        #             break

    
    def make_borders(self):
        for position in self.space: # For each occupied position
            for neighbour, direction in neighbours(*position): # Look for the surrounding 4 spaces
                if neighbour not in self.space: # Is that space occupied?
                    yield (position,direction)  # If not, then this is a border
    
    

def get_id(tile, direction):
    if direction == 'N':
        return int(''.join(['1' if i=="#" else '0' for i in tile[0]]),2)
    elif direction == 'E':
        return int(''.join(['1' if row[-1]=="#" else '0' for row in tile]),2)
    elif direction == 'S':
        return int(''.join(['1' if i=="#" else '0' for i in reversed(tile[-1])]),2)
    elif direction == 'W':
        return int(''.join(['1' if row[0]=="#" else '0' for row in reversed(tile)]),2)
    
def get_all_ids(tile):
    # print(tile)
    N = ['1' if i=="#" else '0' for i in tile[0]]
    E = ['1' if row[-1]=="#" else '0' for row in tile]
    S = ['1' if i=="#" else '0' for i in reversed(tile[-1])]
    W = ['1' if row[0]=="#" else '0' for row in reversed(tile)]
    ids = {'forward':[],'reverse':[]}
    for i, idlist in enumerate([N,E,S,W]):
        idforward = int(''.join(idlist),2)
        idreverse = int(''.join(reversed(idlist)),2)
        ids['forward'].append(idforward)
        ids['reverse'].append(idreverse)
    return ids

def compile_tile_dict(tiles):
    tile_dict = defaultdict(list)
    for tile_id in tiles:
        tile = tiles[tile_id]
        idlist = get_all_ids(tile)
        idlist = idlist['forward'] + idlist['reverse']
        for edge_id in idlist:
            # edge_id = idlist[direction]
            tile_dict[edge_id].append(tile_id) #(tile_id, tile))
    return tile_dict

def border_id_to_tile(tiles):
    idlist = defaultdict(list)
    for tile_id in tiles:
        tile = tiles[tile_id]
        ids = get_all_ids(tile)
        for border_id in ids['forwards'] + ids['reverse']:
            idlist[border_id].append(tile_id)
    return idlist


# def make_space(tiles):
#     space = {}
#     # place a tile at the origin
#     # choose the tile
#     init_tile_id = [i for i in tiles.keys()][0]
#     space[(0,0)] = (init_tile_id, '')
#     for occupied_position in space:
#         for empty_neighbour in neighbours(*occupied_position):
#             if empty_neighbour in space:
#                 continue
#             occ_neighs = []
#             for occupied_neighbour in neighbours(*empty_neighbour) if occupied_neighbour in space:
#                 if occupied_neighbour in space:
#                     occ_neighs.append(occ)

# def get_direction(origin, new):
#     ox,oy = origin
#     nx,ny = new
#     if oy==ny:
#         if ox<nx:
#             return 'E'
#         else:
#             return 'W'
#     elif ox==nx:
#         if oy<ny:
#             return 'N'
#         else:
#             return 'S'

# tiles = process(read_input(20))

# td = compile_tile_dict(tiles)
# print(td[272])

def insert_tile(tiles, space):
    if len(space) == 0:
        # Space is empty, choose a tile and plop it in the middle
        chosen_tile_id = [tile_id for tile_id in tiles][0] # We'll just take the first one
        space[(0,0)] = chosen_tile_id
        return space

    border_to_tile = border_id_to_tile(tiles)
    # Build a list of available borders
    for position,direction in make_borders(space):
        # Look at a border - does it match any ids in my list?
        tile_id = space[position] # My tile_id
        border_id = get_id(tile_id, direction) # The border in the direction
        b_ids = border_to_tile[border_id]

        
    return space




tiles = process(read_input(20))
tile_obs = [Tile(i, tiles[i]) for i in tiles]
# t = Tile(3461, tiles[3461])
# q = Tile(1613, tiles[1613])
# t.pprint()
# print()
# q.pprint()
# print()
# print(t.align(q))
# print()
# q.pprint()

space = Space()
space.place_initial(tile_obs[0])
space.place_a_tile(tile_obs)
print(list(space.space.keys()))
space.place_a_tile(tile_obs)
print(list(space.space.keys()))
space.place_a_tile(tile_obs)
print(list(space.space.keys()))
space.sprint()
space.pprint()

print(tile_obs[0].pprint(True))

print([i for i in tile_obs if i.id==1613][0].pprint(True))

o = [i for i in tile_obs if i.id==1789][0]
o.pprint(True)
o.rotate180()
o.pprint(True)
# space.space[(0,0)].pprint()
# print()
# space.space[(0,-1)].pprint()

[i for i in tile_obs if i.id==1613][0].align([i for i in tile_obs if i.id==1789][0])