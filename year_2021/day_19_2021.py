from typing import Dict, List, Any, Tuple, Set
from collections import defaultdict, namedtuple
from itertools import product
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2021,19)

class P:
    def __init__(self, *pos):
        self.pos = pos
    def __add__(self, other):
        return P(*[x+y for x,y in zip(self.pos, other.pos)])
    def __sub__(self, other):
        return P(*[x-y for x,y in zip(self.pos, other.pos)])
    def __abs__(self):
        return P(*[abs(x) for x in self.pos])
    def __repr__(self):
        return f"P{self.pos}"
    
Beacon = namedtuple("Beacon", ["scanner","beacon"])

def add_to_equivalence_class(equivalence_classes: List[Set], val1, val2):
    """equivalence_classes represents a group of equivalence classes, stored as a list of sets.
    The assertion by running this function is that val1 == val2.
    Values are added to the appropriate class
    """
    match1 = [val1 in r for r in equivalence_classes]
    match2 = [val2 in r for r in equivalence_classes]
    if any(match1) and any(match2):
        if match1.index(True)==match2.index(True):
            return
        eq2 = equivalence_classes[match2.index(True)]
        equivalence_classes[match1.index(True)].update(eq2)
        del equivalence_classes[match2.index(True)]
    elif any(match1):
        equivalence_classes[match1.index(True)].add(val2)
    elif any(match2):
        equivalence_classes[match2.index(True)].add(val1)
    else:
        equivalence_classes.append({val1, val2})
        
def parse(data: List[str]) -> Dict[int, List]:
    scanners = defaultdict(list)
    sc_index = -1
    for row in data:
        if not row:
            continue
        if row.startswith("---"):
            sc_index += 1
            continue
        scanners[sc_index].append(P(*tuple(int(i) for i in row.split(","))))
    return scanners

def d(p1,p2):
    return sum((i-j)**2 for i,j in zip(p1.pos,p2.pos)) 

def generate_fingerprints(scanner) -> List[Set[Tuple]]:
    fingerprints = [] # fingerprints[origin_beacon][beacon]
    for origin in scanner: # taking one beacon as the origin
        fingerprint = set()
        for beacon in scanner: # and comparing it to every other one
            if beacon == origin:
                continue
            iden = tuple(sorted(abs(beacon-origin).pos))
            # iden = d(origin, beacon)
            fingerprint.add(iden) 
            # Get the absolute value of x-o for each coordinate
            # And then sort them, because we don't actually care if it's x, y, or z
            # This will avoid having to worry about rotations until later
        fingerprints.append(fingerprint)
    return fingerprints

def find_adjacent_scanners(scanners):
    fingerprints = {}
    eqc = []
    for i, scanner in scanners.items():
        fingerprints[i] = generate_fingerprints(scanner)
    for i, j in product(range(len(scanners)), repeat=2):
        if i == j: continue
        for origin_k, fingerprint_i in enumerate(fingerprints[i]):
            match = False
            for origin_l, fingerprint_j in enumerate(fingerprints[j]):
                alike = fingerprint_i.intersection(fingerprint_j)
                if len(alike) == 11: 
                    # we have found a set of points that have 11 matching fingerprints
                    # This implies that the origin and 11 matching points are in both scanners
                    # for matching_diff in alike:
                    #     beacon_1 = fingerprint_i.index(matching_diff)
                    #     beacon_2 = fingerprint_j.index(matching_diff)
                    add_to_equivalence_class(eqc, Beacon(scanner=i, beacon=origin_k), Beacon(scanner=j, beacon=origin_l))
                    match = True
                    continue 
            if match:
                continue
    return eqc

def by_scanner(*scanners):
    def f(beacon):
        return beacon.scanner in scanners
    return f

def find_matched_beacons(eqc, *scanners):
    return list(filter(lambda x: len(x)==len(scanners), (list(filter(by_scanner(scanners), i)) for i in eqc)))

def find_equivalent_beacons(scanners, equivalence_classes):
    output = []
    for eqc in equivalence_classes:
        output.append([(Beacon(scanner=b.scanner, beacon=b.beacon), scanners[b.scanner][b.beacon]) for b in eqc])
    return output

@solution_timer(2021,19,1)
def part_one(data: List[str], verbose=False):
    scanners = parse(data)
    eqc = find_adjacent_scanners(scanners)
    num_beacons = sum(len(i) for i in scanners.values())
    return num_beacons - sum(len(i) for i in eqc) + len(eqc)

@solution_timer(2021,19,2)
def part_two(data: List[str], verbose=False):
    _ = parse(data)

    return 0

if __name__ == "__main__":
    data = read_entire_input(2021,19)
    part_one(data)
    part_two(data)

test = """--- scanner 0 ---
404,-588,-901
528,-643,409
-838,591,734
390,-675,-793
-537,-823,-458
-485,-357,347
-345,-311,381
-661,-816,-575
-876,649,763
-618,-824,-621
553,345,-567
474,580,667
-447,-329,318
-584,868,-557
544,-627,-890
564,392,-477
455,729,728
-892,524,684
-689,845,-530
423,-701,434
7,-33,-71
630,319,-379
443,580,662
-789,900,-551
459,-707,401

--- scanner 1 ---
686,422,578
605,423,415
515,917,-361
-336,658,858
95,138,22
-476,619,847
-340,-569,-846
567,-361,727
-460,603,-452
669,-402,600
729,430,532
-500,-761,534
-322,571,750
-466,-666,-811
-429,-592,574
-355,545,-477
703,-491,-529
-328,-685,520
413,935,-424
-391,539,-444
586,-435,557
-364,-763,-893
807,-499,-711
755,-354,-619
553,889,-390

--- scanner 2 ---
649,640,665
682,-795,504
-784,533,-524
-644,584,-595
-588,-843,648
-30,6,44
-674,560,763
500,723,-460
609,671,-379
-555,-800,653
-675,-892,-343
697,-426,-610
578,704,681
493,664,-388
-671,-858,530
-667,343,800
571,-461,-707
-138,-166,112
-889,563,-600
646,-828,498
640,759,510
-630,509,768
-681,-892,-333
673,-379,-804
-742,-814,-386
577,-820,562

--- scanner 3 ---
-589,542,597
605,-692,669
-500,565,-823
-660,373,557
-458,-679,-417
-488,449,543
-626,468,-788
338,-750,-386
528,-832,-391
562,-778,733
-938,-730,414
543,643,-506
-524,371,-870
407,773,750
-104,29,83
378,-903,-323
-778,-728,485
426,699,580
-438,-605,-362
-469,-447,-387
509,732,623
647,635,-688
-868,-804,481
614,-800,639
595,780,-596

--- scanner 4 ---
727,592,562
-293,-554,779
441,611,-461
-714,465,-776
-743,427,-804
-660,-479,-426
832,-632,460
927,-485,-438
408,393,-506
466,436,-512
110,16,151
-258,-428,682
-393,719,612
-211,-452,876
808,-476,-593
-575,615,604
-485,667,467
-680,325,-822
-627,-443,-432
872,-547,-609
833,512,582
807,604,487
839,-516,451
891,-625,532
-652,-548,-490
30,-46,-14""".split('\n')