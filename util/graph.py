from typing import Any, Dict, Optional, Sequence, Hashable, TypeVar, List, Tuple, Generic, Callable, Union
import heapq as hq
from collections import deque

T = TypeVar('T')

# Adapted largely from https://www.redblobgames.com/pathfinding/a-star/introduction.html
# Amit Patel, Red Blob Games

class PriorityQueue(Generic[T]):
    """A priority queue.
    """
    def __init__(self, elements=None):
        if elements is None:
            elements = []
        self.elements: List[Tuple[float, T]] = elements
    def is_empty(self) -> bool:
        return not self.elements
    def put(self, item: T, priority: float):
        hq.heappush(self.elements, (priority, item))
    def get(self) -> T:
        return hq.heappop(self.elements)[1]
    def get_with_priority(self) -> Tuple[float, T]:
        return hq.heappop(self.elements)
    def __len__(self):
        return len(self.elements)

class Queue(Generic[T]):
    def __init__(self):
        self.elements = deque()
    def is_empty(self) -> bool:
        return not self.elements
    def put(self, x: T):
        self.elements.append(x)
    def putleft(self, x: T):
        self.elements.appendleft(x)
    def get(self) -> T:
        return self.elements.popleft()

Node = Any
Numeric = Union[int, float]
WeightedNode = Tuple[Numeric, Node]
EndCondition = Callable[[Node],bool] 
Heuristic = Callable[[Node,Node],float]
Neighbour = Callable[[Node], List[WeightedNode]]

def search(start, neighbours: Neighbour, end: EndCondition=None, depth_first=False): #Dict[Node, Optional[Node]]:
    """Perform a breadth- or depth-first search of the graph, starting at node `start`. 
    Optionally, end the search early when the end condition is satisfied. 
    For a bredth-first search, depth_first=False. Otherwise a depth_first search is performed. 

    Args:
        start (Node): The starting node
        neighbour (f(Node)->[(Node, weight), (Node, weight), ...]: A function which returns the neighbours of a node
        end (f(Node)-> Bool, optional): A function which, when true, will halt the search early. Defaults to f(x)->False.
        depth_first (bool, optional): Perform a depth_first search. Defaults to False.

    Returns:
        Dict[Node: {'parent':Node, 'weight':float, 'depth':int}]
            A visited_from dictionary of (key,val) pairs where d[node_a]=NodeData(node_b) means that node_a arrived via node_b. `None` represents the starting node.
        end: The end node, if `end` is specified
    """
    if end is None:
        end = lambda x: False
    queue: Queue[Node] = Queue()
    enqueue = queue.put if depth_first else queue.putleft
    enqueue(start)
    visited_from = {}#Dict[Node, Optional[Node]] = {}
    visited_from[start] = {'parent':None, 'cost':0, 'depth':0}
    #print(f'Starting {"depth" if depth_first else "bredth"}-first search...')
    while not queue.is_empty():
        current = queue.get()
        #print(current.id, end=" ")
        for neighbour, weight in neighbours(current):

            if neighbour not in visited_from:
                cweight = visited_from[current]['cost']
                cdepth = visited_from[current]['depth']
                enqueue(neighbour)
                visited_from[neighbour] = {'parent':current, 'cost': cweight+weight, 'depth':cdepth+1}
            if end(neighbour):
                #print(" - End condition satisfied, halting!")
                return visited_from, neighbour
    return visited_from

def A_star(start: Node, end: Node, neighbours: Neighbour, heuristic: Optional[Heuristic]=None, draw=None):
    """Priority-search. Perform an A-star or Dijkstra search on the graph. If heuristic is not provided, will perform standard
    Dijkstra search. If heuristic is provided, perform A-star.

    A heuristic is a function of the form f(Node1, Node2)->float

    Args:
        graph (Graph): The graph object
        start (Node): The starting node
        end (Node): The ending node
        neighbour (f(Node)->[(Node, weight), (Node, weight), ...]: A function which returns the neighbours of a node
        heuristic (f(Node,Node) -> float, optional): A function f(Node,Node) -> float providing a heuristic cost. If no function is provided, perform Dijkstra search. Defaults to None.

    Returns:
        ExtendedSearchResult: Dict[Node: {'parent':Node, 'weight':float, 'depth':int}]
        End: The end node
    """
    queue = PriorityQueue[Node]()
    queue.put(start, 0)
    visited_from = {start: {'parent':None,'cost':0,'depth':0}}
    i=0
    while not queue.is_empty():
        current: Node = queue.get()
        # i+=1
        # if i % 10000 == 0:
        if draw is not None:
            draw(current)
            print(f'cost={visited_from[current]["cost"]}, heur={heuristic(current, end)}')
            print()
            i=input()
            if i!="":
                draw(visited_from[current]['parent'])
            # print(i)

        if current == end:
            break
        for neighbour, weight in neighbours(current):
            new_cost = visited_from[current]['cost'] + weight
            new_depth = visited_from[current]['depth'] + 1
            if neighbour not in visited_from or new_cost < visited_from[neighbour]['cost']:
                visited_from[neighbour] = {'parent':current, 'cost':new_cost, 'depth':new_depth}
                if heuristic is None: # Dijkstra search
                    priority = new_cost
                else: # A-star search
                    priority = new_cost + heuristic(neighbour, end)
                queue.put(neighbour, priority)
    return visited_from, end

def construct_path(visited_from, from_node: Node, weighted=False):
    """Return a path from `from_node` to the root of the spanning tree.

    Args:
        visited_from (Dict[Node, Optional[Node]]): The output of DFS or BFS.
        from_node (Node): [description]

    Returns:
        Path: [description]
    """
    path: List[Node] = []
    current_node = from_node
    while current_node != None:
        if weighted:
            path.append((current_node, visited_from[current_node]['cost']))
        else:
            path.append(current_node)
        parent = visited_from[current_node]
        if parent['parent'] is None:
            path.reverse()
            return path
        current_node = parent['parent']
    path.reverse()
    return path