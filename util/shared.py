"""A collection of useful functions that I've had to use multiple times, 
so I've just put them together in a single file

"""

from itertools import islice, zip_longest
import heapq
from typing import Any, Dict, Tuple, TypeVar

T = TypeVar('T')

transpose = lambda l: list(map(list, zip(*l)))
transpose.__doc__ = "Returns the transpose of a 2d array list-of-lists"

Point = Tuple[int, int]
PointDict = Dict[Point, Any]

def store_nested_dict(dictionary, value, *keys):
    val = dictionary
    for key in keys[:-1]:
        try:
            val = val[key]
        except KeyError as e:
            val[key] = {}
            val = val[key]
    val[keys[-1]] = value
    return dictionary

def sgn(a):
    if a > 0: 
        return 1
    if a < 0:
        return -1
    return 0

def overlap(Amin, Amax, Bmin, Bmax):
    "For inclusive ranges [Amin,Amax] and [Bmin, Bmax], do the ranges overlap?"
    return Amin <= Bmax and Bmin <= Amax

### RENDERING HELPERS

def render(points: PointDict, flipy=False, render_function=None):
    """Take a dictionary with keys corresponding to (x,y) coordinates and display them.

    Args:
        points (Dict[Tuple[int,int],Any]): Dictionary with keys of (x,y) pairs
        flipy (bool, optional): [description]. Defaults to True. Should we flip the image vertically. Sometimes this is useful
        render_function ([type], optional): [description]. Defaults to None. How should a particular key be rendered? 

        render function should be f(Tuple[int,int], Dict[Tuple[int,int]]) -> str
    """
    if render_function is None:
        render_function = lambda p, points: chr(9608) if p in points else ' '
    xmin = min(i[0] for i in points)
    xmax = max(i[0] for i in points)
    ymin = min(i[1] for i in points)
    ymax = max(i[1] for i in points)
    if flipy:
        yrange = range(ymax, ymin-1, -1)
    else:
        yrange = range(ymin, ymax+1)
    image = '\n'.join(''.join(render_function((i,j), points) for i in range(xmin, xmax+1)) for j in yrange)
    return image

### Graph tools

class PriorityQueue:
    def __init__(self):
        self.elements: List[Tuple[float, T]] = []
    def empty(self) -> bool:
        return not self.elements
    def put(self, item: T, priority: float):
        heapq.heappush(self.elements, (priority, item))
    def get(self) -> T:
        return heapq.heappop(self.elements)[1]



### ITERATION HELPERS

def window(seq, n=2):
    "Returns a sliding window (of width n) over data from the iterable"
    "   s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...                   "
    "Originally from python docs, removed for some reason. Now on https://stackoverflow.com/a/6822773"
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result

def grouper(n, iterable, fillvalue=None):
    "grouper(3, 'ABCDEFG', 'x') --> ABC DEF Gxx"
    args = [iter(iterable)] * n
    return zip_longest(fillvalue=fillvalue, *args)

class SpiralIterator:
    """Returns a spiral iterator in 2 dimensions, either clockwise or counterclockwise starting in 
    a specified initial direction. Each element is a current position and a direction in which the next step will be taken. 
                    (-1, 1) <- (0,1) <- (1,1)
                       V                  ^
                    (-1, 0)    (0,0) -> (1,0)      (2,0)
                       V                             ^
                    (-1,-1) -> (0,-1) -> (1,-1) -> (2,-1)
    For instance, the default behaviour is:
    
    >>> for x in SpiralIterator():
            print(x)

    ((0, 0), (1, 0))
    ((1, 0), (0, 1))
    ((1, 1), (-1, 0))
    ((0, 1), (-1, 0))
    ((-1, 1), (0, -1))
    ((-1, 0), (0, -1))
    ((-1, -1), (1, 0))
    ((0, -1), (1, 0))
    ((1, -1), (1, 0))
    ((2, -1), (0, 1))
    """
    def __init__(self, initial_direction=(1,0), CCW = True):
        self.pos = (0,0)
        self.dir = tuple(i for i in initial_direction)
        self.idir = tuple(i for i in initial_direction)
        self.rotate_CCW = CCW
        self._CW = {a:b for a,b in window([(0,1),(1,0),(0,-1),(-1,0),(0,1)])}
        self._CCW =  {b:a for a,b in window([(0,1),(1,0),(0,-1),(-1,0),(0,1)])}
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