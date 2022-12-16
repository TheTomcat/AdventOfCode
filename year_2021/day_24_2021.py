from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from lib.iterators import grouper

data = read_entire_input(2021,24)

test1= """inp z
inp x
mul z 3
eql z x""".split('\n')

test2 = """inp w
add z w
mod z 2
div w 2
add y w
mod y 2
div w 2
add x w
mod x 2
div w 2
mod w 2""".split('\n')

COMMANDS = ["inp","add","mul","div","mod","eql"]
VARIABLES = ['w','x','y','z']

def parse(data: List[str]) -> Any:
    yield from [i.split(" ") for i in data]

class ALU:
    def __init__(self, instructions):
        self.instructions = instructions
        self.stack = {'w':0,'x':0,'y':0,'z':0}
    def getvar(self, var):
        if var in VARIABLES:
            return self.stack[var]
        return int(var)
    def run(self, input: List):
        for instr in self.instructions:
            match instr:
                case ["inp", variable]:
                    self.stack[variable] = int(input.pop(0))
                case [command, variable1, variable2]:
                    if command == "add":
                        c = self.getvar(variable1) + self.getvar(variable2)
                        self.stack[variable1] = c
                    elif command == "mul":
                        c = self.getvar(variable1) * self.getvar(variable2)
                        self.stack[variable1] = c
                    elif command == "div":
                        c = int(self.getvar(variable1) / self.getvar(variable2))
                        self.stack[variable1] = c
                    elif command == "mod":
                        c = self.getvar(variable1) % self.getvar(variable2)
                        self.stack[variable1] = c
                    elif command == "eql":
                        c = self.getvar(variable1) == self.getvar(variable2)
                        self.stack[variable1] = 1 if c else 0
        return self.stack['z']
    def __repr__(self):
        return f'ALU({self.stack})'                 
                    
class TranslateALU:
    def __init__(self, instructions, inp):
        self.raw_instructions = instructions
        self.stack = {'w':0,'x':0,'y':0,'z':0}
        self.pyth = []
        for instr in self.raw_instructions:
            match instr:
                case ["inp", var]:
                    self.pyth.append(f"{var}={inp.pop(0)}")
                case [command, var1, var2]:
                    if command == "add":
                        self.pyth.append(f"{var1}={var1}+{var2}")
                    elif command == "mul":
                        self.pyth.append(f"{var1}={var1}*{var2}")
                    elif command == "div":
                        self.pyth.append(f"{var1}=int({var1}/{var2})")
                    elif command == "mod":
                        self.pyth.append(f"{var1}={var1}%{var2}")
                    elif command == "eql":
                        self.pyth.append(f"{var1}=1 if {var1} == {var2} else 0")             

Z_divisor_offset = 4
X_addend_offset = 5
Y_addend_offset = 15
Instr_length = 18

def extract_values(instructions):
    As = []
    Bs = []
    Cs = []
    for block in grouper(Instr_length, instructions):
        As.append(int(block[Z_divisor_offset][-1]))
        Bs.append(int(block[X_addend_offset][-1]))
        Cs.append(int(block[Y_addend_offset][-1]))
    return As, Bs, Cs

@solution_timer(2021,24,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    alu = ALU(instructions)
    #alu.run([])
    return alu

@solution_timer(2021,24,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,24)
    part_one(data)
    part_two(data)