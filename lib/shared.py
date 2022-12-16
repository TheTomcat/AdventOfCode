"""A collection of useful functions that I've had to use multiple times, 
so I've just put them together in a single file
"""

from itertools import islice, zip_longest
from typing import Any, Dict, Tuple, TypeVar, List

from lib.allen import AllenInterval

T = TypeVar('T')

transpose = lambda l: list(map(list, zip(*l)))
transpose.__doc__ = "Returns the transpose of a 2d array list-of-lists"

Point = Tuple[int, int]
PointDict = Dict[Point, Any]

def sgn(a):
    if a > 0: 
        return 1
    if a < 0:
        return -1
    return 0

def overlap(Amin, Amax, Bmin, Bmax):
    "For inclusive ranges [Amin,Amax] and [Bmin, Bmax], do the ranges overlap?"
    return Amin <= Bmax and Bmin <= Amax

AllenInterval = AllenInterval 
# For a more definitive solution

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
