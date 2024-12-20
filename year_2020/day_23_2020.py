"""Autogenerated solution template, v2"""
__version__ = 2


from framework.input_helper import read_entire_input, read_input_by_line
from framework.console import log
from framework.helpers import solution_timer

data = read_entire_input(2020,23)
test = ["389125467"]

def parse(data):
    return [int(i) for i in list(data[0])]

def run_game_slice(initial_state, turns):
    # Trying to keep track of wrapping indices is too hard
    # Instead, I've opted to make the "selected" cup always at the head of the list, and move
    # the entire list around to achieve this.
    cups = [i for i in initial_state]
    T = len(cups)
    for _ in range(turns):
        selection = cups[1:4]
        cups = cups[0:1] + cups[4:]
        sorted_cups = sorted(cups)
        dest = sorted_cups[(sorted_cups.index(cups[0]) - 1) % (T - 3)]
        dest_idx = cups.index(dest) + 1
        cups = cups[1:dest_idx] + selection + cups[dest_idx:] + cups[0:1]
    return cups

#@solution_timer(2020,23,1)
def part_one(data, verbose=False):
    cups = parse(data)
    T = len(cups)
    cups = run_game_slice(cups, 100)
    
    index_of_cup_1 = cups.index(1)
    # Now undo the weird loop we did earlier
    rest_of_cups = cups[index_of_cup_1 + 1 :] + cups[:index_of_cup_1]
    res = "".join([str(c) for c in rest_of_cups])
    return res

def build_linked_list(initial_state, up_to):
    cups = {}
    for i in range(0,up_to):
        if i < len(initial_state)-1:
            cups[initial_state[i]] = initial_state[i+1]
        elif i == len(initial_state)-1:
            cups[initial_state[i]] = max(initial_state)+1
        elif i < up_to-1:
            cups[i+1] = i+2
        else:
            cups[i+1] = initial_state[0]
    return cups

def run_game_linked_list(cups, selected_cup, up_to):
    T = len(cups)
    for _ in range(up_to):
        cup1 = cups[selected_cup] # The cup next to the selected cup
        cup2 = cups[cup1]
        cup3 = cups[cup2]
        # now "remove" them from the list by adjusting the pointer of the first cup
        cups[selected_cup] = cups[cup3]

        # Where do they go?
        destination_cup = (selected_cup - 1 - 1) % T + 1 # Adjust for zero/one index lists *facepalm*
        while destination_cup in [cup1, cup2, cup3]: # If the destination cup is one of the cups we've chosen, then step through the list and chose another cup
            destination_cup = (destination_cup - 1 - 1) % T + 1 # Adjust for zero/one index lists *facepalm*
        # reinsert
        cups[cup3] = cups[destination_cup] # d -> cups[d] becomes d -> cup1 -> cup2 -> cup3 -> cups[d]
        # No need to adjust cup2, it already points to cup 3
        cups[destination_cup] = cup1

        # advance the pointer
        selected_cup = cups[selected_cup]
    return cups

#@solution_timer(2020,23,2)
def part_two(data, verbose=False):
    # Using the above approach is far too slow. Like, > 10 mins slow.
    # I think the slicing of the lists is the problem
    cups = parse(data)
    selected_cup = cups[0]
    T = len(cups)
    cups = build_linked_list(cups, 1000000)
    # selected_cup = cups[1]    
    cups = run_game_linked_list(cups, selected_cup, 10000000)
    return cups[1] * cups[cups[1]]

if __name__ == "__main__":
    data = parse(data)
    part_one(data)
    part_two(data)