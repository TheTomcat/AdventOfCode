"""Autogenerated solution template, v2"""
__version__ = 2

from collections import deque

from framework.input_helper import read_entire_input, read_input_by_line
from framework.console import log
from framework.helpers import solution_timer

data = read_entire_input(2020,22)

test = """Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10""".split("\n")

test2 = """Player 1:
43
19

Player 2:
2
29
14""".split("\n")


def parse(data):
    hands = [deque(), deque()]
    hand = hands[0]
    for row in data[1:]:
        if row == "Player 2:":
            hand = hands[1]
        elif row != "":
            hand.append(int(row))
    return hands
 
def play_combat(a: deque,b: deque):
    a_card = a.popleft()
    b_card = b.popleft()
    if a_card > b_card:
        a.append(a_card)
        a.append(b_card)
    else:
        b.append(b_card)
        b.append(a_card)
    return a,b
    
def score(a: deque,b: deque, force_win=None):
    if len(a)==0 or force_win == "b":
        d=b
    else:
        d=a
    multiplier = 1
    total = 0
    while len(d) > 0:
        v = d.pop()
        # print(v, multiplier)
        total += multiplier * v
        multiplier += 1
    return total

def play_all_recursive_combat(a: deque,b: deque):
    previous_rounds = []
    while True:
        previous_rounds.append((tuple(a),tuple(b)))
        # log.debug(f"Player 1's deck: {a}")
        # log.debug(f"Player 2's deck: {b}")        
        a_card = a.popleft()
        b_card = b.popleft()

        # log.debug(f"Player 1 plays {a_card}")
        # log.debug(f"Player 2 plays {b_card}")
        if len(a) >= a_card and len(b) >= b_card:
            # log.debug("Playing a sub-game to determine the winner...")
            # s = input() #log.debug()
            new_a_deck = deque()
            new_a_deck.extend([a[i] for i in range(a_card)])
            new_b_deck = deque()
            new_b_deck.extend([b[i] for i in range(b_card)])
            a_wins, _, _ = play_all_recursive_combat(new_a_deck, new_b_deck)
            # log.debug(f"The winner of the sub-game is player {1 if a_wins else 2}")
            # spawn a recursive game and play it to find the winner
        else:
            a_wins = a_card > b_card

        if a_wins:
            a.append(a_card)
            a.append(b_card)
        else:
            b.append(b_card)
            b.append(a_card)
        if ((tuple(a),tuple(b)) in previous_rounds):
            # log.debug(f"Infinite rule - {tuple(a),tuple(b)}")
            return True, a, b
        if len(a) * len(b) == 0:
            return len(a) > 0, a, b # I.e., A wins if A has card 


#@solution_timer(2020,22,1)
def part_one(data, verbose=False):
    a,b = parse(data)
    round = 1
    while len(a) * len(b) != 0:
        round += 1
        # print()
        a,b = play_combat(a,b)
    return score(a,b)

#@solution_timer(2020,22,2)
def part_two(data, verbose=False):
    a_deck,b_deck = parse(data)
    log.setLevel("ERROR")
    winner, A, B = play_all_recursive_combat(a_deck, b_deck)
    return score(A,B)
    # previous_rounds = []
    # while len(a_deck) * len(b_deck) != 0 and (tuple(a_deck),tuple(b_deck) not in previous_rounds):
    #     previous_rounds.append((tuple(a_deck),tuple(b_deck)))
    #     a_deck, b_deck, a_card, b_card= play_recursive_combat(a_deck,b_deck)
        

    
