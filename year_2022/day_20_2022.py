from typing import List, Any, Tuple
from framework.helpers import solution_profiler, solution_timer
from framework.input_helper import read_entire_input

from lib.linkedlist import Node

data = read_entire_input(2022,20)
test = """1
2
-3
3
-2
0
4""".split("\n")

def parse(data: List[str]) -> List[int]:
    seq = []
    for line in data:
        seq.append(int(line))
    return seq

# class NodeMod(Node):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#     def get_offset(self, offset, modulus) -> 'NodeMod':
#         if offset == 0:
#             return self
#         elif offset > 0:
#             if self.next is not None:
#                 return self.next.get_offset((offset-1)% (modulus-1))
#         elif offset < 0:
#             if self.prev is not None:
#                 return self.prev.get_offset((offset+1)% (modulus-1))

def build_order(seq: List[int], KEY: int = 1) -> List[Node]:
    nodes = []
    next = Node(seq[0]*KEY, circular_list=True)
    nodes.append(next)
    for item in seq[1:]:
        next = next.insert_after(item*KEY)
        nodes.append(next)
    return nodes

def mix(nodes: List[Node]) -> List[Node]:
    for item in nodes:
        item.move(item.value % (len(nodes)-1))

def find_offset(nodes: List[Node]) -> Node:
    for item in nodes:
        if item.value == 0:
            return item

@solution_timer(2022,20,1)
def part_one(data: List[str], verbose=False):
    seq = parse(data)
    nodes = build_order(seq)
    mix(nodes)
    zero = find_offset(nodes)
    x = zero.get_offset_loop(1000)
    y = x.get_offset_loop(1000)
    z = y.get_offset_loop(1000)
    return x.value+y.value+z.value

@solution_timer(2022,20,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)
    KEY = 811589153
    seq = parse(data)
    nodes = build_order(seq, KEY)
    for _ in range(10):
        mix(nodes)
    zero = find_offset(nodes)
    x = zero.get_offset_loop(1000)
    y = x.get_offset_loop(1000)
    z = y.get_offset_loop(1000)

    return x.value+y.value+z.value

if __name__ == "__main__":
    data = read_entire_input(2022,20)
    part_one(data)
    part_two(data)