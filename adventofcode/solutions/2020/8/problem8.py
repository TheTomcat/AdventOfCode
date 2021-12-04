def read_input(i):
    with open(f'2020/{i}/input.txt', 'r') as f:
        return f.read()
        
def process_data(data):
    lines = data.split("\n")
    commands = []
    for line in lines:
        command = line.split(" ")
        commands.append((command[0], int(command[1].strip("+"))))
    return commands

def step(commands, pointer, accumulator):
    command = commands[pointer][0]
    argument = commands[pointer][1]
    if command == "acc":
        accumulator += argument
        pointer += 1
    elif command == "nop":
        pointer += 1
    elif command == "jmp":
        pointer += argument
    return pointer, accumulator

def run(commands, start=0):
    visited = []
    pointer = start
    accumulator = 0
    while pointer < len(commands):
        visited.append(pointer)
        pointer, accumulator = step(commands, pointer, accumulator)
        if pointer in visited:
            return 1, accumulator
    return 0, accumulator

def find_corrupted_commands(commands):
    for command_index, (command, argument) in enumerate(commands):
        if command not in ["nop", "jmp"]:
            continue
        commands = alter_command(commands, command_index) 
        code, acc = run(commands)
        if code == 0:
            print(f"command {command} at {command_index}")
            return acc
        commands = alter_command(commands, command_index)

def alter_command(commands, command_index):
    rep = {"nop":"jmp","jmp":"nop"}
    return commands[0:command_index] + [(rep[commands[command_index][0]],commands[command_index][1])] + commands[command_index+1:]

data = read_input(8)
commands = process_data(data)
print(run(commands, 0))
print(find_corrupted_commands(commands))