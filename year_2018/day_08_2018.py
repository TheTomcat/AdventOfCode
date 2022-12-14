from typing import Iterator, List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2018,8)
test = """2 3 0 3 10 11 12 1 1 0 1 99 2 1 1 2""".split("\n")

def parse(data: List[str]) -> Any:
    data = ' '.join(data)
    data = data.split(' ')
    nodes = []
    for item in data:
        nodes.append(int(item))
    return iter(nodes)

class Node:
    def __init__(self, datastream: Iterator):
        self.num_children = next(datastream)
        self.num_metadata = next(datastream)
        self.children = []
        self.metadata = []
        for i in range(self.num_children):
            self.children.append(Node(datastream))
        for i in range(self.num_metadata):
            self.metadata.append(next(datastream))
    def checksum(self):
        return sum(self.metadata) + sum([child.checksum() for child in self.children])

    def value(self):
        if len(self.children) == 0:
            return sum(self.metadata)
        return sum(self.children[node_index-1].value() if node_index <= len(self.children) else 0 for node_index in self.metadata)


@solution_timer(2018,8,1)
def part_one(data: List[str], verbose=False):
    datastream = parse(data)
    tree = Node(datastream)
    return tree.checksum()

@solution_timer(2018,8,2)
def part_two(data: List[str], verbose=False):
    datastream = parse(data)
    tree = Node(datastream)
    return tree.value()

if __name__ == "__main__":
    data = read_entire_input(2018,8)
    part_one(data)
    part_two(data)