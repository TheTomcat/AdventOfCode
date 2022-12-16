from typing import List, Any, Optional, Tuple
from framework.helpers import solution_profiler, solution_timer
from framework.input_helper import read_entire_input

from framework.console import console

import operator

data = read_entire_input(2018,9)
test = """10 players; last marble is worth 1618 points
13 players; last marble is worth 7999 points
17 players; last marble is worth 1104 points
21 players; last marble is worth 6111 points
30 players; last marble is worth 5807 points""".split("\n")

def parse(data: List[str]) -> Any:
    games = []
    for game in data:
        players, _, _, _, _, _, points, _ = game.split(" ")
        games.append((int(players), int(points)))
    return games

def play(num_players, last_marble_point, verbose=False):
    game_running = True
    
    points = {i+1:0 for i in range(num_players)}

    circle = [0]
    insertion_position = 0
    next_marble = 0
    current_player = 0

    circle_length = 1

    if verbose:
        console.print('[---------]  [red]0[/red]')

    while next_marble <= last_marble_point:
        next_marble += 1
        current_player = (current_player ) % num_players + 1

        if (next_marble % 23) == 0:
            points[current_player] += next_marble
            insertion_position = (insertion_position - 7) % len(circle) 
            points[current_player] += circle.pop(insertion_position)
            #insertion_position += 1
        else:
            insertion_position = (insertion_position + 1) % len(circle) + 1
            circle.insert(insertion_position, next_marble)
        if verbose:
            console.print(f'[{current_player:2}-{points[current_player]:6}]' + ''.join(f"[red]{marble:3}[/red]" if index==insertion_position else f"{marble:3}" for index, marble in enumerate(circle)), end="")
            input()
    return points

class Node:
    def __init__(self, val, circular_list=False):#, head=None, tail= None):
        self.value = val
        if circular_list:
            pointer = self
        else:
            pointer = None
        self.next: Node = pointer
        self.prev: Node = pointer
        # if head is None:
        #     self.head: Node = pointer
        # if tail is None:
        #     self.tail: Node = pointer
    def insert_after(self, val):
        b = Node(val)
        c = self.next
        if c is not None:
            c.prev = b        
        b.prev = self
        b.next = c
        self.next = b
        return b
    def insert_before(self, val):
        b = Node(val)
        a = self.prev
        if a is not None:
            a.next = b        
        b.prev = a
        b.next = self
        self.prev = b
        return b
    def delete(self):
        a, c = self.prev, self.next
        if a is not None:
            a.next = c
        if c is not None:
            c.prev = a
        return self.value
    def get_offset(self, offset):
        if offset == 0:
            return self
        elif offset > 0:
            if self.next is not None:
                return self.next.get_offset(offset-1)
        elif offset < 0:
            if self.prev is not None:
                return self.prev.get_offset(offset+1)
    def __iter__(self):
        start = self
        yield self
        node = start.next
        while node != start:
            yield node
            if node.next is not None:
                node = node.next
            else:
                break
    def __repr__(self):
        return f'Node({self.value})'#f'[' + (f'..., Node({self.prev.value}), ' if self.prev is not None else '') + f'Node({self.value})' + (f', Node({self.next.value}), ...' if self.next is not None else '') + ']'

# class DoublyLinkedList:
#     def __init__(self, nodes: List=None):
#         self.head = None
#         if nodes is not None:
#             node = Node(nodes.pop(0))
#             self.head = node
#             for value in nodes:
#                 node.next = Node(value)
#                 node = node.next
#         self.tail = None
#     def __iter__(self):
#         node = self.head
#         while node is not None:
#             yield node
#             node = node.next

#     def append(self, val):
#         if self.tail is None:
#             self.head = Node(val)
#             self.tail = self.head
#         else:
#             self.tail.next = Node(val)
#             self.tail = self.tail.next

def play_linked_list(num_players, last_marble_point, verbose=False):
    points = {i+1:0 for i in range(num_players)}

    #circle = DoublyLinkedList([0])
    head = Node(0, circular_list=True)
    insertion_pointer = head
    next_marble = 0
    current_player = 0

    circle_length = 1

    if verbose:
        console.print('[---------]  [red]0[/red]')

    while next_marble <= last_marble_point:
        next_marble += 1
        current_player = (current_player ) % num_players + 1

        if (next_marble % 23) == 0:
            points[current_player] += next_marble
            to_be_deleted = insertion_pointer.get_offset(-7)
            insertion_pointer = to_be_deleted.next
            #insertion_position = (insertion_position - 7) % circle_length
            points[current_player] += to_be_deleted.delete()
            #insertion_position += 1
        else:
            #insertion_position = (insertion_position + 1) % len(circle) + 1
            insertion_pointer = insertion_pointer.next.insert_after(next_marble)
            #circle.insert(insertion_position, next_marble)
        if verbose:
            console.print(f'[{current_player:2}-{points[current_player]:6}]' + ''.join(f"[red]{node.value:3}[/red]" if node==insertion_pointer else f"{node.value:3}" for node in head), end="")
            input()
    return points

@solution_timer(2018,9,1)
def part_one(data: List[str], verbose=False):
    games = parse(data)
    for players, points in games:
        points = play_linked_list(players, points, verbose)
        #if verbose:
        #print(players, points, max(val for val in points.values()))
    return max(val for val in points.values())

@solution_timer(2018,9,2)
def part_two(data: List[str], verbose=False):
    games = parse(data)
    for players, points in games[0:1]:
        points = play_linked_list(players, points*100, verbose)
    return max(val for val in points.values())

if __name__ == "__main__":
    data = read_entire_input(2018,9)
    part_one(data)
    part_two(data)