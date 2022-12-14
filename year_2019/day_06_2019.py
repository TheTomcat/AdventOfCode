from collections import defaultdict
from typing import List, Any, Tuple, Dict
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2019,6)

def parse(data: List[str]) -> Any:
    orbits = defaultdict(list)
    orbiting = {}
    for row in data:
        a,b=row.split(")")
        orbits[a].append(b)
        orbiting[b] = a
    return orbits, orbiting

class Node:
    def __init__(self, name, degree=0, parent=None, head=None):
        self.name = name
        self.degree=degree
        self.parent=parent
        self.head=self if head is None else head
        self.children = []
        self.total_degree=0
    def add_child(self, name: str):
        child = Node(name=name, degree=self.degree+1,parent=self,head=self.head)
        self.children.append(child)
        self.head.total_degree += child.degree
        return child
    def __repr__(self):
        return f"Node({self.name})"

def build_orbital_tree(orbits: Dict[str,str], parent: Node):
    for child_name in orbits[parent.name]:
        child = parent.add_child(child_name)
        build_orbital_tree(orbits, child)

def path_to_root(orbiting: Dict[str,str], start):
    parent = orbiting.get(start, None)
    if parent is None:
        return start
    return parent + ',' + path_to_root(orbiting, parent)

def find_node(root: Node, name: str):
    if root.name == name:
        return root
    else:
        for child in root.children:
            return find_node(child, name)

def find_first_common_element(A: list, B: list):
    for a in A:
        if a in B:
            return a

@solution_timer(2019,6,1)
def part_one(data: List[str], verbose=False):
    orbits, _ = parse(data)
    root_node = Node('COM')
    build_orbital_tree(orbits, root_node)
    return root_node.total_degree

@solution_timer(2019,6,2)
def part_two(data: List[str], verbose=False):
    _, orbiting = parse(data)
    your_orbits = path_to_root(orbiting,'YOU').split(",")
    santa_orbits= path_to_root(orbiting,'SAN').split(",")
    first_common_element = find_first_common_element(your_orbits, santa_orbits)
    return your_orbits.index(first_common_element) + santa_orbits.index(first_common_element)
if __name__ == "__main__":
    data = read_entire_input(2019,6)
    part_one(data)
    part_two(data)