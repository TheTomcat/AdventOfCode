import math
from typing import Dict, Optional, Tuple

import disjoint_set

from util.graph.Graph import Graph, Node, ID, GraphError
from util.graph.priorityqueue import PriorityQueue

def floyd_warshall(g: Graph) -> Dict[ID, Dict[ID,float]]:
    "length of shortest paths between all the pairs of vertices in a directed weighted graph "
    # construct dist matrix V x V initialised to infinity
    dist = {n:{m:math.inf for m,_ in g.nodes()} for n,_ in g.nodes()}
    for n1,n2,w in g.edges():
        dist[n1.id][n2.id] = w
    for n, _ in g.nodes():
        dist[n][n] = 0
    for k,_ in g.nodes():
        for i, _ in g.nodes():
            for j, _ in g.nodes():
                dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])
    return dist

def floyd_warshall_with_path(g: Graph):
    "length of shortest paths between all the pairs of vertices in a directed weighted graph with the actual path"
    # construct dist matrix V x V initialised to infinity
    dist = {n:{m:math.inf for m,_ in g.nodes()} for n,_ in g.nodes()}
    next: Dict[ID, Dict[ID, Optional[Node]]] = {n:{m:None for m,_ in g.nodes()} for n,_ in g.nodes()}
    for n1,n2,w in g.edges():
        dist[n1.id][n2.id] = w
        next[n1.id][n2.id] = n2.id
    for _,n in g.nodes():
        dist[n.id][n.id] = 0
        next[n.id][n.id] = n.id
    for k,_ in g.nodes():
        for i,_ in g.nodes():
            for j,_ in g.nodes():
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
                    next[i][j] = next[i][k]

    return dist, next # 'next' is the floyd_warshall_path used in reconstruct_shortest_path

def reconstruct_shortest_path(start, finish, floyd_warshall_path):
    if floyd_warshall_path[start][finish] is None:
        return []
    node = start
    path = [start]
    while node != finish:
        node = floyd_warshall_path[node][finish]
        path.append(node)
    return path

def prim_MST(g: Graph, start: Node) -> Tuple[Graph, float]:
    "Construct Prim Minimum Spanning Tree"
    if g.directed:
        raise GraphError("Cannot compute MST on a directed graph")
    mst = Graph(directed=False, weighted=g.weighted)
    #visited: Set[ID] = set(start.id)
    cost: float = 0
    edges = PriorityQueue[Tuple[ID, ID]]()
    for to, weight in start.neighbours():
        edges.put((start.id, to.id), weight)
        # https://bradfieldcs.com/algos/graphs/prims-spanning-tree-algorithm/
    mst.add_node(start.id)
    while not edges.is_empty():
        weight, (a_id, b_id) = edges.get_with_priority()
        if b_id not in mst:
            mst.add_node(b_id)
            mst.add_edge(a_id, b_id, weight)
            cost += weight
            for neighbour, weight in g.get_node(b_id).neighbours():
                if neighbour.id not in mst:
                    edges.put((b_id, neighbour.id), weight)
    return mst, cost

def kruskal_MST(g: Graph, start: Node) -> Tuple[Graph, float]:
    "Construct Kruskal Minimum Spanning Tree"
    if g._directed:
        raise GraphError("Cannot compute MST on a directed graph")
    mst = Graph(weighted=g.weighted, directed=False)
    dsu: disjoint_set.DisjointSet[Node] = disjoint_set.DisjointSet()
    cost: float = 0
    # Create edge list
    edge_list = [(w,a,b) for (a,b,w) in g.edges()]
    edge_list.sort()
    for w,a,b in edge_list:
        if not dsu.connected(a,b):
            cost += w
            mst.add_node(a.id)
            mst.add_node(b.id)
            mst.add_edge(a.id, b.id, w)
            dsu.union(a,b)
    return mst, cost