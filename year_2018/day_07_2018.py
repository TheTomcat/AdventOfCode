from collections import deque
from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from util.graph.Graph import Graph, Node, ID
from util.graph.algorithms import floyd_warshall
from util.graph.priorityqueue import PriorityQueue

from framework.console import console

import bisect

data = read_entire_input(2018,7)
test = """Step C must be finished before step A can begin.
Step C must be finished before step F can begin.
Step A must be finished before step B can begin.
Step A must be finished before step D can begin.
Step B must be finished before step E can begin.
Step D must be finished before step E can begin.
Step F must be finished before step E can begin.""".split("\n")

def parse(data: List[str]) -> Any:
    items = []
    for row in data:
        words = row.split(" ")
        items.append((words[1], words[-3]))
    return items

def find_roots(graph: Graph) -> List[Node]:
    starts = set(a for a,_,_ in graph.edges())
    ends = set(b for _,b,_ in graph.edges())
    return starts.difference(ends)

def compute_order(graph: Graph, roots: List[Node]):
    q = PriorityQueue()
    priority = lambda node: ord(node.id)-64
    for node in roots:
        q.put(node, priority(node))
    ordering = ''
    prerequisites = lambda node: [a for a,b,_ in graph.edges() if b==node] 
    while not q.is_empty():
        node = q.get()
        ordering += node.id
        for neighbour, _ in node.neighbours():
            if all(prereqs.id in ordering for prereqs in prerequisites(neighbour)):
                q.put(neighbour, priority(neighbour))
    return ordering

@solution_timer(2018,7,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    G = Graph.from_edge_list(instructions, directed=True)
    roots = find_roots(G)
    return compute_order(G, roots)

class Worker:
    def __init__(self):
        self._is_free = True
        self.task_done_at = 0
        self.task = None
    def is_free(self):
        return self._is_free
    def assign(self, task, priority_fn, offset, current_time):
        self._is_free = False
        self.task_done_at = priority_fn(task) + offset + current_time
        self.task = task
        return self.task_done_at, priority_fn(task)
    def complete(self, time: Node) -> Node:
        if time >= self.task_done_at and not self.is_free():
            self._is_free = True
            t = self.task
            self.task = None
            return t
    def __repr__(self):
        return f'Worker(free:{self._is_free}, task:{self.task}, done_at:{self.task_done_at})'

def debug(time, workers, done):
    console.print(f' {time: 4}   ' + '   '.join(f'   {worker.task.id if worker.task is not None else "."}    ' for worker in workers) + f'   {"".join(i.id for i in done)}', end='')

def timer(graph: Graph, roots: List[Node], offset=0, verbose=False, num_workers=5):
    priority_fn = lambda node: ord(node.id)-64
    find_prerequisites = lambda node: [a for a,b,_ in graph.edges() if b==node] 

    q = PriorityQueue()
    # Put roots in queue with priority (priority, priority)
    for node in roots:
        q.put(node, (priority_fn(node), priority_fn(node)))

    ordering = ''
    workers: List[Worker] = [Worker() for _ in range(num_workers)]

    if verbose:
        console.print('Second   ' + '   '.join(f'Worker {i+1}' for i in range(len(workers))) + '   Done')

    stops: List[Tuple] = [(0,0,None)] # Stoptime, priority, worker

    # Assign initial tasks
    for worker in workers:
        if q.is_empty():
            break
        task = q.get()
        stops.append((*worker.assign(task, priority_fn, offset, 0), worker))
    stops.sort()
    #print(f'stops: {stops}')
    done = []
    if verbose:
        debug(0, workers, done)
        print()
        
    while len(stops) > 0: 
        c_time, priority, worker = stops.pop(0)

        if worker is None:
            continue
        task = worker.complete(c_time)
        done.append(task)
        for neighbour, _ in task.neighbours():
            if all(prereq in done for prereq in find_prerequisites(neighbour)):
                q.put(neighbour, (priority_fn(neighbour), priority_fn(neighbour) + offset))

        for worker in workers:
            if worker.is_free():
                if not q.is_empty():
                    node = q.get()
                    priorities = worker.assign(node, priority_fn, offset, c_time)
                    bisect.insort(stops, (*priorities, worker))

        if verbose:
            debug(c_time, workers, done)
            print()
    return c_time

@solution_timer(2018,7,2)
def part_two(data: List[str], verbose=False):
    instructions = parse(data)
    G = Graph.from_edge_list(instructions, directed=True)
    roots = find_roots(G)
    return timer(G, roots, verbose=verbose, offset=60, num_workers=5)

if __name__ == "__main__":
    data = read_entire_input(2018,7)
    part_one(data)
    part_two(data)