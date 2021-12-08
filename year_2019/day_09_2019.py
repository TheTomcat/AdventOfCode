from typing import List, Any, Tuple
from collections import defaultdict
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console

data = read_entire_input(2019,9)

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
ADJUSTOFFSET = 9
HALT = 99

POSITIONAL = '0'
IMMEDIATE = '1'
RELATIVE = '2'

class IntCode:
    def __init__(self, opcodes):
        self.opcodes = defaultdict(int)
        for i, val in enumerate(opcodes):
            self.opcodes[i] = val
        self.halted = False
        self.pointer = 0
        self.initialised = False
        self.relative_base = 0
    def get_arguments(self, read_modes, offset):
        value = self.opcodes[self.pointer+offset]
        read_mode = read_modes[offset-1]
        if read_mode == POSITIONAL: # i.e., positional
            return self.opcodes[value]
        elif read_mode == IMMEDIATE:
            return value
        elif read_mode == RELATIVE:
            return self.opcodes[self.relative_base + value]
        else:
            raise ValueError("Invalid Parameter Mode")
            
    def get_address(self, read_modes, offset):
        read_mode = read_modes[offset-1]
        value = self.opcodes[self.pointer + offset]
        if read_mode == POSITIONAL:
            return value
        elif read_mode == RELATIVE:
            return self.relative_base + value
        else:
            raise ValueError("Invalid Address Mode")

    def run(self, inputs: list):
        opcodes = self.opcodes
        diagnostic_code = 0
        while True:
            try:
                pointer = self.pointer
                opcode = opcodes[pointer]
                instruction = opcode % 100
                parameters = list(f"{opcode//100:03d}")[::-1]
                if instruction == ADD:
                    #console.print(f"INST {opcode:4} in mode {parameters} -> {self.get_arguments(parameters, 2)} + {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
                    opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) + self.get_arguments(parameters, 1)
                    self.pointer +=4
                elif instruction == MULTIPLY:
                    #console.print(f"INST {opcode:4} in mode {parameters} -> {self.get_arguments(parameters, 2)} * {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
                    opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) * self.get_arguments(parameters, 1)
                    self.pointer += 4
                elif instruction == INPUT:
                    val = inputs.pop()
                    #console.print(f"INST {opcode:4} in mode {parameters} -> Val {val} to {self.get_arguments(parameters, 1)}")
                    opcodes[self.get_address(parameters, 1)] = val
                    self.pointer +=2
                elif instruction == OUTPUT:
                    diagnostic_code = opcodes[self.get_address(parameters, 1)]
                    #console.print(f"INST {opcode:4} in mode {parameters} -> Code {diagnostic_code} from {self.get_address(parameters, 1)}")
                    self.pointer +=2
                    self.signal = diagnostic_code
                    return diagnostic_code
                elif instruction == JUMPIFTRUE:
                    self.pointer = self.get_arguments(parameters,2) if self.get_arguments(parameters,1) else pointer + 3
                elif instruction == JUMPIFFALSE:
                    self.pointer = self.get_arguments(parameters,2) if not self.get_arguments(parameters,1) else pointer + 3
                elif instruction == LESSTHAN:
                    opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) < self.get_arguments(parameters,2) else 0
                    self.pointer += 4
                elif instruction == EQUALS:
                    opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) == self.get_arguments(parameters,2) else 0
                    self.pointer += 4
                elif instruction == ADJUSTOFFSET:
                    self.relative_base += self.get_arguments(parameters,1)
                    self.pointer += 2
                elif instruction == HALT:
                    self.halted = True
                    return diagnostic_code
                else:
                    raise ValueError(f"{instruction}:{opcode} is an invalid opcode")
            except Exception as e:
                print(f"{opcode}: {parameters=}, {opcodes[pointer],opcodes[pointer+1],opcodes[pointer+2],opcodes[pointer+3]}")
                raise e
@solution_timer(2019,9,1)
def part_one(data: List[str]):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([1])

@solution_timer(2019,9,2)
def part_two(data: List[str]):
    instr = parse(data)
    computer = IntCode(instr)
    return computer.run([2])

    return False

if __name__ == "__main__":
    data = read_entire_input(2019,9)
    part_one(data)
    part_two(data)