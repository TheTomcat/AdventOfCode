from typing import List, Any, Optional, Tuple, Type
from collections import namedtuple, deque
from itertools import product
import enum
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2021,18)
test = """[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]""".split('\n')
test2 = """[[[0,[4,5]],[0,0]],[[[4,5],[2,6]],[9,5]]]
[7,[[[3,7],[4,3]],[[6,3],[8,8]]]]
[[2,[[0,8],[3,4]]],[[[6,7],1],[7,[1,6]]]]
[[[[2,4],7],[6,[0,5]]],[[[6,8],[2,8]],[[2,1],[4,5]]]]
[7,[5,[[3,8],[1,4]]]]
[[2,[2,2]],[8,[8,1]]]
[2,9]
[1,[[[9,3],9],[[9,0],[0,7]]]]
[[[5,[7,4]],7],1]
[[[[4,2],2],6],[8,7]]""".split("\n")
def parse(data: List[str]) -> Any:
    return [row for row in data]
        
class Position(enum.Enum):
    L = 0
    R = 1

def isnumber(n):
    return isinstance(n, int)

class Node:
    def __init__(self, stream=None, drop_first=True, parent: Optional["Node"]=None, position=Position.L, depth=0):
        if isinstance(stream, str):
            stream = iter(stream)
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

    def __repr__(self):
        return f'[{self.L},{self.R}]'

    def add_child(self, stream=None, position=Position.L):
        c = next(stream)
        if c == "[":
            return Node(stream, drop_first=False, parent=self, position=position, depth=self.depth + 1)
        return int(c)
    
    def explode(self):
        L, R = self.L, self.R
        assert isnumber(L) and isnumber(R)
        
        node, position = self.parent, self.position
        # handle the L number first
        while node is not None and position == Position.L: # Stop when we get to a "R" node, or we reach the top
            node, position = node.parent, node.position
        if node is not None: # if we're not at the top yet
            if isnumber(node.L):
                node.L += L
            else:
                node.L.join(Position.R, L)

        node, position = self.parent, self.position
        # handle the L number first
        while node is not None and position == Position.R: # Stop when we get to a "R" node, or we reach the top
            node, position = node.parent, node.position
        if node is not None: # if we're not at the top yet
            if isnumber(node.R):
                node.R += R
            else:
                node.R.join(Position.L, R)
        
        # if self.parent is not None:
        if self.position == Position.L:
            self.parent.L = 0
        if self.position == Position.R:
            self.parent.R = 0

    def get(self, position: Position):
        """Return the child of this node (L or R)"""
        if position == Position.L:
            return self.L
        else:
            return self.R
        
    def put(self, position: Position, node: "Node"):
        "Insert `node` as a child to this node, either position L or R"
        if position == Position.L:
            self.L = node
        else:
            self.R = node

    def split(self, position: Position):
        v = self.get(position)
        if isnumber(v):
            node = Node()
            node.L = int(v//2)
            node.R = int((v-1)//2+1)
            node.depth = self.depth+1
            node.parent = self
            node.position = position
            self.put(position, node)

    def join(self, position: Position, value: int):
        v = self.get(position)
        if isnumber(v):
            try:
                self.put(position, v+value)
            except TypeError as e:
                print(v, value, position)
                raise e
        elif isinstance(v, Node): # Unnecessary but made typechecking happy
            v.join(position, value)
    
    def mag(self):
        L = self.L if isnumber(self.L) else self.L.mag()
        R = self.R if isnumber(self.R) else self.R.mag()
        return 3*L + 2*R

    def __add__(self, other: "Node"):
        total = Node(f'[{self},{other}]')
        return total
    
    def increase_depth(self):
        self.depth += 1
        if not isnumber(self.L):
            self.L.increase_depth()
        if not isnumber(self.R):
            self.R.increase_depth()

    def find_and_explode(self):
        if self.depth >= 4:
            self.explode()
            return True
        if not isnumber(self.L):
            if self.L.find_and_explode():
                return True
        if not isnumber(self.R):
            if self.R.find_and_explode():
                return True
        return False

    def find_and_split(self):
        if isnumber(self.L) and self.L >= 10:
            self.split(Position.L)
            return True
        if not isnumber(self.L) and self.L.find_and_split():
            return True
        if isnumber(self.R) and self.R >= 10:
            self.split(Position.R)
            return True
        if not isnumber(self.R) and self.R.find_and_split():
            return True
        return False

    def reduce(self):
        while True:
            if self.find_and_explode():
                continue
            if self.find_and_split():
                continue
            return

@solution_timer(2021,18,1)
def part_one(data: List[str], verbose=False):
    numbers = parse(data)
    total: Node = Node(numbers[0])
    for number in numbers[1:]:
        total = total + Node(number)
        total.reduce()
    return total.mag()

@solution_timer(2021,18,2)
def part_two(data: List[str], verbose=False):
    numbers = parse(data)
    totals = []
    for a, b in product(numbers, repeat=2):
        if a == b:
            continue
        a = Node(a)
        b = Node(b)
        c = a+b
        c.reduce()
        totals.append(c.mag())
    return max(totals)

if __name__ == "__main__":
    data = read_entire_input(2021,18)
    part_one(data)
    part_two(data)