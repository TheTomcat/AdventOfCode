from collections import deque
from typing import Deque, List, Any, Set, Tuple, Dict
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,12)
test = """start-A
start-b
A-c
A-b
b-d
A-end
b-end""".split('\n')

def parse(data: List[str]) -> Dict[str,str]:
    edges = set()
    nodes = set()
    for row in data:
        a,b = row.split("-")
        nodes.add(a)
        nodes.add(b)
        edges.add((a,b))
        edges.add((b,a))
    return nodes, edges

def step(node: str, edges: Set[Tuple[str,str]]) -> List[str]:
    E = list(filter(lambda x: x[0]==node, edges))
    return E

@solution_timer(2021,12,1)
def part_one(data: List[str], verbose=False):
    V, E = parse(data)
    front = deque()
    front.append((['start'],['start'])) # Route, Visited small caves
    paths = []
    while len(front) > 0:
        path, visited = front.popleft()
        #print(path, visited)
        next = step(path[-1], E)
        for edge in next:
            n = edge[1]
            if n == 'end':
                paths.append(path + [n])
                continue
            if n in visited:
                continue
            N = [n] if n.islower() else []
            front.append((path + [n], visited + N))
    return len(paths)

@solution_timer(2021,12,2)
def part_two(data: List[str], verbose=False):
    V, E = parse(data)
    front: Deque[List[str], Set[str], str] = deque() 
    front.append((['start'],set(['start']), "")) # Route, Visited small caves, double-visited cave
    paths = []
    while len(front) > 0:
        path, visited, twice_visited = front.popleft()
        #print(path, visited)
        next = step(path[-1], E)
        for edge in next:
            n_twice_visited = twice_visited
            n_visited = {v for v in visited}
            n = edge[1]
            if n == 'end':
                paths.append(path + [n])
                continue
            if n == 'start':
                continue
            if n in visited and twice_visited != "":
                continue
            if n in visited and twice_visited == "":
                n_twice_visited = n
            n_path = path + [n]
            if n.islower():
                n_visited = visited | {n}
            front.append((n_path, n_visited, n_twice_visited))
    return len(paths)

if __name__ == "__main__":
    data = read_entire_input(2021,12)
    part_one(data)
    part_two(data)