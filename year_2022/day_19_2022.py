from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

from dataclasses import dataclass
from math import ceil
import re

from lib.graph.priorityqueue import PriorityQueue

data = read_entire_input(2022,19)
test = """Blueprint 1: Each ore robot costs 4 ore. Each clay robot costs 2 ore. Each obsidian robot costs 3 ore and 14 clay. Each geode robot costs 2 ore and 7 obsidian.
Blueprint 2: Each ore robot costs 2 ore. Each clay robot costs 3 ore. Each obsidian robot costs 3 ore and 8 clay. Each geode robot costs 3 ore and 12 obsidian.""".split("\n")

def parse(data: List[str]) -> Any:
    pattern = r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.'
    matcher = re.compile(pattern)
    blueprints = {}
    for line in data:
        #index, ore_robot_ore_cost, clay_robot_ore_cost, obsidian_robot_ore_cost, obsidian_robot_clay_cost, geode_robot_ore_cost, geode_robot_obsidian_cost = 
        index, *blueprint = [int(i) for i in matcher.search(line).groups()]
        blueprints[index] = Blueprint(index, *blueprint)
    return blueprints

ORE = 0
CLAY = 1
OBSIDIAN = 2
GEODE =3 

@dataclass
class Blueprint:
    index: int
    ore_robot_ore_cost: int
    clay_robot_ore_cost: int
    obsidian_robot_ore_cost: int
    obsidian_robot_clay_cost: int
    geode_robot_ore_cost: int
    geode_robot_obsidian_cost: int
    def strategies(self, c_state: 'State', tmax):
        time_left = tmax - c_state.time_elapsed
        max_ore = ceil((max(self.ore_robot_ore_cost,
                            self.clay_robot_ore_cost, 
                            self.obsidian_robot_ore_cost,
                            self.geode_robot_ore_cost) * (time_left) - c_state.ore) / time_left)
        max_clay= ceil((self.obsidian_robot_clay_cost*time_left - c_state.clay) / time_left)
        max_obs = ceil((self.geode_robot_obsidian_cost*time_left - c_state.obsidian) / time_left)

        require = [c_state.ore_robots < max_ore,
                   c_state.clay_robots < max_clay,
                   c_state.obsidian_robots < max_obs]
        
        can_build = [
            c_state.ore >= self.ore_robot_ore_cost and require[ORE],
            c_state.ore >= self.clay_robot_ore_cost and require[CLAY] and require[OBSIDIAN],
            c_state.ore >= self.obsidian_robot_ore_cost and c_state.clay >= self.obsidian_robot_clay_cost and require[OBSIDIAN],
            c_state.ore >= self.geode_robot_ore_cost and c_state.obsidian >= self.geode_robot_obsidian_cost
        ]

        if can_build[GEODE]:
            


@dataclass
class State:
    time_elapsed: int
    ore: int
    clay: int
    obsidian: int
    geodes: int
    ore_robots: int
    clay_robots: int
    obsidian_robots: int
    geode_robots: int
    def produce(self, n=1):
        self.time_elapsed += n
        self.ore += self.ore_robots*n
        self.clay += self.clay_robots*n
        self.obsidian += self.obsidian_robots*n
        self.geodes += self.geode_robots*n
    def produce_all(self, tmax=24):
        self.produce(tmax - self.time_elapsed)
    def time_until_build(self, blueprint: Blueprint, robot):
        try:
            match robot:
                case 0:
                    return max(0, ceil((blueprint.ore_robot_ore_cost-self.ore)/self.ore_robots))
                case 1:
                    return max(0, ceil((blueprint.clay_robot_ore_cost-self.ore) / self.ore_robots))
                case 2:
                    return max(0, ceil((blueprint.obsidian_robot_clay_cost-self.clay)/self.clay_robots), ceil((blueprint.obsidian_robot_ore_cost-self.ore)/self.ore_robots))
                case 3:
                    return max(0, ceil((blueprint.geode_robot_obsidian_cost-self.obsidian)/self.obsidian_robots), ceil((blueprint.geode_robot_ore_cost-self.ore)/self.ore_robots))
        except ZeroDivisionError:
            return None
    def can_produce(self, blueprint: Blueprint) -> list:
        return [
            self.ore // blueprint.ore_robot_ore_cost,
            self.ore // blueprint.clay_robot_ore_cost,
            min(self.clay//blueprint.obsidian_robot_clay_cost, self.ore//blueprint.obsidian_robot_ore_cost),
            min(self.ore//blueprint.geode_robot_ore_cost, self.obsidian//blueprint.geode_robot_obsidian_cost)
        ]
    def build(self, blueprint: Blueprint, robot):
        match robot:
            case 0:
                if self.ore < blueprint.ore_robot_ore_cost:
                    raise ValueError(f"Not enough ore to build ore robot - {blueprint.ore_robot_ore_cost} required, {self.ore} in stock")
                self.ore -= blueprint.ore_robot_ore_cost
                self.ore_robots += 1
            case 1:
                if self.ore < blueprint.clay_robot_ore_cost:
                    raise ValueError(f"Not enough ore to build clay robot - {blueprint.clay_robot_ore_cost} required, {self.ore} in stock")
                self.ore -= blueprint.clay_robot_ore_cost 
                self.clay_robots += 1
            case 2: 
                if self.ore < blueprint.obsidian_robot_ore_cost or self.clay < blueprint.obsidian_robot_clay_cost:
                    raise ValueError(f"Not enough resources to build obsidian robot - ({blueprint.obsidian_robot_ore_cost}, {blueprint.obsidian_robot_clay_cost}) required, {self.ore}, {self.clay} in stock")
                self.ore -= blueprint.obsidian_robot_ore_cost 
                self.clay -= blueprint.obsidian_robot_clay_cost 
                self.obsidian_robots += 1
            case 3:
                if self.obsidian < blueprint.geode_robot_obsidian_cost or self.ore < blueprint.geode_robot_ore_cost:
                    raise ValueError(f"Not enough resources to build geode robot - ({blueprint.obsidian_robot_ore_cost}, {blueprint.geode_robot_obsidian_cost}) required, {self.ore}, {self.obsidian} in stock")
                self.obsidian -= blueprint.geode_robot_obsidian_cost 
                self.ore -= blueprint.geode_robot_ore_cost 
                self.geode_robots += 1

    def max_possible_geodes(self, tmax):
        "num current geodes + num geodes built by our current geode robots + num geodes if we built a geode robot on every turn till the end, even if we couldn't"
        return self.geodes + (tmax-self.time_elapsed)*self.geode_robots + triangle(tmax-self.time_elapsed)
    
    def quality(self, blueprint: Blueprint):
        return self.geodes * blueprint.index

class BuildPattern:
    def __init__(self, pattern: List):
        self.pattern = pattern
    def __iter__(self):
        yield from self.pattern
        # while True:
        #     yield 3
    def iterate(self, blueprint: Blueprint):
        for robot in [3,2,1,0]:
            for position in reversed(range(len(self.pattern)+1)):
                new_pat = BuildPattern(self.pattern[:position] + [robot] + self.pattern[position:])
                if new_pat.is_valid(blueprint):
                    yield new_pat
    def is_valid(self, blueprint:Blueprint) -> bool:
        if not (self.pattern.index(1) < self.pattern.index(2) < self.pattern.index(3)):
            return False
        if not self.pattern[-1] == 3:
            return False
        if len(self.pattern) > 23:
            return False
        if not all(self.pattern.count(robot) < blueprint.maximums()[robot] for robot in range(3)):
            return False
        return True
    def evaluate(self, blueprint: Blueprint, tmax) -> Tuple[State, int, int]:
        state = State(0,0,0,0,0,1,0,0,0)
        time_of_last_build = 0
        for index, next_robot in enumerate(self.pattern):
            if state.time_until_build(blueprint, next_robot) is None:
                state.produce_all()
                return state
            t = state.time_until_build(blueprint, next_robot)
            if state.time_elapsed + t >= tmax:
                index -= 1
                break
            # print(f"{t}s until I can build the next robot:", end="")
            state.produce(t+1) # Produce up until I can build the robot, and for the minute it takes to produce the robot
            # print(f"after that time I have {state}. ")
            state.build(blueprint, next_robot)
            time_of_last_build = state.time_elapsed

            # print(f"     - Building robot: {state}")
        state.produce_all()
        return state, time_of_last_build, index
    def prune(self, index_last_robot):
        if index_last_robot + 1 <= len(self):
            self.pattern = self.pattern[:index_last_robot+1]
    def __hash__(self):
        return hash(tuple(self.pattern))
    def __len__(self):
        return len(self.pattern)
    def __lt__(self, other):
        return tuple(self.pattern) < tuple(other.pattern)
    def __repr__(self):
        return f"BuildPattern({self.pattern})"

def triangle(i: int):
    return i*(i-1)/2

def A_star(start: BuildPattern, blueprint, tmax):
    queue = PriorityQueue[BuildPattern]()
    final_state, tlr, ilr = start.evaluate(blueprint, tmax)
    start.prune(ilr)
    queue.put(start, (final_state.geodes, len(start), tlr, ilr))
    visited_from = {start: {'parent':None,'value':final_state.geodes}}
    while not queue.is_empty():
        weights, build_pattern = queue.get_with_priority()
      

        for new_build_pattern in build_pattern.iterate(blueprint): # iterate_over_build_patterns(build_pattern, visited_from):
            final_state, tlr, ilr = new_build_pattern.evaluate(blueprint, tmax)
            new_build_pattern.prune(ilr)
            new_value = final_state.geodes
            print(f"Examining {new_build_pattern}... {final_state.geodes}")
            if new_build_pattern not in visited_from or new_value > visited_from[build_pattern]['value']:
                visited_from[new_build_pattern] = {'parent':build_pattern, 'value':new_value}
                
                queue.put(new_build_pattern, (new_value, len(new_build_pattern), tlr, ilr))
    return visited_from

# def search(start, blueprint):
#     queue: PriorityQueue[List]()
#     enqueue = queue.put
#     enqueue(start)
#     visited_from = {}#Dict[Node, Optional[Node]] = {}
#     visited_from[start] = {'geodes':0}
#     #print(f'Starting {"depth" if depth_first else "bredth"}-first search...')
#     while not queue.is_empty():
#         build_pattern = queue.get()
#         #print(current, end=" ")
#         for extended_build_pattern in iterate_over_build_patterns(build_pattern, visited_from):
#             if extended_build_pattern not in visited_from:
#                 geodes = visited_from[build_pattern]['geodes']
#                 cdepth = visited_from[build_pattern]['depth']
#                 enqueue(extended_build_pattern)
#                 visited_from[extended_build_pattern] = {'cost': cweight+weight, 'depth':cdepth+1}
#             if end(neighbour):
#                 #print(" - End condition satisfied, halting!")
#                 return visited_from, neighbour
#     return visited_from



# def valid_pattern(build_pattern: List):
#     if not (build_pattern.index(1) < build_pattern.index(2) < build_pattern.index(3)):
#         return False
#     if not build_pattern[-1] == 3:
#         return False
#     if len(build_pattern) > 23:
#         return False
#     return True

# def iterate_over_build_patterns(build_pattern: List, already_visited):
#     for robot in [3,2,1,0]:
#         for position in reversed(range(len(build_pattern)+1)):
#             new_pat = tuple(list(build_pattern[:position]) + [robot] + list(build_pattern[position:]))
#             if new_pat not in already_visited and valid_pattern(new_pat):
#                 yield tuple(new_pat)

@solution_timer(2022,19,1)
def part_one(data: List[str], verbose=False):
    blueprints = parse(data)
    state = [0,0,0,0,1,0,0,0]
    return False

@solution_timer(2022,19,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2022,19)
    part_one(data)
    part_two(data)