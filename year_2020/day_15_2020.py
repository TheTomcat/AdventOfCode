from collections import defaultdict
from tqdm import trange
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2020,15)
test = "11,18,0,20,1,7,16"

def parse(data):
    return [int(i) for i in data[0].split(',')]

def play(start_nums, end_turn):
    # This is pretty slow for a large input, and there is probably a nice way to solve it
    # that takes much shorter than the 30 sec I used...
    # history[spoken_number] = [list of turns]
    history = defaultdict(list)
    last_num = None
    for turn in range(1, end_turn+1):
        if turn <= len(start_nums): # If we are in the starting numbers
            spoken_num = start_nums[turn-1]
            history[spoken_num].append(turn)
            last_num = spoken_num

        elif len(history[last_num]) == 1: # This was the first time the previous number was spoken
            spoken_num = 0
            history[spoken_num].append(turn)
            last_num = spoken_num
        else: # We've spoken that number a few times already
            spoken_num = history[last_num][-1] - history[last_num][-2] 
            history[spoken_num].append(turn)
            last_num = spoken_num
    return spoken_num

@solution_timer(2020,15,1)
def part_one(data):
    starting_numbers = parse(data)
    return play(starting_numbers, 2020)    


@solution_timer(2020,15,2)
def part_two(data):
    starting_numbers = parse(data)
    return play(starting_numbers, 30000000)    

if __name__ == "__main__":
    data = read_entire_input(2020,15)
    part_one(data)
    part_two(data)