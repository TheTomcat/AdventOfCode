# graph.py
from typing import (Generator, Hashable, Dict, ItemsView, Iterable, 
        List, Protocol, Sequence, Set, Tuple, TypeVar, Optional, 
        Callable, TypedDict, Union)
from functools import total_ordering

import math

from util.graph.pathfinding import search as _search, A_star as _a_star

#import disjoint_set

ID = Hashable

# http://yaroslavvb.com/upload/graphs2.txt ? Test graphs

class GraphError(Exception): ...
class DirectedGraphError(GraphError): ...
class WeightedGraphError(GraphError): ...
class NodeError(GraphError): ...
class EdgeError(GraphError): ...

@total_ordering
class Node(object):
    def __init__(self, id: ID, payload=None):
        self._id = id
        self._connections: Dict['Node', float] = dict()
        self.payload = payload
    def __repr__(self):
        return self.__class__.__qualname__ + f'(id={self.id})'
    def join(self, n: 'Node', weight=1):
        """Add an edge from this node to `n` with optional `weight`"""
        self._connections[n] = weight
    def neighbours(self) -> Generator[Tuple['Node',float], None, None]: #-> Iterable['Node']:
        """Iterate over the neighbouring nodes -> [(neighbour:Node, weight:float), ...]"""
        yield from self._connections.items()
    @property
    def id(self):
        return self._id
    def __lt__(self, other: 'Node') -> bool: 
        # Hack for ordering within priority queue when nodes have the same priority. It's honestly probably not, but I'm lazy and this was the easiest way. 
        # Obviously can't be used with ids of mixed types. One day I'll fix this, but it isn't a problem for me right now, so it's staying.
        return self.id < other.id 

    def get_weight(self, other: 'Node'):
        try:
            return self._connections[other]
        except KeyError:
            return None
    def __len__(self):
        return len(self._connections)

class NodeData(TypedDict):
    cost: float
    parent: Optional[Node]
    depth: int


Weight = Union[float, int]
Edge = Union[Tuple[ID,ID],Tuple[ID,ID,Weight]]

Path = List[Node]
SearchResult = Dict[Node, NodeData] 
ExtendedSearchResult = Tuple[SearchResult, Node]
EndCondition = Callable[[Node],bool] 
Heuristic = Callable[[Node,Node],float]#Union[...,Callable[[Node,Node,'Graph'],float]]
class NodeLike(Protocol):
    _connections: Dict['NodeLike', float]
    def join(self, n: 'NodeLike', weight: Optional[float]): ...
    def neighbours(self) -> Sequence['NodeLike']: ...
    @property
    def id(self) -> Hashable: ...


class Graph(object):
    def __init__(self, weighted=True, directed=False):
        self._nodes: Dict[ID, Node] = dict()
        self._weighted = weighted
        self._directed = directed
    @property
    def weighted(self):
        return self._weighted
    @property
    def directed(self):
        return self._directed
    def __iter__(self):
        return iter(self._nodes.values())
    def nodes(self) -> Generator[Tuple[ID,Node], None, None]:
        yield from self._nodes.items()
    def nodes_by_id(self) -> Generator[ID, None, None]:
        print("Depreciated call nodes_by_id, instead use for id, node in nodes()")
        yield from self._nodes.keys()
    def nodes_by_node(self) -> Generator[Node, None, None]:
        print("Depreciated call nodes_by_node, instead use for id, node in nodes()")
        yield from self._nodes.values()
    def edges(self) -> Generator[Tuple[Node, Node, float], None, None]:
        for _, node in self.nodes():
            for neighbour, weight in node.neighbours():
                yield (node, neighbour, weight)
    # def select_node(self) -> Node:
    #     """Select a random node from this graph"""
    #     return next(iter(self._nodes.values()))
    def add_node(self, id: ID, payload=None) -> Node:
        "Create a node by ID and add it to the graph. Return the new node. If it already exists, return that node"
        if id in self._nodes:
            return self._nodes[id]
        n = Node(id, payload=payload)
        self._nodes[id] = n
        return n
    def get_node(self, id: ID) -> Node:
        "Fetch a node by ID from the graph."
        try: 
            return self._nodes[id] # self._nodes.get(id, None)
        except KeyError as e:
            raise NodeError from e
    def __contains__(self, id: Union[ID, Node]) -> bool:
        "Does a node exist in this graph? Search by Node object or ID"
        if isinstance(id, Node):
            return id.id in self._nodes
        else:
            return id in self._nodes
    def __len__(self):
        return len(self._nodes)
    def add_edge(self, start: ID, end: ID, weight=1, weight_backwards=None):
        """Add an edge to the graph from start -> end.

        Examples:
        g = Graph(weighted=True, directed=True) ; g.add_node('a') ; g.add_node('b')
        g.add_edge('a','b',1) # Adds an edge from a->b with weight 1
        g.add_edge('a','b',1,2) # Adds an edge from a->b with weight 1 AND b->a with weight 2

        h = Graph(weighted=False, directed=True) ; h.add_node('a') ; h.add_node('b')
        h.add_edge('a','b') # No weight needed, adds an unweighted edge a->b
        h.add_edge('b','a') # Again, no weight needed, adds an unweighted edge b->a

        i = Graph(weighted=True, directed=False) ; i.add_node('a') ; i.add_node('b')
        i.add_edge('a','b',3) # Adds an edge from a->b with weight 3 and from b->a with weight 3

        j = Graph(weighted=False, directed=False) ; j.add_node('a') ; j.add_node('b')
        j.add_edge('a','b') # Adds an unweighted edge a->b AND an unweight edge from b->a

        Args:
            start (ID): The ID of the starting node
            end (ID): The ID of the ending node
            weight (float, optional): The weight of the forward direction edge. Raises an error if the graph is unweighted. Defaults to 0.
            weight_backwards (float, optional): The weight of the reverse edge. Defaults to None.

        Raises:
            DirectedGraphError: [description]
            WeightedGraphError: [description]
        """
        # You have given a backwards weight for an undirected graph. Error
        if weight_backwards is not None and not self._directed: 
            raise DirectedGraphError("This is not a directed graph. You cannot specify a backwards weight for an undirected graph.")
        # You have given a weight for an unweighted graph. Error
        if ((weight != 1) or (weight_backwards is not None)) and not self._weighted: 
            raise WeightedGraphError(f"This is not a weighted graph. You cannot specify a forwards or a backwards weight: weight:{weight}, backwards_weight:{weight_backwards}")
        if start not in self:
            self.add_node(start)
        if end not in self:
            self.add_node(end)
        # Add the edge from start -> end with weight 
        self._nodes[start].join(self._nodes[end],weight) 
        # If we are an undirected graph, add the edge from end->start with weight
        if not self._directed:
            self._nodes[end].join(self._nodes[start],weight)
        # Special case: We are a directed graph, and the user has specified a backwards_weight. Add this edge.
        if self._directed and weight_backwards is not None:
            self._nodes[end].join(self._nodes[start],weight_backwards)
        
    @classmethod
    def from_edge_list(cls, edges: Sequence[Sequence[ID]], weighted: bool=False, directed:bool=False) -> 'Graph':
        g = cls(weighted=weighted, directed=directed)
        # Keep track of the nodes we've mapped so far. 
        # I guess you could also peek inside the graph object? 
        # if g.get_node(node_a_id) is None
        node_index: Dict[ID,Node] = {} 
        if weighted:
            expected_length = 3 # (node, node, weight)
        else:
            expected_length = 2
        for edge in edges:
            try:
                if weighted:
                    node_a_id, node_b_id, weight = edge
                else:
                    node_a_id, node_b_id = edge
            except ValueError as e:
                raise EdgeError(f"Edge supplied with {len(edge)} nodes, expected {expected_length}: Edge={edge}") from e
            if node_a_id not in node_index:
                node_index[node_a_id] = g.add_node(node_a_id)
            if node_b_id not in node_index:
                node_index[node_b_id] = g.add_node(node_b_id)
            if not weighted:
                g.add_edge(node_a_id, node_b_id)
                if not directed:
                    g.add_edge(node_b_id, node_a_id)
            elif weighted:
                g.add_edge(node_a_id, node_b_id, weight)
                if not directed:
                    g.add_edge(node_b_id, node_a_id, weight)
        return g
    
    @classmethod
    def from_adjacency_list(cls, adj_list: Dict[str,Sequence], weighted: bool=False, directed:bool=False) -> 'Graph':
        """Create a graph from a supplied adjacency list (but actually a dictionary...)

        Args:
            adj_list (Dict[str,Sequence]): The adjacency list. 
            weighted (bool, optional): _description_. Defaults to False. If weighted, then the weights should be the second item along with the node as a tuple. 
            directed (bool, optional): _description_. Defaults to False.

        Returns:
            Graph: _description_
        """
        g = cls(weighted=weighted, directed=directed)
        for node, adjacents in adj_list.items():
            g.add_node(node)
            if isinstance(adjacents, dict):
                loop_over: Union[ItemsView,list, tuple] = adjacents.items()
            elif isinstance(adjacents, (list, tuple)):
                loop_over = adjacents
            for e in loop_over:
                if weighted:
                    neighbour, weight = e
                else:
                    neighbour = e
                g.add_node(neighbour)
                if weighted:
                    g.add_edge(node, neighbour, weight)
                else:
                    g.add_edge(node, neighbour)
        return g

class Grid(Graph):
    """Construct a graph in a grid layout, omitting nodes in the list `walls`. Node ids are given by their integer coordinates as a 2-tuple.

    Args:
        width (int): The width of the grid
        height (int): The height of the grid
        walls (List[Tuple[int,int]]): A list of 2-tuples corresponding to coordinates where walls are present
        link_8 (bool, optional): What directions make up neighbours? if True, use 8 directions (N,NE,E,SE,S,SW,W,NW). Otherwise use NSEW. Defaults to True.

    Returns:
        Graph: A graph representation of the above. 
    """
    def __init__(self, width: int, height: int, walls: List[Tuple[int,int]], link_8=True):
        super(Grid, self).__init__(weighted=True, directed=False)
        self.width = width
        self.height = height
        self.walls = walls
        self.from_grid(width, height, walls, link_8)
    def from_grid(self, width: int, height: int, walls: List[Tuple[int,int]], link_8=True):
        for y in range(height):
            for x in range(width):
                if (x,y) in walls:
                    continue
                n = self.add_node((x,y))
                for dx,dy,d in [(0,1,1),(1,1,1.414),(1,0,1),(1,-1,1.414),(0,-1,1),(-1,-1,1.414),(-1,0,1),(-1,1,1.414)]:
                    nx,ny = x+dx, y+dy
                    if not link_8 and d!=1: continue
                    if not (0<=nx<width and 0<=ny<height): continue
                    if (nx,ny) in walls: continue
                    if (nx,ny) not in self:
                        self.add_node((nx,ny))
                    # try:
                    #     neighbour = self.get_node((nx,ny))
                    # except NodeError as e:
                    #     neighbour = self.add_node((nx,ny))
                    self.add_edge((x,y),(nx,ny),d)
    def ascii_print(self, path=None, mapping: Dict[Tuple[int,int],str]=None):
        if mapping is None:
            mapping = {}
        print("___" * self.width + '__')
        for y in range(self.height):
            print('|', end="")
            for x in range(self.width):
                r = ' . '
                try:
                    node = self.get_node((x,y))
                except NodeError as e: # No such node exists
                    r = '###'
                if (x,y) in mapping:
                    r = f' {mapping[(x,y)][0]} '
                print(r, end="")
            print('|')
        print("___" * self.width + '__')

    @staticmethod 
    def l2_norm(a: Node, b: Node) -> float:
        x1,y1 = a.id
        x2,y2 = b.id
        return math.sqrt((x2-x1)**2+(y2-y1)**2)
    @staticmethod
    def l1_norm(a: Node, b: Node) -> float:
        x1,y1 = a.id
        x2,y2 = b.id
        return abs(x1-x2)+abs(y1-y2)
    @staticmethod
    def grid_dist(a: Node, b: Node) -> float:
        x1,y1 = a.id
        x2,y2 = b.id
        dx = abs(x2-x1)
        dy = abs(y2-y1)
        low = min(dx,dy)
        dd = abs(dy-dx)
        return low*1.414 + dd

def search(start: Node, end: EndCondition=None, depth_first=False) -> Union[SearchResult, ExtendedSearchResult]:
    "BFS or DFS search, with implementation for graph and nodes"
    return _search(start, 
                   neighbours = lambda x: x.neighbours(), 
                   end=end, 
                   depth_first=depth_first)

def A_star(start: Node, end:Node, heuristic: Optional[Heuristic]=None) -> ExtendedSearchResult:
    "A* or Dijkstra search with implementation for graph and nodes"
    return _a_star(start=start,
                   end=end,
                   neighbours=lambda x: x.neighbours(),
                   heuristic=heuristic)