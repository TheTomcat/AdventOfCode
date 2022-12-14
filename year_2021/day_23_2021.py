from collections import defaultdict
from typing import List, Any, Tuple
from itertools import chain
from framework.console import console
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.graph.pathfinding import search, construct_path, A_star
from util.shared import window

data = read_entire_input(2021,23)

def parse(data: List[str]) -> Any:
    return data[1][1:-1] + data[2][3:10:2] + data[3][3:10:2]

COST = {'A':1, 'B':10, 'C': 100, 'D':1000}
END = '.'*11 + 'ABCD'*2
END2 = '.'*11 + 'ABCD'*4
VALID = [0,1,3,5,7,9,10] # theoretically valid positions
    
G = {0:(1,),
     1:(0,2),
     2:(1,3,11),
     3:(2,4),
     4:(3,5,12),
     5:(4,6),
     6:(5,7,13),
     7:(6,8),
     8:(7,9,14),
     9:(8,10),
     10:(9,),
     11:(2,15),
     12:(4,16),
     13:(6,17),
     14:(8,18),
     15:(11,),
     16:(12,),
     17:(13,),
     18:(14,)}

G2 = G.copy()
G2.update({15:(11,19),
      16:(12,20),
      17:(13,21),
      18:(14,22),
      19:(15,23),
      20:(16,24),
      21:(17,25),
      22:(18,26),
      23:(19,),
      24:(20,),
      25:(21,),
      26:(22,)})

def build_paths(adjacency):
    paths = {}
    for start in adjacency:
        paths[start] = {}
        dfs = search(start, lambda position: ((neighb, 1) for neighb in adjacency[position]))
        for end in adjacency:
            paths[start][end] = construct_path(dfs, end, weighted=False)
    return paths

def find_all_steps(state, current_position, num_amphipods=4):

    if current_position > 10: # We are in a well
        yield from VALID # So any position in the top row is valid
    
    # For any starting position, we can move into an empty well
    WELLS = {'A':1, 'B':2, 'C':3,'D':4}
    dest_well = WELLS[state[current_position]]

    if num_amphipods == 4:
        if state[22+dest_well] == '.':
            yield 22+dest_well
        elif state[18+dest_well] == '.' and state[22+dest_well] == state[current_position]:
            yield 18+dest_well
        elif state[14+dest_well] == '.' and state[18+dest_well] == state[22+dest_well] == state[current_position]:
            yield 14+dest_well
        elif state[10+dest_well] == '.' and state[14+dest_well] == state[18+dest_well] == state[22+dest_well] == state[current_position]:
            yield 10+dest_well
    else:
        if state[14+dest_well] == '.':
            yield 14+dest_well
        elif state[10+dest_well] == '.' and state[14+dest_well] == state[current_position]:
            yield 10+dest_well

    # for depth in range(num_amphipods-1,-1,-1):
    #     if state[10+4*depth+dest_well] == '.':
    #         yield 10+4*depth+dest_well
    #     else:
    #         break
        


    # valid_wells = [1,2,3,4]
    # if current_position > 10: # We're in a well
    #     yield from VALID # Move to the top
    #     valid_wells.remove((current_position-11) % 4 + 1) # Remove the current well
    # WELLS = {'A':1, 'B':2, 'C':3,'D':4}
    # w = state[current_position]
    # if w in valid_wells:
    #     valid_wells.remove(WELLS[state[current_position]])
    #  # We're in the top OR in a well, move to a well.
    # # wellnum = lambda x: 0 if x <= 10 else (x-11) % 4 + 1
        
    # if num_amphipods == 4:
    #     # yield from [i for i in range(23,27) if state[i] == '.' ]
    #     # yield from [i for i in range(19,23) if state[i] == '.' and state[i+4] == state[current_position]]
    #     # yield from [i for i in range(15,19) if state[i] == '.' and state[i+4] == state[i+8] == state[current_position] ]
    #     # yield from [i for i in range(11,15) if state[i] == '.' and state[i+4] == state[i+8] == state[i+12] == state[current_position]]
    #     yield from [i+22 for i in valid_wells if state[i+22] == '.' ]
    #     yield from [i+18 for i in valid_wells if state[i+18] == '.' and state[i+18+4] == state[current_position]]
    #     yield from [i+14 for i in valid_wells if state[i+14] == '.' and state[i+14+4] == state[i+14+8] == state[current_position] ]
    #     yield from [i+10 for i in valid_wells if state[i+10] == '.' and state[i+10+4] == state[i+10+8] == state[i+10+12] == state[current_position]]    
    # else:
    #     yield from [i for i in range(15,19) if state[i] == '.' ]
    #     yield from [i for i in range(11,15) if state[i] == '.' and state[i+4] == state[current_position]]
            
def is_step_valid(start, end, state, paths):
    return all(state[i] == '.' for i in paths[start][end][1:])

def neighbours(state:str, paths, num_amphipods=4):
    for chr in 'ABCD':
        index = 0
        for _ in range(num_amphipods):
            old_position = state.index(chr, index)
            index = old_position+1
            for new_position in find_all_steps(state, old_position, num_amphipods):
                if is_step_valid(old_position, new_position, state, paths):
                    new_state = list(state)
                    new_state[old_position] = '.'
                    new_state[new_position] = chr
                    yield ''.join(new_state), (len(paths[old_position][new_position])-1) * COST[chr]

def heuristic(state: str, paths, num_amphipods=4):
    if num_amphipods == 4:
        EP = {'A':23,'B':24,'C':25,'D':26}
    elif num_amphipods == 2:
        EP = {'A':15,'B':16,'C':17,'D':18}
    heur = 0
    for chr in 'ABCD':
        dist = 0
        ind = 0
        for _ in range(num_amphipods):
            next_pos = state.index(chr, ind)
            ind = next_pos + 1
            dist += len(paths[next_pos][EP[chr]]) - 1
        dist -= (num_amphipods) * (num_amphipods - 1) / 2
        heur += dist * COST[chr]
    return heur

def draw(state, weight=None):
    print("#"*13)
    print("#" + state[:11]+"#")
    i=11
    while i < len(state):
        print("  #" + "#".join(state[i:i+4]) + "#  ")
        i+=4
    if weight is not None:
        print(f"{weight=:^13}")
    # print()

def comp_draw(old_state, new_state, paths, weight=None):
    # Compute cost to convert
    cost = 0
    try:
        (x, (a,b)),(y, (c,d)) = list(highlight_differences(old_state, new_state))
    except ValueError as e:
        return
    char = a if a != '.' else b
    cost = (len(paths[x][y]) - 1) * COST[char]

    std = {i:c for i,c in enumerate(new_state)}
    std[x] = '[red]' + std[x] + '[/red]'
    std[y] = '[red]' + std[y] + '[/red]'

    output = "#"*13 + '\n'
    output += "#" + ''.join(std[k] for k in range(11)) +"#"+ '\n'
    i=11
    while i < len(new_state):
        output += "  #" + "#".join(std[k] for k in range(i, i+4)) + "#  "+ '\n'
        i+=4
    if weight is not None:
        output += f"{weight=:^13} (+{cost})"+ '\n'
    console.print(output)

def draw_moves(mapping, end_node, paths):
    p = construct_path(mapping, end_node, True)
    for (old, old_w),(new, new_w) in window(p):
        comp_draw(old, new, paths, new_w)

def highlight_differences(string1, string2):
    for i, (a,b) in enumerate(zip(string1, string2)):
        if a != b:
            yield i, (a, b)

@solution_timer(2021,23,1)
def part_one(data: List[str], verbose=False):
    state = parse(data)
    paths = build_paths(G)
    mapping, end_node = A_star(state, END, lambda st: neighbours(st, paths, 2), lambda st,_: heuristic(st, paths, 2))#, draw=lambda x: None)
    return mapping[end_node]['cost']

@solution_timer(2021,23,2)
def part_two(data: List[str], verbose=False):
    state = parse(data)
    state = state[:15] + 'DCBA'+'DBAC' + state[15:]
    #state = '...........BCBDDCBADBACADCA'
    paths = build_paths(G2)
    mapping, end_node = A_star(state, END2, lambda st: neighbours(st, paths, 4), lambda st,_: heuristic(st, paths, 4))#, draw=draw)
    return mapping[end_node]['cost']

if __name__ == "__main__":
    data = read_entire_input(2021,23)
    part_one(data)
    part_two(data)