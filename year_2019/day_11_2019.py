from collections import defaultdict
from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,11)

# def parse(data: List[str]) -> List[int]:
#     return [int(i) for i in data[0].split(',')]

# ADD = 1
# MULTIPLY = 2
# INPUT = 3
# OUTPUT = 4
# JUMPIFTRUE = 5
# JUMPIFFALSE = 6
# LESSTHAN = 7
# EQUALS = 8
# ADJUSTOFFSET = 9
# HALT = 99

# POSITIONAL = '0'
# IMMEDIATE = '1'
# RELATIVE = '2'

# class IntCode:
#     def __init__(self, opcodes, debug=False):
#         self.debug = debug
#         self.opcodes = defaultdict(int)
#         for i, val in enumerate(opcodes):
#             self.opcodes[i] = val
#         self.halted = False
#         self.pointer = 0
#         self.initialised = False
#         self.relative_base = 0
#     def print(self, message):
#         if self.debug:
#             console.print(message)
#     def get_arguments(self, read_modes, offset):
#         value = self.opcodes[self.pointer+offset]
#         read_mode = read_modes[offset-1]
#         if read_mode == POSITIONAL: # i.e., positional
#             return self.opcodes[value]
#         elif read_mode == IMMEDIATE:
#             return value
#         elif read_mode == RELATIVE:
#             return self.opcodes[self.relative_base + value]
#         else:
#             raise ValueError("Invalid Parameter Mode")
            
#     def get_address(self, read_modes, offset):
#         read_mode = read_modes[offset-1]
#         value = self.opcodes[self.pointer + offset]
#         if read_mode == POSITIONAL:
#             return value
#         elif read_mode == RELATIVE:
#             return self.relative_base + value
#         else:
#             raise ValueError("Invalid Address Mode")

#     def run(self, inputs: list):
#         opcodes = self.opcodes
#         diagnostic_code = 0
#         while True:
#             try:
#                 pointer = self.pointer
#                 opcode = opcodes[pointer]
#                 instruction = opcode % 100
#                 parameters = list(f"{opcode//100:03d}")[::-1]
#                 if instruction == ADD:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-ADD in mode {parameters} -> {self.get_arguments(parameters, 2)} + {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
#                     opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) + self.get_arguments(parameters, 1)
#                     self.pointer +=4
#                 elif instruction == MULTIPLY:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-MUL in mode {parameters} -> {self.get_arguments(parameters, 2)} * {self.get_arguments(parameters, 1)} to {self.get_address(parameters,3)}")
#                     opcodes[self.get_address(parameters,3)] = self.get_arguments(parameters, 2) * self.get_arguments(parameters, 1)
#                     self.pointer += 4
#                 elif instruction == INPUT:
#                     val = inputs.pop()
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-INP in mode {parameters} -> Val {val} to {self.get_arguments(parameters, 1)}")
#                     opcodes[self.get_address(parameters, 1)] = val
#                     self.pointer +=2
#                 elif instruction == OUTPUT:
#                     diagnostic_code = self.get_arguments(parameters, 1)
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-OUT in mode {parameters} -> Code {diagnostic_code}")
#                     self.pointer +=2
#                     return diagnostic_code
#                 elif instruction == JUMPIFTRUE:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-JMT in mode {parameters} -> Jumptrue based on {self.get_arguments(parameters,1)}")
#                     self.pointer = self.get_arguments(parameters,2) if self.get_arguments(parameters,1) else pointer + 3
#                 elif instruction == JUMPIFFALSE:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-JMF in mode {parameters} -> Jumpfalse based on {self.get_arguments(parameters,1)}")
#                     self.pointer = self.get_arguments(parameters,2) if not self.get_arguments(parameters,1) else pointer + 3
#                 elif instruction == LESSTHAN:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-LES in mode {parameters} -> {self.get_arguments(parameters,1)}<{self.get_arguments(parameters,2)}")
#                     opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) < self.get_arguments(parameters,2) else 0
#                     self.pointer += 4
#                 elif instruction == EQUALS:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-EQU in mode {parameters} -> {self.get_arguments(parameters,1)}={self.get_arguments(parameters,2)}")
#                     opcodes[self.get_address(parameters,3)] = 1 if self.get_arguments(parameters,1) == self.get_arguments(parameters,2) else 0
#                     self.pointer += 4
#                 elif instruction == ADJUSTOFFSET:
#                     self.print(f"INST {opcode:4}@{self.pointer:3}-OFF in mode {parameters} -> offset += {self.get_arguments(parameters,1)} = {self.relative_base}")
#                     self.relative_base += self.get_arguments(parameters,1)
#                     self.pointer += 2
#                 elif instruction == HALT:
#                     self.halted = True
#                     return diagnostic_code
#                 else:
#                     raise ValueError(f"{instruction}:{opcode} is an invalid opcode")
#             except Exception as e:
#                 print(f"{opcode}: {parameters=}, {opcodes[pointer],opcodes[pointer+1],opcodes[pointer+2],opcodes[pointer+3]}")
#                 raise e

def run_robot(data:List[str], init=0):
    debug = False
    robot = IntCode(data, debug=debug)
    is_white = defaultdict(lambda: 0)
    is_white[(0,0)] = init
    position = (0,0)
    direction = (0,1)

    while not robot.halted:
        colour = robot.run([is_white[position]])
        turn = robot.run([])
        if debug:
            console.print(f"ROBO pos{position}-dir{direction} -> current colour: {is_white[position]} -> {colour}. Turning {turn}")
        is_white[position] = colour
        if turn == 0: # Turn left
            direction = -direction[1], direction[0]
        elif turn == 1:
            direction = direction[1], -direction[0]
        position = position[0] + direction[0], position[1] + direction[1]
        if debug:
            console.print(f"MOVE pos{position}-dir{direction} -> current colour: {is_white[position]}")
    return is_white

@solution_timer(2019,11,1)
def part_one(data: List[str]):
    instructions = parse(data)
    is_white = run_robot(instructions)
    return len(is_white)

@solution_timer(2019,11,2)
def part_two(data: List[str]):
    instructions = parse(data)
    is_white = run_robot(instructions, 1)
    xmin = min(i[0] for i in is_white.keys())
    xmax = max(i[0] for i in is_white.keys())
    ymin = min(i[1] for i in is_white.keys())
    ymax = max(i[1] for i in is_white.keys())
    image = '\n'.join(''.join(chr(9608) if is_white[(i,j)] else ' ' for i in range(xmin, xmax+1)) for j in range(ymax, ymin-1, -1))
    return '\n'+image

if __name__ == "__main__":
    data = read_entire_input(2019,11)
    part_one(data)
    part_two(data)