from typing import List, Any
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2019,1)

def parse(data: List[str]) -> List[int]:
    return [int(i) for i in data]

def calculate_fuel(mass):
    return max(int(mass/3)-2,0)

def recursive_calculate_fuel(mass):
    total_fuel = 0
    fuel=1
    while fuel > 0:
        fuel = calculate_fuel(mass)
        total_fuel += fuel
        mass=fuel
    return total_fuel
    
@solution_timer(2019,1,1)
def part_one(data: List[str], verbose=False):
    weights = parse(data)
    fuel = [calculate_fuel(weight) for weight in weights]
    return sum(fuel)

@solution_timer(2019,1,2)
def part_two(data: List[str], verbose=False):
    weights = parse(data)
    fuel = [recursive_calculate_fuel(weight) for weight in weights]
    return sum(fuel)

if __name__ == "__main__":
    data = read_entire_input(2019,1)
    part_one(data)
    part_two(data)