from typing import List, Any, Tuple
import re
from itertools import product
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import sgn

data = read_entire_input(2019,12)
test = """<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""".split("\n")
def parse(data: List[str]) -> Any:
    moons = []
    for row in data:
        x,y,z = re.findall(r'-?\d+', row)
        moons.append((int(x),int(y),int(z),0,0,0))
    return moons

def step_vel(moon1, moon2):
    dvx = sgn(moon1[0] - moon2[0])
    dvy = sgn(moon1[1] - moon2[1])
    dvz = sgn(moon1[2] - moon2[2])
    # print(moon1, moon2)
    moon1 = (moon1[0], moon1[1], moon1[2], moon1[3] - dvx, moon1[4] - dvy, moon1[5] - dvz)
    moon2 = (moon2[0], moon2[1], moon2[2], moon2[3] + dvx, moon2[4] + dvy, moon2[5] + dvz)
    return moon1, moon2

def step_pos(moon):
    return (moon[0] + moon[3], moon[1] + moon[4], moon[2] + moon[5], *moon[3:])

def energy(moons):
    en = 0
    for moon in moons:
        pot = sum([abs(i) for i in moon[0:3]])
        kin = sum([abs(i) for i in moon[3:6]])
        en += pot*kin
    return en

def lcm(x, y):
    a, b = x, y
    while a:
        a, b = b % a, a
    return x // b * y

@solution_timer(2019,12,1)
def part_one(data: List[str], verbose=False):
    moons = parse(data)
    debug = False
    for i in range(1000):
        if debug:
            print(f"After {i} steps:")
            for moon in moons:
                print(f"pos=<x={moon[0]:3}, y={moon[1]:3}, z={moon[2]:3}>, vel=<x={moon[3]:3}, y={moon[4]:3}, z={moon[5]:3}>")
        for i in range(len(moons)):
            for j in range(i, len(moons)):
                if i == j:
                    continue
                moons[i], moons[j] = step_vel(moons[i], moons[j])
        for i in range(len(moons)):
            moons[i] = step_pos(moons[i])
    return energy(moons)

@solution_timer(2019,12,2)
def part_two(data: List[str], verbose=False):
    moons = parse(data)
    xs, ys, zs = set(), set(), set()
    while True:
        for i in range(len(moons)):
            for j in range(i, len(moons)):
                moons[i], moons[j] = step_vel(moons[i], moons[j])
        for i in range(len(moons)):
            moons[i] = step_pos(moons[i])
        X = tuple((moon[0], moon[3]) for moon in moons)
        Y = tuple((moon[1], moon[4]) for moon in moons)
        Z = tuple((moon[2], moon[5]) for moon in moons)
        if X in xs and Y in ys and Z in zs:
            break
        xs.add(X)
        ys.add(Y)
        zs.add(Z)
    return lcm(lcm(len(xs), len(ys)),len(zs))

if __name__ == "__main__":
    data = read_entire_input(2019,12)
    part_one(data)
    part_two(data)