from typing import List
from collections import defaultdict, deque 
from framework.console import console

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
    def __init__(self, opcodes, debug=False):
        self.debug = debug
        self.opcodes = defaultdict(int)
        for i, val in enumerate(opcodes):
            self.opcodes[i] = val
        self.halted = False
        self.pointer = 0
        self.relative_base = 0
    def print(self, message):
        if self.debug:
            console.print(message)

    def provide_inputs(self, inputs):
        self.inputs = [i for i in inputs]

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

    def run(self, inputs: list=None):
        opcodes = self.opcodes
        diagnostic_code = 0
        while True:
            try:
                pointer = self.pointer
                opcode = opcodes[pointer]
                instruction = opcode % 100
                parameters = list(f"{opcode//100:03d}")[::-1]
                if instruction == ADD:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-ADD in mode {parameters} -> {self.get_arguments(parameters, 2)} + {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
                    opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) + self.get_arguments(parameters, 1)
                    self.pointer +=4
                elif instruction == MULTIPLY:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-MUL in mode {parameters} -> {self.get_arguments(parameters, 2)} * {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
                    opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) * self.get_arguments(parameters, 1)
                    self.pointer += 4
                elif instruction == INPUT:
                    val = self.inputs.pop()
                    self.print(f"INST {opcode:4}@{self.pointer:3}-INP in mode {parameters} -> Val {val} to {self.get_arguments(parameters, 1)}")
                    opcodes[self.get_address(parameters, 1)] = val
                    self.pointer +=2
                elif instruction == OUTPUT:
                    diagnostic_code = self.get_arguments(parameters, 1)
                    self.print(f"INST {opcode:4}@{self.pointer:3}-OUT in mode {parameters} -> Code {diagnostic_code}")
                    self.pointer +=2
                    return diagnostic_code
                elif instruction == JUMPIFTRUE:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-JMT in mode {parameters} -> Jumptrue based on {self.get_arguments(parameters,1)}")
                    self.pointer = self.get_arguments(parameters,2) if self.get_arguments(parameters,1) else pointer + 3
                elif instruction == JUMPIFFALSE:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-JMF in mode {parameters} -> Jumpfalse based on {self.get_arguments(parameters,1)}")
                    self.pointer = self.get_arguments(parameters,2) if not self.get_arguments(parameters,1) else pointer + 3
                elif instruction == LESSTHAN:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-LES in mode {parameters} -> {self.get_arguments(parameters,1)}<{self.get_arguments(parameters,2)}")
                    opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) < self.get_arguments(parameters,2) else 0
                    self.pointer += 4
                elif instruction == EQUALS:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-EQU in mode {parameters} -> {self.get_arguments(parameters,1)}={self.get_arguments(parameters,2)}")
                    opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) == self.get_arguments(parameters,2) else 0
                    self.pointer += 4
                elif instruction == ADJUSTOFFSET:
                    self.print(f"INST {opcode:4}@{self.pointer:3}-OFF in mode {parameters} -> offset += {self.get_arguments(parameters,1)} = {self.relative_base}")
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