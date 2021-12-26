from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,21)

def parse(data: List[str]) -> Any:
    return [int(row.split(":")[1]) for row in data]

class DeterministicDice:
    def __init__(self, cycle=100):
        self.state = 1
        self.cycle = cycle
        self.n = 0

    def roll(self, n=3):
        roll = [((self.state + i - 1) % self.cycle)+1  for i in range(n)]
        self.state += n
        self.n += n
        return roll

class DiracDie:
    pass

class Player:
    def __init__(self, s, cycle=10):
        self.position = s
        self.cycle = cycle
        self.score = 0
    def move(self, n):
        self.position += n
        self.position = ((self.position -1) % self.cycle) + 1
        self.score += self.position

def win(p1: Player, p2: Player):
    return p1.score >= 1000 or p2.score >= 1000

def sim(s1, s2):
    d = DeterministicDice()
    p1 = Player(s1)
    p2 = Player(s2)
    
    while not win(p1, p2):
        # for roll in d.roll():
        p1.move(sum(d.roll()))
        if win(p1, p2):
            return min(p1.score, p2.score) * d.n
    # for roll in d.roll():
        p2.move(sum(d.roll()))
        if win(p1, p2):
            return min(p1.score, p2.score) * d.n
    

@solution_timer(2021,21,1)
def part_one(data: List[str]):
    d = DeterministicDice()
    s1, s2 = parse(data)
    return sim(s1, s2)

@solution_timer(2021,21,2)
def part_two(data: List[str]):
    _ = parse(data)

    return False

if __name__ == "__main__":
    data = read_entire_input(2021,21)
    part_one(data)
    part_two(data)