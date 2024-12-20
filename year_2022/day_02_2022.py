"""Autogenerated solution template, v2"""
__version__ = 2

from typing import List, Any, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input

data = read_entire_input(2022,2)
test = """A Y
B X
C Z""".split('\n')


def parse(data: List[str]) -> Any:
    moves = []
    for row in data:
        moves.append(row.split(' '))
    return moves

points_for_play = {
    'X': 1,
    'Y': 2,
    'Z': 3
}

def points_for_win(opp, strat):
    OPP = {'A':0, 'B':1, 'C':2}[opp]
    STRAT = {'X':0, 'Y':1, 'Z':2}[strat]
    if OPP==STRAT:
        return 3
    if (OPP+1)%3 == STRAT:
        return 6
    return 0
    
#@solution_timer(2022,2,1)
def part_one(data: List[str], verbose=False):
    moves = parse(data)
    score = 0
    for opp, strat in moves:
        score += points_for_play[strat]
        score += points_for_win(opp,strat)
    return score

def what_to_play(opp, outcome):
    '''For a given opponent play and a required outcome, tell me what I need to play'''
    OPP = {'A':0, 'B':1, 'C':2}[opp]
    OUTCOME = {'X':-1, 'Y':0, 'Z':1}[outcome]
    return (OPP+OUTCOME )% 3+1

points_for_outcome = {
    'X':0,'Y':3,'Z':6
}

#@solution_timer(2022,2,2)
def part_two(data: List[str], verbose=False):
    moves = parse(data)
    score = 0
    for opp, outcome in moves:
        score += what_to_play(opp, outcome)
        score += points_for_outcome[outcome]
    
    return score

if __name__ == "__main__":
    data = read_entire_input(2022,2)
    part_one(data)
    part_two(data)