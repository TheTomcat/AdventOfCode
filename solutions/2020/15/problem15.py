from collections import defaultdict
from tqdm import trange

def read_input(i):
    with open(f'turn/{i}/input.txt', 'r') as f:
        return f.read()

text = "11,18,0,20,1,7,16"

def process(text):
    return [int(i) for i in text.split(',')]

def play(start_nums, end_turn):
    # This is pretty slow for a large input, and there is probably a nice way to solve it
    # that takes much shorter than the 30 sec I used...
    # history[spoken_number] = [list of turns]
    history = defaultdict(list)
    last_num = None
    for turn in trange(1, end_turn+1):
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

turn = 2020
print(play([0,3,6],turn), 436)
print(play([1,3,2],turn),1)
print(play([2,1,3],turn),10)
print(play([1,2,3],turn),27)
print(play([2,3,1],turn),78)
print(play([3,2,1],turn),438)
print(play([3,1,2],turn),1836)

print(play(process(text), turn))

turn = 30000000
# print(play([0,3,6],turn), 175594)
# print(play([1,3,2],turn),2578)
# print(play([2,1,3],turn),3544142)
# print(play([1,2,3],turn),261214)
# print(play([2,3,1],turn),6895259)
# print(play([3,2,1],turn),18)
# print(play([3,1,2],turn),362)

print(play(process(text), turn))