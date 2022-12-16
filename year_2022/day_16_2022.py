from collections import defaultdict
import re
from typing import Dict, List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from lib.graph.Graph import Graph, ID
from lib.graph.algorithms import floyd_warshall_with_path, reconstruct_shortest_path, Node
from lib.graph.priorityqueue import PriorityQueue

data = read_entire_input(2022,16)
test = """Valve AA has flow rate=0; tunnels lead to valves DD, II, BB
Valve BB has flow rate=13; tunnels lead to valves CC, AA
Valve CC has flow rate=2; tunnels lead to valves DD, BB
Valve DD has flow rate=20; tunnels lead to valves CC, AA, EE
Valve EE has flow rate=3; tunnels lead to valves FF, DD
Valve FF has flow rate=0; tunnels lead to valves EE, GG
Valve GG has flow rate=0; tunnels lead to valves FF, HH
Valve HH has flow rate=22; tunnel leads to valve GG
Valve II has flow rate=0; tunnels lead to valves AA, JJ
Valve JJ has flow rate=21; tunnel leads to valve II""".split("\n")

def parse(data: List[str]) -> Dict[str,tuple]:
    pattern = r'Valve (\w+) has flow rate=(\d+); tunnels* leads* to valves* (.+)'
    matcher = re.compile(pattern)
    valves = {}
    for line in data:
        valve, flow_rate, tunnels = matcher.search(line).groups()
        valves[valve] = (int(flow_rate), tunnels.split(", "))
    return valves

class PumpGraph(Graph):
    @classmethod
    def from_valve_data(cls, valve_data) -> 'Graph':
        """Create a graph from a supplied adjacency list (but actually a dictionary...)

        Args:
            adj_list (Dict[str,Sequence]): The adjacency list. 
            weighted (bool, optional): _description_. Defaults to False. If weighted, then the weights should be the second item along with the node as a tuple. 
            directed (bool, optional): _description_. Defaults to False.

        Returns:
            Graph: _description_
        """
        g = cls(weighted=True, directed=True)
        for valve, (flow, tunnels) in valve_data.items():
            a = g.add_node(valve, flow)
            #b = g.add_node(valve+'on', 0)
            #a.join(b, 1)
            #b.join(a, 0)
            for neighbour in tunnels:
                c = g.add_node(neighbour, valve_data[neighbour][0])
                #d = g.add_node(neighbour+'on', 0)
                #c.join(d, 1)
                #d.join(c, 0)
                g.add_edge(valve, neighbour, 1)
        return g

# def priority_search(start, max_time=30):
#     """Priority-search. """
#     queue = PriorityQueue[Node]()
#     queue.put(start, (0,0)) # Weight = flow, time_elapsed
#     paths = {}
#     paths[start] = [{'path': [start], 'open':set(), 'cum_flow':0, 'time': 0}]
#     #visited_from[start] = [{'path': start.id, 'current_time':0, 'total_flow':0}]
#     while not queue.is_empty():
#         current = queue.get()
#         for neighbour, _ in current.neighbours():
#             new_path = [i for i in current['path']] + [neighbour]
            


#             time_at_node = visited_from[current]['time'] + 1
#             total_flow_if_on = visited_from[current]['flow'] + (max_time-time_at_node) * current.payload
#             time_if_on = time_at_node + 1
#             path = visited_from[current]['path']

#             visited_from[neighbour].append()
#                 # or total_flow > visited_from[neighbour]['flow']:
#                 visited_from[neighbour] = {'parent':current, 'time':time_at_node, 'flow':total_flow}
#                 queue.put(neighbour, total_flow)
#     return visited_from

def compute_best_flow(G: Graph, start: ID, max_time: int):
    paths = [(G.get_node(start), [], 0)]
    best_flows = {}

    for t in range(1,max_time+1):
        new_paths = []

        for current_valve, opened_valves, current_flow in paths:
            index = (current_valve.id, ','.join(i.id for i in opened_valves))
            if (index) in best_flows and current_flow <= best_flows[index]:
                continue
            best_flows[index] = current_flow

            extra_flow = current_valve.payload
            if current_valve not in opened_valves and extra_flow > 0:
                new_paths.append((current_valve, opened_valves+[current_valve], current_flow + extra_flow*(max_time-t)))
            for neighbour, _ in current_valve.neighbours():
                new_paths.append((neighbour, opened_valves, current_flow))
        paths = new_paths
    return paths

@solution_timer(2022,16,1)
def part_one(data: List[str], verbose=False):
    valves = parse(data)
    G = PumpGraph.from_valve_data(valves) #{valve: tunnels for valve, (flow, tunnels) in valves.items()})
    paths = compute_best_flow(G, 'AA', 30)
    return max(flow for _,_,flow in paths)
    #get_flow = lambda valve: valves[valve][0]
    
    #FWG, paths = floyd_warshall_with_path(G)
    #max_flow_rate = max((flow, valve) for valve, (flow, _) in valves.items())
    #return G, FWG, paths

@solution_timer(2022,16,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2022,16)
    part_one(data)
    part_two(data)