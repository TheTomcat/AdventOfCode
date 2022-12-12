from collections import defaultdict, deque
from itertools import product
from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,15)

COMMANDS = {1: (0,1), 2: (0,-1), 3: (-1,0), 4: (1,0)}
DIRECTIONS = {1:3, 3:2, 2:4, 4:1}
BACKTRACK = {1:2, 2:1, 3:4, 4:3}
class Robot:
    def __init__(self, instructions, debug=False):
        self.debug = debug
        self.computer = IntCode(instructions)
        self.position = (0,0)
        self.map = {(0,0):1}
        self.visited = set([(0,0)])
        self.memory = []
        self.distances = {(0,0):0}
    def print(self, message, end=None):
        if self.debug:
            if end is None:
                console.print(message)
            else:
                console.print(message, end=end)
    def step(self, direction, backtrack = False):
        x,y = self.position
        i = self.computer.run([direction])
        dx, dy = COMMANDS[direction]
        self.map[(x+dx, y+dy)] = i
        self.visited.add((x+dx, y+dy)) 
        if i == 1 or i == 2: # We can step there
            #console.print("[green] - We can step here.")
            self.position = x+dx, y+dy # Step there
            if not backtrack:
                self.distances[(x+dx, y+dy)] = self.distances[(x,y)]+1
                self.memory.append(direction) # Remeber how we got here
        else:
            pass
        return i
    def backtrack(self, steps=1):
        for _ in range(steps):
            direction = BACKTRACK[self.memory.pop()]
            i = self.step(direction, backtrack=True)
            if i == 0:
                raise ValueError("Something went wrong, we hit a wall and shouldn't have.")
    def explore(self):
        forks = deque()
        while True:
            options = []
            x,y = self.position
            for direction, (dx, dy) in COMMANDS.items():
                self.print(f"[yellow]From {self.position} looking {direction} to {(x+dx, y+dy)}", end="")
                if self.has_explored((x+dx, y+dy)):
                    self.print(f"[red] - Already visited")
                    continue
                i = self.step(direction)
                if i == 0:
                    self.print(f"[red] - Wall")
                else:
                    self.print(f"[green] - We can step here")
                    options.append((direction, dx, dy))
                    self.backtrack()
            if len(options) == 0:
                try:
                    dest, direction = forks.pop()
                except IndexError as e:
                    return 
                self.print(f"[red] Dead end, backtracking to get to {dest}.")
                while self.position != dest: 
                    self.backtrack()
                    self.print(f"{self.position} ", end="")
                self.print(f"\n[green]Now back at {self.position} and stepping {direction}")
                self.step(direction)
            elif len(options) == 1:
                self.step(options[0][0])
            elif len(options) == 2:
                self.print(f"[green] FORK in the road - {self.position} - {options} -", end="")
                actual_direction = options[0][0]
                for direction, dx, dy in options[1:]:
                    forks.append((self.position, direction))
                self.step(actual_direction)
                self.print(f"[yellow] going {actual_direction}")
            else:
                raise ValueError(f"Should not have this many options: {self.position}, {options}")
    def has_explored(self, position):
        return position in self.map
    def show_map(self):
        tile = {0: chr(9608), 1: " ", '.':'.', 2:"#"}
        xmin = min(i[0] for i in self.map.keys())
        xmax = max(i[0] for i in self.map.keys())
        ymin = min(i[1] for i in self.map.keys())
        ymax = max(i[1] for i in self.map.keys())
        image = '\n'.join(''.join(tile[self.map.get((i,j), ".")] for i in range(xmin, xmax+1)) for j in range(ymax, ymin-1, -1))
        return image

def neighbours(position):
    yield position[0]+1, position[1]
    yield position[0]-1, position[1]
    yield position[0], position[1]+1
    yield position[0], position[1]-1

def longest_line(map, start):
    distances = {}
    distances[start] = 0 # i.e., explored
    frontier = deque()
    frontier.append(start)
    while frontier:
        position = frontier.popleft()
        for neighbour in neighbours(position):
            if map.get(neighbour, 0) != 0 and neighbour not in distances:
                distances[neighbour] = distances[position] + 1
                frontier.append(neighbour)
    return distances

@solution_timer(2019,15,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    robot = Robot(instructions)
    robot.explore()
    return robot.distances[[i for i,v in robot.map.items() if v == 2][0]]

@solution_timer(2019,15,2)
def part_two(data: List[str], verbose=False):
    instructions = parse(data)
    robot = Robot(instructions)
    robot.explore()
    oxygen = [i for i,v in robot.map.items() if v == 2][0]
    distances = longest_line(robot.map, oxygen)
    return max(i for i in distances.values())

if __name__ == "__main__":
    data = read_entire_input(2019,15)
    part_one(data)
    part_two(data)