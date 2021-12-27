from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

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
                    

@solution_timer(2021,24,1)
def part_one(data: List[str]):
    instructions = parse(data)
    alu = ALU(instructions)
    alu.run([])
    return alu

@solution_timer(2021,24,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,24)
    part_one(data)
    part_two(data)