from typing import List, Any
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2019,2)
test=["1,9,10,3,2,3,11,0,99,30,40,50"]

def parse(data: List[str]) -> List[int]:
    return [int(i) for i in data[0].split(',')]

def run(opcodes):
    pointer = 0
    # i=0
    while True:
        # i=i+1
        opcode, arg1, arg2, destination = opcodes[pointer:pointer+4]
        if opcode == 1:
            opcodes[destination] = opcodes[arg1] + opcodes[arg2]
        elif opcode == 2:
            opcodes[destination] = opcodes[arg1] * opcodes[arg2]
        elif opcode == 99:
            # print(i)
            return opcodes
        else:
            raise ValueError(f"{opcode} is an invalid opcode")
        pointer += 4

@solution_timer(2019,2,1)
def part_one(data: List[str], verbose=False):
    opcodes = parse(data)
    opcodes[1] = 12
    opcodes[2] = 2
    return run(opcodes)[0]

@solution_timer(2019,2,2)
def part_two(data: List[str], verbose=False):
    opcodes = parse(data)
    for noun in range(0,99):
        for verb in range(0,99):
            opcodes = parse(data)
            opcodes[1] = noun
            opcodes[2] = verb
            opcodes = run(opcodes)
            if opcodes[0] == 19690720:
                return 100*noun + verb

if __name__ == "__main__":
    data = read_entire_input(2019,2)
    part_one(data)
    part_two(data)