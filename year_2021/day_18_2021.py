from typing import List, Any, Optional, Tuple
from collections import namedtuple, deque
import enum
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,18)

def parse(data: List[str]) -> Any:
    return [(i for i in row) for row in data]
        
class Position(enum.Enum):
    L = 0
    R = 1

def isnumber(n):
    return isinstance(n, int)

SFN = int | "Node"

class Node:
    def __init__(self, stream=None, drop_first=True, parent: Optional["Node"]=None, position=Position.L, depth=0):
        self.L = 0
        self.R = 0
        self.parent = parent
        self.depth = depth
        self.position=position
        if stream is None:
            return
        if drop_first:
            _ = next(stream)
        self.L = self.add_child(stream, Position.L)
        _ = next(stream) # ,
        self.R = self.add_child(stream, Position.R)
        _ = next(stream) # ]

    def add_child(self, stream=None, position=Position.L):
        c = next(stream)
        if c != "[":
            return int(c)
        else:
            return Node(stream, self, position, self.depth + 1)
    
    def explode(self):
        L, R = self.L, self.R
        
        node, position = self.parent, self.position
        # handle the L number first
        while node is not None and position == Position.L: # Stop when we get to a "R" node, or we reach the top
            node, position = node.parent, node.position
        if node is not None: # if we're not at the top yet
            if isnumber(node.L):
                node.L += L
            else:
                node.L.add(Position.R, L)

        node, position = self.parent, self.position
        # handle the L number first
        while node is not None and position == Position.R: # Stop when we get to a "R" node, or we reach the top
            node, position = node.parent, node.position
        if node is not None: # if we're not at the top yet
            if isnumber(node.R):
                node.R += R
            else:
                node.R.add(Position.L, R)
        
        if self.position == Position.L:
            self.parent.L = 0
        if self.position == Position.R:
            self.parent.R = 0

    def get(self, position: Position) -> SFN:
        if position == Position.L:
            return self.L
        else:
            return self.R
        
    def put(self, position: Position, value: int):
        if position == Position.L:
            self.L = value
        else:
            self.R = value

    def add(self, position: Position, value: int):
        v = self.get(position)
        if isnumber(v):
            self.put(position, v+value)
        elif isinstance(v, Node): # Unnecessary but made typechecking happy
            v.add(position, value)
    
    

@solution_timer(2021,18,1)
def part_one(data: List[str]):
    _ = parse(data)

    return False

@solution_timer(2021,18,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,18)
    part_one(data)
    part_two(data)