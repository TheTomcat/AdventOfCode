from typing import List, Any, Tuple
from itertools import permutations
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from framework.console import log

log.setLevel("INFO")

data = read_entire_input(2019,7)

test = ["""3,52,1001,52,-5,52,3,53,1,52,56,54,1007,54,5,55,1005,55,26,1001,54,
-5,54,1105,1,12,1,53,54,53,1008,54,0,55,1001,55,1,55,2,53,55,53,4,
53,1001,56,-1,56,1005,56,6,99,0,0,0,0,10""".replace("\n","")]

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

class IntCode:
    def __init__(self, data, input_, verbosity=0):
        self.opcodes = parse(data)
        self.halted = False
        # self.verbosity = verbosity
        self.input = input_
        self.pointer = 0
        self.initialised = False
    # def print(self, level, msg):
    #     if level <= self.verbosity:
    #         if level == 1:
    #             log.info(msg)
    #         elif level ==2:
    #             log.debug(msg)
    #         else:
    #             log.warn(msg)
    def get_arguments(self, read_mode, value):
        if read_mode == '0': # i.e., positional
            try:
                return self.opcodes[value]
            except Exception as e:
                print(value)
                raise e
        else:
            return value
    def run(self, signal):
        opcodes = self.opcodes
        diagnostic_code = 0
        while True:
            pointer = self.pointer
            opcode = opcodes[pointer]
            instruction = opcode % 100
            parameters = list(f"{opcode//100:03d}")[::-1]
            if instruction in [1,2,5,6,7,8]:
                try:
                    arguments = [self.get_arguments(parameters[i],opcodes[pointer+i+1]) for i in range(2)] 
                except Exception as e:
                    print(f"{parameters=}, {opcodes[pointer:pointer+4]}")
                    raise e
            if instruction == ADD:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> ADD")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                opcodes[opcodes[pointer+3]] = arguments[1] + arguments[0]
                # self.print(2,f"[green]    Storing {opcodes[opcodes[pointer+3]]} at {opcodes[pointer+3]}")
                self.pointer +=4
            elif instruction == MULTIPLY:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> MULTIPLY")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                opcodes[opcodes[pointer+3]] = arguments[1] * arguments[0]
                # self.print(2,f"[green]    Storing {opcodes[opcodes[pointer+3]]} at {opcodes[pointer+3]}")
                self.pointer += 4
            elif instruction == INPUT:
                val = signal if self.initialised else self.input 
                self.initialised = True
                opcodes[opcodes[pointer+1]] = val
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> INPUT ({opcodes[opcodes[pointer+1]]})")
                # self.print(2,f"[green]    Storing {opcodes[opcodes[pointer+1]]} at {opcodes[pointer+1]}")
                self.pointer +=2
            elif instruction == OUTPUT:
                diagnostic_code = opcodes[opcodes[pointer+1]]
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> OUTPUT ({opcodes[opcodes[pointer+1]]})")
                # self.print(2,f"[green]    Getting {opcodes[opcodes[pointer+1]]} from {opcodes[pointer+3]}")
                self.pointer +=2
                self.signal = diagnostic_code
                return self.signal
            elif instruction == JUMPIFTRUE:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> JUMPIFTRUE")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                self.pointer = arguments[1] if arguments[0] else pointer + 3
                # self.print(2,f"[green]    Checking: {arguments[0]}==1 so jumping to {pointer}")
            elif instruction == JUMPIFFALSE:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> JUMPIFFALSE")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                self.pointer = arguments[1] if not arguments[0] else pointer + 3
                # self.print(2,f"[green]    Checking: {arguments[0]}==0 so jumping to {pointer}")
            elif instruction == LESSTHAN:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> LESSTHAN")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                opcodes[opcodes[pointer+3]] = 1 if arguments[0] < arguments[1] else 0
                # self.print(2,f"[green]    Checking: {arguments[0]}<{arguments[1]} ({arguments[0] < arguments[1]}) so storing {opcodes[opcodes[pointer+3]]} in {opcodes[pointer+3]}")
                self.pointer += 4
            elif instruction == EQUALS:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> EQUALS")
                # self.print(2,f"[yellow]    Mode: {parameters} -> opcodes {opcodes[pointer+1:pointer+4]}")
                # self.print(2,f"[yellow]    Arguments: {arguments}")
                opcodes[opcodes[pointer+3]] = 1 if arguments[0] == arguments[1] else 0
                # self.print(2,f"[green]    Checking: {arguments[0]}=={arguments[1]} ({arguments[0] == arguments[1]}) so storing {opcodes[opcodes[pointer+3]]} in {opcodes[pointer+3]}")
                self.pointer += 4
            elif instruction == HALT:
                # self.print(1,f"[red]INSTRUCTION {pointer:4}:{opcodes[pointer]} -> HALT")
                self.halted = True
                self.signal = diagnostic_code
                return None
            else:
                raise ValueError(f"{instruction}:{opcode} is an invalid opcode")

def run_amplifier(data, phase_settings):
    signal = 0
    for phase_setting in phase_settings:
        computer = IntCode(data, phase_setting)
        signal = computer.run(signal)
    return signal

def run_feedback_amplifier(data, phase_settings):
    signal = 0
    computers = [IntCode(data, phase_setting) for phase_setting in phase_settings]
    lv = None
    while not any(c.halted for c in computers):
        for computer in computers:
            signal = computer.run(signal)
            # print(signal)
            if signal is not None:
                lv = signal
    return lv

# run_amplifier(["3,15,3,16,1002,16,10,16,1,16,15,15,4,15,99,0,0"],[4,3,2,1,0]) -> 43210
# run_amplifier(["3,23,3,24,1002,24,10,24,1002,23,-1,23,101,5,23,23,1,24,23,23,4,23,99,0,0"],[0,1,2,3,4]) -> 54321
# run_amplifier(["3,31,3,32,1002,32,10,32,1001,31,-2,31,1007,31,0,33,1002,33,7,33,1,33,31,31,1,32,31,31,4,31,99,0,0,0"],[1,0,4,2,3]) -> 65210
# run_feedback_amplifier(["3,26,1001,26,-4,26,3,27,1002,27,2,27,1,27,26,27,4,27,1001,28,-1,28,1005,28,6,99,0,0,5"],[9,8,7,6,5]) -> 139629729
# run_feedback_amplifier(test, [9,7,8,5,6]) -> 18216

@solution_timer(2019,7,1)
def part_one(data: List[str], verbose=False):
    outputs = []
    for phase_settings in permutations(range(5)):
        signal = run_amplifier(data, phase_settings)
        outputs.append((signal,phase_settings))
    return sorted(outputs,reverse=True)[0][0]

@solution_timer(2019,7,2)
def part_two(data: List[str], verbose=False):
    outputs = []
    phase_settings = [9,7,8,5,6]
    for phase_settings in permutations(range(5,10)):
        signal = run_feedback_amplifier(data, phase_settings)
        outputs.append(signal)
    return max(outputs)

if __name__ == "__main__":
    data = read_entire_input(2019,7)
    part_one(data)
    part_two(data)