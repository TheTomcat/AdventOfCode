from typing import List, Any, Tuple
import math
from collections import defaultdict, deque, namedtuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2019,14)
test="""10 ORE => 10 A
1 ORE => 1 B
7 A, 1 B => 1 C
7 A, 1 C => 1 D
7 A, 1 D => 1 E
7 A, 1 E => 1 FUEL""".split("\n") # 31

test1 = """9 ORE => 2 A
8 ORE => 3 B
7 ORE => 5 C
3 A, 4 B => 1 AB
5 B, 7 C => 1 BC
4 C, 1 A => 1 CA
2 AB, 3 BC, 4 CA => 1 FUEL""".split('\n') # 165

test2 = """157 ORE => 5 NZVS
165 ORE => 6 DCFZ
44 XJWVT, 5 KHKGT, 1 QDVJ, 29 NZVS, 9 GPVTF, 48 HKGWZ => 1 FUEL
12 HKGWZ, 1 GPVTF, 8 PSHF => 9 QDVJ
179 ORE => 7 PSHF
177 ORE => 5 HKGWZ
7 DCFZ, 7 PSHF => 2 XJWVT
165 ORE => 2 GPVTF
3 DCFZ, 7 NZVS, 5 HKGWZ, 10 PSHF => 8 KHKGT""".split("\n") # 13312

test3 = """2 VPVL, 7 FWMGM, 2 CXFTF, 11 MNCFX => 1 STKFG
17 NVRVD, 3 JNWZP => 8 VPVL
53 STKFG, 6 MNCFX, 46 VJHF, 81 HVMC, 68 CXFTF, 25 GNMV => 1 FUEL
22 VJHF, 37 MNCFX => 5 FWMGM
139 ORE => 4 NVRVD
144 ORE => 7 JNWZP
5 MNCFX, 7 RFSQX, 2 FWMGM, 2 VPVL, 19 CXFTF => 3 HVMC
5 VJHF, 7 MNCFX, 9 VPVL, 37 CXFTF => 6 GNMV
145 ORE => 6 MNCFX
1 NVRVD => 8 CXFTF
1 VJHF, 6 MNCFX => 4 RFSQX
176 ORE => 6 VJHF""".split('\n') # 180697

test4 = """171 ORE => 8 CNZTR
7 ZLQW, 3 BMBT, 9 XCVML, 26 XMNCP, 1 WPTQ, 2 MZWV, 1 RJRHP => 4 PLWSL
114 ORE => 4 BHXH
14 VRPVC => 6 BMBT
6 BHXH, 18 KTJDG, 12 WPTQ, 7 PLWSL, 31 FHTLT, 37 ZDVW => 1 FUEL
6 WPTQ, 2 BMBT, 8 ZLQW, 18 KTJDG, 1 XMNCP, 6 MZWV, 1 RJRHP => 6 FHTLT
15 XDBXC, 2 LTCX, 1 VRPVC => 6 ZLQW
13 WPTQ, 10 LTCX, 3 RJRHP, 14 XMNCP, 2 MZWV, 1 ZLQW => 1 ZDVW
5 BMBT => 4 WPTQ
189 ORE => 9 KTJDG
1 MZWV, 17 XDBXC, 3 XCVML => 2 XMNCP
12 VRPVC, 27 CNZTR => 2 XDBXC
15 KTJDG, 12 BHXH => 5 XCVML
3 BHXH, 2 VRPVC => 7 MZWV
121 ORE => 7 VRPVC
7 XCVML => 6 RJRHP
5 BHXH, 4 VRPVC => 5 LTCX""".split('\n') # 2210736

def parse(data: List[str]) -> Any:
    reactions = {}
    for row in data:
        reagents, products = row.split(" => ")
        reagents = [(int(i.split(" ")[0]), i.split(' ')[1]) for i in reagents.split(", ")]
        products = products.split(" ")
        reactions[products[1]] = (int(products[0]), reagents)
    return reactions

def calculate_ore_required(reactions, fuel=1):
    requirements = defaultdict(int)
    requirements['FUEL'] = fuel
    leftovers = defaultdict(int)
    ore = 0
    while requirements:
        # choose a product I need
        product = list(requirements.keys())[0]
        # if we have it already
        if leftovers[product] > requirements[product]:
            leftovers[product] -= requirements[product] # Remove it from leftovers
            del requirements[product] # Remove it from required
            continue # Skip processing this step
        
        amt_required = requirements[product] - leftovers[product]
        amt_produced = reactions[product][0]
        del requirements[product]
        del leftovers[product]

        rxn = math.ceil(amt_required / amt_produced)
        leftovers[product] += amt_produced * rxn - amt_required
        for amt_reagent, reagent in reactions[product][1]:
            if reagent == "ORE":
                ore += amt_reagent * rxn
            else:
                requirements[reagent] += amt_reagent * rxn
    return ore

@solution_timer(2019,14,1)
def part_one(data: List[str], verbose=False):
    reactions = parse(data)
    return calculate_ore_required(reactions, 1)

@solution_timer(2019,14,2)
def part_two(data: List[str], verbose=False):
    reactions = parse(data)
    high = 1E12 // calculate_ore_required(reactions, 1)
    while calculate_ore_required(reactions, high) < 1E12:
        low = high
        high = high*10
    while high-low > 1:
        mid = (high + low) // 2
        ore = calculate_ore_required(reactions, mid)
        if ore < 1E12:
            low = mid
        elif ore > 1E12:
            high = mid
        else:
            break
    return int(low)

if __name__ == "__main__":
    data = read_entire_input(2019,14)
    part_one(data)
    part_two(data)