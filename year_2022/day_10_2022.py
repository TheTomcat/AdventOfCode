from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2022,10)

def parse(data: List[str]) -> Any:
    instructions = []
    for instruction in data:
        if instruction.startswith("addx"):
            command, value = instruction.split(" ")
            value = int(value)
            instructions.append((command, value))
        else:
            instructions.append((instruction,0))
    return instructions

class CPU:
    def __init__(self, x=1, cycles=0, breakpoints = None):
        self.x = x
        self.cycles = cycles
        self.breakpoints = [i for i in breakpoints] if breakpoints is not None else []
        self.returns = {}
    def process(self, instruction):
        command, value = instruction
        if instruction[0] == 'addx':
            self.check()
            self.cycles += 1
            self.check()
            self.cycles += 1
            self.x += value            
        else:
            self.check()
            self.cycles += 1
            
    def check(self):
        if self.cycles in self.breakpoints:
            self.returns[self.cycles] = self.x       
    def sig_strengths(self):
        tot = 0
        for cyc, val in self.returns.items():
            tot += cyc*val
        return tot

class CRT(CPU):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.display = []
    def check(self):
        if self.x-1 <= self.cycles % 40 <= self.x+1:
            self.display += chr(9608)
        else:
            self.display += ' '
    def print(self):
        return '\n'+'\n'.join(''.join(self.display[i+row*40] for i in range(40)) for row in range(6))
    

@solution_timer(2022,10,1)
def part_one(data: List[str]):
    instructions = parse(data)
    c = CPU(x=1, breakpoints=[20,60,100,140,180,220])
    for instruction in instructions:
        c.process(instruction)
    return c.sig_strengths()

@solution_timer(2022,10,2)
def part_two(data: List[str]):
    instructions = parse(data)
    c = CRT(x=1)
    for instruction in instructions:
        c.process(instruction)
    return c.print()

if __name__ == "__main__":
    data = read_entire_input(2022,10)
    part_one(data)
    part_two(data)


test = """addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop""".split("\n")