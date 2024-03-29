from itertools import islice, zip_longest

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
