from typing import List, Any, Tuple
import operator as op
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from framework.console import log

log.setLevel("ERROR")

data = read_entire_input(2019,5)
test = ["1002,4,3,4,33"]

tests = [
    ("3,9,8,9,10,9,4,9,99,-1,8",[8],1), # position mode, test == 8 -> True
    ("3,9,8,9,10,9,4,9,99,-1,8",[5],0), # position mode, test == 8 -> False
    ("3,9,7,9,10,9,4,9,99,-1,8",[5],1), # position mode, test < 8 -> True
    ("3,9,7,9,10,9,4,9,99,-1,8",[9],0), # position mode, test < 8 -> False
    ("3,3,1108,-1,8,3,4,3,99",[8],1), # immediate mode, test == 8
    ("3,3,1108,-1,8,3,4,3,99",[5],0),
    ("3,3,1107,-1,8,3,4,3,99",[5],1),
    ("3,3,1107,-1,8,3,4,3,99",[9],0),
]

def run_test(tests):
    output = []
    for test_input, inputs, expected_output in tests:
        output.append(run(parse([test_input]), inputs), expected_output)
    return output

def parse(data: List[str]) -> List[int]:
    return [int(i) for i in data[0].split(',')]

ADD = 1
MULTIPLY = 2
INPUT = 3
OUTPUT = 4
JUMPIFTRUE = 5
JUMPIFFALSE = 6
LESSTHAN = 7
EQUALS = 8
HALT = 99

def position(parameters, i):
    return len(parameters) <= i or parameters[i] == 0

def immediate(parameters, i):
    return i >= len(parameters) or parameters[i]

def param(opcode):
    return opcode // 100 % 10, opcode // 1000 % 10

def run(opcodes, inputs):
    pointer = 0
    diagnostic_code = 0
    while True:
        opcode = opcodes[pointer]
        instruction = opcode % 100
        parameters = param(opcode) #[opcode // 10** i % 10 for i in range(2,len(str(opcode)))]
        if instruction in [1,2,5,6,7,8]:
            arguments = [opcodes[pointer+i+1] if parameters[i] else opcodes[opcodes[pointer+i+1]] for i in range(2)] 
        if instruction == ADD:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> ADD")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            opcodes[opcodes[pointer+3]] = arguments[1] + arguments[0]
            log.debug(f"[green]    Storing {opcodes[opcodes[pointer+3]]} at {opcodes[pointer+3]}")
            pointer +=4
        elif instruction == MULTIPLY:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> MULTIPLY")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            opcodes[opcodes[pointer+3]] = arguments[1] * arguments[0]
            log.debug(f"[green]    Storing {opcodes[opcodes[pointer+3]]} at {opcodes[pointer+3]}")
            pointer += 4
        elif instruction == INPUT:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> INPUT")
            opcodes[opcodes[pointer+1]] = inputs.pop(0)
            log.debug(f"[green]    Storing {opcodes[opcodes[pointer+1]]} at {opcodes[pointer+1]}")
            pointer +=2
        elif instruction == OUTPUT:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> OUTPUT")
            diagnostic_code = opcodes[opcodes[pointer+1]]
            log.debug(f"[green]    Getting {opcodes[opcodes[pointer+1]]} from {opcodes[pointer+3]}")
            pointer +=2
        elif instruction == JUMPIFTRUE:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> JUMPIFTRUE")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            pointer = arguments[1] if arguments[0] else pointer + 3
            log.debug(f"[green]    Checking: {arguments[0]}==1 so jumping to {pointer}")
        elif instruction == JUMPIFFALSE:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> JUMPIFFALSE")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            pointer = arguments[1] if not arguments[0] else pointer + 3
            log.debug(f"[green]    Checking: {arguments[0]}==0 so jumping to {pointer}")
        elif instruction == LESSTHAN:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> LESSTHAN")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            opcodes[opcodes[pointer+3]] = 1 if arguments[0] < arguments[1] else 0
            log.debug(f"[green]    Checking: {arguments[0]}<{arguments[1]} ({arguments[0] < arguments[1]}) so storing {opcodes[opcodes[pointer+3]]} in {opcodes[pointer+3]}")
            pointer += 4
        elif instruction == EQUALS:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> EQUALS")
            log.debug(f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
            log.debug(f"[yellow]    Arguments: {arguments}")
            opcodes[opcodes[pointer+3]] = 1 if arguments[0] == arguments[1] else 0
            log.debug(f"[green]    Checking: {arguments[0]}=={arguments[1]} ({arguments[0] == arguments[1]}) so storing {opcodes[opcodes[pointer+3]]} in {opcodes[pointer+3]}")
            pointer += 4
        elif instruction == HALT:
            log.debug(f"[red]INSTRUCTION {opcodes[pointer]} -> HALT")
            return diagnostic_code
        else:
            raise ValueError(f"{instruction}:{opcode} is an invalid opcode")

@solution_timer(2019,5,1)
def part_one(data: List[str], verbose=False):
    opcodes = parse(data)
    return run(opcodes, [1])

@solution_timer(2019,5,2)
def part_two(data: List[str], verbose=False):
    opcodes = parse(data)
    return run(opcodes, [5])

if __name__ == "__main__":
    data = read_entire_input(2019,5)
    part_one(data)
    part_two(data)