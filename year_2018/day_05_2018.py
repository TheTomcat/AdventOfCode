from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2018,5)
test = """dabAcCaCBAcCcaDA""".split("\n")

def parse(data: List[str]) -> Any:
    return data[0]

def react(polymer:str, remove='', verbose=False):
    i=0
    if remove:
        polymer = ''.join(i for i in polymer if i.upper() != remove.upper())
    while i < len(polymer)-1:
        a, b = polymer[i], polymer[i+1]
        # if a.upper() == remove.upper():
        #     polymer = polymer[:i] + (polymer[i+1:] if i+1 <= len(polymer) else '')
        #     continue
        if a.upper() == b.upper():
            if (a.islower() or b.islower()) and not (a.islower() and b.islower()):
                if verbose:
                    print(f'reacting {a} and {b} at position {i}', end="->")
                    print(f'   {polymer[max(i-4,0):min(len(polymer),i+4)]}', end='->')
                polymer = polymer[:i] + (polymer[i+2:] if i+2 <= len(polymer) else '')
                if verbose:
                    print(f'   {polymer[max(i-3,0):min(len(polymer),i+3)]}')
                i -= 1
                if i < 0:
                    i=0
            else: 
                i += 1
        else:
            i+=1
    return polymer

@solution_timer(2018,5,1)
def part_one(data: List[str], verbose=False):
    polymer = parse(data)
    reacted_polymer = react(polymer, verbose=verbose)
    return len(reacted_polymer)

@solution_timer(2018,5,2)
def part_two(data: List[str], verbose=False):
    polymer = parse(data)
    log = dict()
    for element in 'abcdefghijklmnopqrstuvwxyz':
        if element not in polymer:
            continue
        if verbose:
            print(f'removing element {element}')
        reacted_polymer = react(polymer, remove=element, verbose=verbose)
        log[element] = len(reacted_polymer)
        if verbose:
            print()
    return min(log.values())

if __name__ == "__main__":
    data = read_entire_input(2018,5)
    part_one(data)
    part_two(data)