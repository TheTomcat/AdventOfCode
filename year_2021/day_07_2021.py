from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,7)

def parse(data: List[str]) -> Any:
    return [int(i) for i in data[0].split(',')]

def calculate_crab_fuel_linear(crabs, final_position):
    fuel = 0
    for crab in crabs:
        fuel += abs(crab-final_position)
    return fuel

def calculate_crab_fuel_quadratic(crabs, final_position):
    fuel = 0
    for crab in crabs:
        d = abs(crab-final_position)
        fuel += d*(d+1)/2
    return fuel
    

@solution_timer(2021,7,1)
def part_one(data: List[str], verbose=False):
    crabs = parse(data)
    fuel = []
    for position in range(min(crabs), max(crabs)):
        fuel.append(calculate_crab_fuel_linear(crabs, position))
    return min(fuel)

@solution_timer(2021,7,2)
def part_two(data: List[str], verbose=False):
    crabs = parse(data)
    # Actually the minimum for this will be the average (minimising the squared distance)
    guess = calculate_crab_fuel_quadratic(crabs, int(sum(crabs)/len(crabs)))
    # For completion, check all of them
    fuel = []
    for position in range(min(crabs), max(crabs)):
        fuel.append(calculate_crab_fuel_quadratic(crabs, position))
    
    return min(fuel)

if __name__ == "__main__":
    data = read_entire_input(2021,7)
    part_one(data)
    part_two(data)