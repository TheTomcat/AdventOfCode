from collections import deque
from itertools import chain
from os import walk
from typing import Dict, List, Any, Tuple
import time
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import window, render, PointDict, Point
from util.console import console
from year_2019.intcode import IntCode, parse

data = read_entire_input(2019,17)

class Camera:
    def __init__(self, instructions):
        self.computer = IntCode(instructions)

def neighbours(x,y,W,H):
    if x+1 < W:
        yield x+1, y
    if x-1 > 0:
        yield x-1, y
    if y+1 < H:
        yield x, y+1
    if y-1 > 0:
        yield x,y-1 

def take_picture(camera, movements = None):
    if movements is None:
        movements = []
    view = []
    while not camera.halted:
        view.append(chr(camera.run(movements)))
    image = ''.join(view)
    return [list(row) for row in image.split('\n') if len(row) > 4]

def calculate_alignment_parameters(image):
    intersections = []
    for j, (p_row, row, n_row) in enumerate(window(image, 3)):
        for i, (p_pixel, pixel, n_pixel) in enumerate(window(row, 3)):
            if pixel == "#":
                if p_row[i+1] == n_row[i+1] == p_pixel == n_pixel == "#":
                    intersections.append((i+1,j+1))
    return sum(i*j for i,j in intersections)

def find_next_step(current_position: Point, current_direction: str, points: PointDict) -> Tuple[str, Point, str]:
    directions = {"^":(0,-1), ">": (1,0), "v":(0,1), "<":(-1,0)}
    rotate = {"^":">",">":"v","v":"<","<":"^"}
    revrotate = {"^":"<","<":"v","v":">",">":"^"}

    cx,cy = current_position
    cdir = directions[current_direction]

    for dx,dy in chain([cdir], directions.values()): # Start by looking forward first, doesn't matter if we revisit this direction
        step=new_dir =None
        if (dx+cx,dy+cy) not in points:
            continue
        if (dx,dy) == cdir:
            step = "F"
            new_dir = current_direction
            break
        elif (-dx,-dy) == cdir:
            continue # Ignore points that are directly behing us
        elif (dx,dy) == directions[rotate[current_direction]]:
            step = "R"
            new_dir = rotate[current_direction]
            break
        elif (dx,dy) == directions[revrotate[current_direction]]:
            step = "L"
            new_dir = revrotate[current_direction]
            break
    return step, (dx+cx, dy+cy), new_dir

def generate_scaffolding(camera: IntCode) -> Tuple[PointDict, Tuple[int,int], str]:
    view = {}
    r=c=0
    while not camera.halted:
        c+=1
        pix = camera.run([])
        if pix == 10:
            r+=1
            c=0
        elif pix == 35:
            view[(c,r)] = pix
        elif chr(pix) in "^v<>":
            X,Y = c,r
            D = chr(pix)
            view[(c,r)] = "#"
    return view, (X,Y),D

def walk_scaffolding(scaffold: PointDict, start: Point, start_dir: str, _render=False):
    pos, dir = start, start_dir
    steps = []
    step = True
    while step is not None:
        step, pos, dir = find_next_step(pos, dir, scaffold)
        steps.append(step)
        if _render:
            def render_function(p: Point, points: PointDict):
                if not p in points:
                    return ' '
                if p == pos:
                    return f'[red]{step}[/red]'
                if points[p] == 35 or points[p]=="#":
                    return chr(9608)    
            console.print(render(scaffold,render_function=render_function))
            time.sleep(0.2)
    return steps

def condense_steps(steps: List[str]):
    cstep = []
    dir = 0
    count = 1
    for step in steps:
        if step is None:
            cstep.append((dir, count))
            break
        if step in 'LR':
            #if dir == 'F': # i.e., we're changing direction
            cstep.append((dir, count))
            dir = step
            count = 1
        elif step == 'F':
            count += 1
    return cstep[1:]

def find_subseq_in_seq(seq, subseq):
    """Return an index of `subseq`uence in the `seq`uence.
    Or `-1` if `subseq` is not a subsequence of the `seq`.
    The time complexity of the algorithm is O(n*m), where
        n, m = len(seq), len(subseq)
    from https://stackoverflow.com/questions/425604/best-way-to-determine-if-a-sequence-is-in-another-sequence
    """
    i, n, m = -1, len(seq), len(subseq)
    try:
        while True:
            i = seq.index(subseq[0], i + 1, n - m + 1)
            if subseq == seq[i:i + m]:
               return i
    except ValueError:
        return -1

def is_prefix(seq, subseq):
    return find_subseq_in_seq(seq, subseq) == 0

def find_longest_repeating_subseq(seq):
    for substr_length in range(len(seq)//2,0,-1): # Can start at length of len(seq)//2 because it must repeat at least once!
        substr = seq[:substr_length]
        #print(f'examining length {substr_length} - {substr}')
        substr = seq[:substr_length]
        if find_subseq_in_seq(seq[substr_length:], substr) > -1:
            #print(' found!')
            return substr

def find_potential_covering_sequence(condensed_steps):
    cs = []
    cs.extend(condensed_steps)
    substr = find_longest_repeating_subseq(cs)
    while is_prefix(cs, substr):
        cs = cs[len(substr):]
    return substr, cs

def mutate(sequence: List, subseqs: List[List], i=-1):
    # console.print(f"[yellow] Removing element from the {i} seq {subseqs[i]}")
    subseqs[i].pop()
    seq = [i for i in sequence]
    if i == -1 and len(subseqs[i]) > 0: # We are looking at the last element and it is not yet empty, so all good
        # console.print(f"[green] NOT EMPTY, continue")
        return subseqs
    elif i < -1 and len(subseqs[i]) > 0: # We are looking at not the last element, and it is not empty, but we need to generate at least one element
        # console.print(f"[green] This not-last element is not empty, let's make some cover")
        j=1
        while i+j < 0:
            # Trim the sequence
            for substr in subseqs[:i+j]:
                while is_prefix(seq, substr):
                    seq = seq[len(substr):]
            subseqs[i+j] = find_potential_covering_sequence(seq)[0]
            # console.print(f"[red]                                - {subseqs[i+j]}")
            j+=1
        # console.print(f"{subseqs}")
        return subseqs
    elif len(subseqs[i]) == 0: # The element we're looking at is empty, so look at the previous one
        # console.print(f"[red] EMPTY, mutate!")
        return mutate(seq, subseqs, i-1) 
    raise ValueError("Invalid covering sequence")

def compute_movement_function(condensed_steps):
    cs = []
    cs.extend(condensed_steps)
    seq1, newseq = find_potential_covering_sequence(cs)
    seq2, newseq = find_potential_covering_sequence(newseq)
    seq3, newseq = find_potential_covering_sequence(newseq)
    subseqs = [seq1, seq2, seq3]
    
    # console.print(f"Subseqns: {subseqs}")
    # console.print(f"Sequence: {cs}")  
    # console.print(f"Attempting to cover sequence with sequence")
    pattern = attempt_to_cover_sequence(cs, subseqs)
    while pattern is False:
        subseqs = mutate(cs, subseqs)
        # console.print(f"Subseqns: {subseqs}")
        # console.print(f"Sequence: {cs}")
        # console.print(f"Attempting to cover sequence with sequence")
        pattern = attempt_to_cover_sequence(cs, subseqs)
    return pattern, subseqs
        
def attempt_to_cover_sequence(seq, covers):
    pattern = []
    while len(seq) > 0:
        for i, subseq in enumerate(covers):
            # console.print(f"[yellow]Try subsequence {i}", end="")
            if is_prefix(seq, subseq):
                pattern.append(i)
                # console.print(f"[green] - SUCCESS! - {pattern}")
                seq = seq[len(subseq):]
                # console.print(f"[green]            - sequence: {seq}")
                break
            # console.print("[red] Fail")
        else:
            # console.print("[red] - ALL sequences failed, mutating")
            return False
    return pattern

def encode_movement_functions_as_intcode(movement_functions: Dict[str, str], continuous='n'):
    "Also error check the input"
    output = []
    for func in movement_functions:
        if len(movement_functions[func]) > 20:
            raise IndexError(f"The movement function provided for {func}:{movement_functions[func]} is too long.")
        for char in movement_functions[func]:
            if char not in ['A','B','C','R','L',',','y','n'] and not char.isdigit():
                raise ValueError(f"Supplied {char} which is an invalid instruction")
            output.append(ord(char))
        output.append(10)
    output.append(ord(continuous))
    output.append(10)
    return output

def generate_movement_functions(main, A, B, C):
    mapping = {0:"A",1:"B",2:"C"}
    main = ','.join(mapping[i] for i in main)
    A = ','.join(','.join(map(str,i)) for i in A)
    B = ','.join(','.join(map(str,i)) for i in B)
    C = ','.join(','.join(map(str,i)) for i in C)
    return {
        "main": main,
        "A":A,
        "B":B,
        "C":C,
    }

@solution_timer(2019,17,1)
def part_one(data: List[str]):
    instructions = parse(data)
    camera = IntCode(instructions)
    image = take_picture(camera)
    return calculate_alignment_parameters(image)

@solution_timer(2019,17,2)
def part_two(data: List[str]):
    instructions = parse(data)
    robot = IntCode(instructions)
    scaffold, start, direction = generate_scaffolding(robot)
    steps = walk_scaffolding(scaffold, start, direction)
    condensed_steps = condense_steps(steps)
    cover, (A,B,C) = compute_movement_function(condensed_steps)
    movement_functions = generate_movement_functions(cover, A, B, C)
    movements = encode_movement_functions_as_intcode(movement_functions, continuous = "n")
    
    # Now reset computer, I don't know if this is necessary
    # while True:
    #     image = take_picture(robot, movements)
    #     print(image)
    #     i=input()
    instructions = parse(data)
    instructions[0] = 2
    robot = IntCode(instructions)
    output = []
    robot.provide_inputs(reversed(movements))
    while not robot.halted:
        output.append(robot.run())

    return output[-2]

if __name__ == "__main__":
    data = read_entire_input(2019,17)
    part_one(data)
    part_two(data)


# from year_2019.day_17_2019 import * ; instr = parse(data) ; camera=IntCode(instr) ; cs = condense_steps(walk_scaffolding(*generate_scaffolding(camera)))