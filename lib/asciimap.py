from collections import defaultdict
from typing import Callable, Optional


Position = tuple[int,int]
AsciiMap = dict[Position, str]

Bounds = tuple[int, int, int, int]

UP = (0,-1)
RIGHT = (1,0)
DOWN = (0,1)
LEFT = (-1,0)
UDLR = [UP,RIGHT,DOWN,LEFT]

class AsciiMap(object):
    W: int
    H: int
    mapdata: dict
    def parse(self, data: list[str], mut: Optional[Callable] = None, store_reverse_lookup: bool = False):
        ...
    def __init__(self, data: list[str], mut: Optional[Callable] = None, store_reverse_lookup: bool = False):
        self.reverse_lookup = defaultdict(list)
        self.parse(data, mut, store_reverse_lookup)
    def __contains__(self, position: Position):
        x,y = position
        return 0 <= x < self.W and 0 <= y < self.H
    def __getitem__(self, k):
        if k in self.mapdata:
            return self.mapdata[k]
        return None
    def __iter__(self):
        for y in range(self.H):
            for x in range(self.W):
                yield (x,y)
    def render(self, bounds: Optional[Bounds] = None, fill=".", format: Optional[Callable[[int, int, str], str]] = None):
        """Render grid. 
        Optionally, supply bounds [xmin, xmax, ymin, ymax]
        Optionally, supply `fill` when data unavailable (SparseMap)
        Optionally, supply Callable to format map - (x,y,v) -> character/s"""
        if bounds is None:
            W = min(self.W, 40) 
            H = min(self.H, 40)
            xmin, xmax = 0, W
            ymin, ymax =  0, H
        else:
            xmin, xmax, ymin, ymax = bounds
            ymax += 1
            xmax += 1
        output = ""
        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                v = self.mapdata[(x,y)] if (x,y) in self.mapdata else fill
                if format is not None:
                    v = format(x, y, v)
                output += v
            output += "\n"
        return output

class DenseAsciiMap(AsciiMap):
    """Process a grid of ascii characters, storing the characters
     as elements in a dictionary of the form dict[(x,y)] = '#'
     Optionally, provide a function to mutate the strings `mut`"""
    def parse(self, data: list[str], mut: Optional[Callable] = None, store_reverse_lookup: bool = False):
        self.mapdata = {}
        for y, row in enumerate(data):
            for x, col in enumerate(row):
                val = col if mut is None else mut(col)
                self.mapdata[(x,y)] = val
                if store_reverse_lookup:
                    self.reverse_lookup[val].append((x,y))
        self.H = len(data)
        self.W = len(data[0])
    
class SparseAsciiMap(AsciiMap):
    """Process a grid of ascii characters, storing the characters
    as elements in a dictionary. 
    Ignore certain characters as for a sparse map
    Optionally, build a reverse lookup table so as to iterate over the coordinates of specific points.
    Optionally, supply a mutation function to transform the input data. """
    def __init__(self, data: list[str], ignore: str = "", store_reverse_lookup: bool = False, mut: Optional[Callable] = None):
        self.reverse_lookup = defaultdict(list)
        self.parse(data, ignore, store_reverse_lookup, mut)
    def parse(self, data: list[str], ignore: str, store_reverse_lookup: bool=False, mut: Optional[Callable] = None):
        self.mapdata = {}
        for y, row in enumerate(data):
            for x, col in enumerate(row):
                if col in ignore:
                    continue
                if mut:
                    val = mut(col)
                else:
                    val = col
                self.mapdata[(x,y)] = val
                if store_reverse_lookup:
                    self.reverse_lookup[val].append((x,y))
        self.H = len(data)
        self.W = len(data[0])
