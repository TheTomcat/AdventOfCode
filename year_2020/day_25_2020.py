from typing import List, Any
import math
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,25)
test = """5764801
17807724""".split("\n")

PRIME = 20201227

def parse(data: List[str]) -> Any:
    return [int(i) for i in data]

def brute_force_get_encryption_key(pubkey1, pubkey2, modulus=PRIME):
    loop1 = 1
    while pow(7,loop1,modulus) != pubkey1:
        loop1+= 1
    loop2 = 1
    while pow(7, loop2, modulus) != pubkey2:
        loop2+=1
    return pow(pubkey1, loop2, modulus)

def baby_step_giant_step(subject_number, pubkey, modulus=PRIME):
    m = int(math.sqrt(modulus))+1
    index = {}
    for j in range(m):
        k = pow(subject_number,j,modulus)
        if k in index:
            raise IndexError(f"the value {k} (j={j}) is already in the table")
        index[k] = j
    reducer = pow(subject_number, -m, modulus)
    gamma = pubkey
    for i in range(m):
        if gamma in index:
            return (i*m+index[gamma]) % modulus
        else:
            gamma = (gamma * reducer) % modulus
    raise ValueError("No solution found")

@solution_timer(2020,25,1)
def part_one(data: List[str]):
    card_public_key, door_public_key = parse(data)
    card_loop_size = baby_step_giant_step(7, card_public_key)
    return pow(door_public_key, card_loop_size, PRIME)
    #return brute_force_get_encryption_key(card_public_key, door_public_key)

@solution_timer(2020,25,2)
def part_two(data: List[str]):
    _ = parse(data)

    return True

if __name__ == "__main__":
    data = read_entire_input(2020,25)
    part_one(data)
    part_two(data)

    # 2020 day 25 part 01: 9620012 in 37221.45 ms