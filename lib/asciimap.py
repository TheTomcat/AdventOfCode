from collections import defaultdict


Position = tuple[int,int]
AsciiMap = dict[Position, str]

class AsciiMap(object):
    W: int
    H: int
    mapdata: dict
    def parse(self, data: list[str]):
        ...
    def __init__(self, data: list[str]):
        self.parse(data)
    def __contains__(self, position: Position):
        x,y = position
        return 0 <= x < self.W and 0 <= y < self.H
    def __iter__(self):
        for y in range(self.H):
            for x in range(self.W):
                yield (x,y)
    def render(self, bounds=None, fill="."):
        if bounds is None:
            xmin, xmax = 0, self.W
            ymin, ymax =  0, self.H
        else:
            xmin, xmax, ymin, ymax = bounds
            ymax += 1
            xmax += 1
        output = ""
        for y in range(ymin, ymax):
            for x in range(xmin, xmax):
                output += self.mapdata[(x,y)] if (x,y) in self.mapdata else fill
            output += "\n"
        return output

class DenseAsciiMap(AsciiMap):
    """Process a grid of ascii characters, storing the characters
     as elements in a dictionary of the form dict[(x,y)] = '#'"""
    def parse(self, data: list[str]):
        self.mapdata = {}
        for y, row in enumerate(data):
            for x, col in enumerate(row):
                self.mapdata[(x,y)] = col
        self.H = len(data)
        self.W = len(data[0])
    
class SparseAsciiMap(AsciiMap):
    """Process a grid of ascii characters, storing the characters
    as elements in a dictionary. 
    Ignore certain characters as for a sparse map
    Optionally, build a reverse lookup table so as to iterate over the coordinates of specific points"""
    def __init__(self, data: list[str], ignore: str = "", store_reverse_lookup: bool = False):
        self.reverse_lookup = defaultdict(list)
        self.parse(data, ignore, store_reverse_lookup)
    def parse(self, data: list[str], ignore: str, store_reverse_lookup: bool=False):
        self.mapdata = {}
        for y, row in enumerate(data):
            for x, col in enumerate(row):
                if col in ignore:
                    continue
                self.mapdata[(x,y)] = col
                if store_reverse_lookup:
                    self.reverse_lookup[col].append((x,y))
        self.H = len(data)
        self.W = len(data[0])
