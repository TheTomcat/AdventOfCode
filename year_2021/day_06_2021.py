from typing import List
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,6)
test=["3,4,3,1,2"]


def parse(data):
    internal_timers = [int(i) for i in data[0].split(",")]
    return internal_timers


class LanternFish:
    def __init__(self, timer):
        self.timer = timer
    def procreate(self):
        return LanternFish(8)
    def tick(self):
        self.timer -= 1
        if self.timer < 0:
            self.timer = 6
            return self.procreate()

def make_fish(timers):
    fishes: List[LanternFish] = []
    for time in timers:
        fishes.append(LanternFish(time))
    return fishes

def brute_force_simulate_fish(fishes, days):
    for day in range(days):
        new_fishes = []
        for fish in fishes:
            a = fish.tick()
            if a:
                new_fishes.append(a)
        fishes.extend(new_fishes)
    return fishes

@solution_timer(2021,6,1)
def part_one(data):
    timers = parse(data)
    fishes = make_fish(timers)
    fishes = brute_force_simulate_fish(fishes, 80)
    return len(fishes)

def smart_simulate_fish(timers, days):
    possible_ages = [0]*9
    for timer in timers:
        possible_ages[timer] += 1
    # print(f"Initial state: {possible_ages}")
    for day in range(days):
        new_fish = possible_ages.pop(0)
        possible_ages.append(new_fish)
        possible_ages[6] += new_fish
        # print(f"After {day+1:3} days: {possible_ages} => {sum(possible_ages)}")
    return sum(possible_ages)

@solution_timer(2021,6,2)
def part_two(data):
    timers = parse(data)
    return smart_simulate_fish(timers, 256)

if __name__ == "__main__":
    data = read_entire_input(2021,6)
    part_one(data)
    part_two(data)