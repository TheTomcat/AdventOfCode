from typing import List, Tuple
from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from util.shared import window, overlap

data = read_entire_input(2019,3)
test="""R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51
U98,R91,D20,R16,D67,R40,U7,R15,U6,R7""".split("\n") # 135

def parse(data: List[str]) -> List[List[Tuple[str,int]]]:
    return [[(instruction[0], int(instruction[1:])) for instruction in wire.split(",")] for wire in data]

def get_coords(wire, start=(0,0)):
    x,y = start
    yield (x,y)
    for direction, distance in wire:
        # print(direction, distance)
        if direction == "U":
            # print(direction)
            y += distance
        elif direction == "D":
            y -= distance
        elif direction == "L":
            x -= distance
        elif direction == "R":
            x += distance
        yield x,y

def Attempt1():
    def horizontal(p1,p2):
        "if p1->p2 is horizontal, return the (sorted) y values and the constant x value, else false"
        if p1[1] == p2[1]:
            return sorted([p1[1], p2[1]]), p1[0]
        return False

    def vertical(p1,p2):
        "if p1->p2 is vertical, return the (sorted) x values and the constant y value, else false"
        if p1[0] == p2[0]:
            return sorted([p1[0], p2[0]]), p1[1]
        return False

    def intersect(p1,p2,q1,q2):
        H1 = horizontal(p1,p2)
        H2 = horizontal(q1,q2)
        if bool(H1) != bool(H2): # The lines are perpendicular
            try:
                (x1,x2),y = vertical(p1,p2)
                (y1,y2),x = H2
            except TypeError as e:
                (y1,y2),x = H1
                (x1,x2),y = vertical(q1,q2)
            return (x,y) if y1 <= y <= y2 and x1 <= x <= x2 else False
        else:
            return False

    def brute_force_intersection(wire1: List[Tuple[str,int]], wire2: List[Tuple[str,int]]) -> List[Tuple[int,int]]:
        intersections = []
        for p1,p2 in window(get_coords(wire1)):
        #    p_horizontal = horizontal(p1,p2)
            for q1,q2 in window(get_coords(wire2)):
        #        q_horizontal = horizontal(q1,q2)
                intersection = intersect(p1,p2,q1,q2)
                if intersection:
                    intersections.append(intersection)
        print(intersections)
        return intersections

def find_intersections(wire1: List[Tuple[str,int]], wire2: List[Tuple[str,int]]) -> List[Tuple[int, int]]:
    intersections = []
    for p1, p2 in window(get_coords(wire1)):
        for q1,q2 in window(get_coords(wire2)):
            if p1[1] == p2[1] == q1[1] == q2[1]: # Both horizontal and the same coord
                pmin, pmax = sorted((p1[0], p2[0]))
                qmin, qmax = sorted((q1[0], q2[0]))
                if overlap(pmin, pmax, qmin, qmax): # Iterate over the length of the overlap and add these intersections
                    for x in range(max(pmin, qmin), min(pmax, qmax)+1):
                        intersections.append((x,p1[1]))
            elif p1[0] == p2[0] == q1[0] == q2[0]: # Both vertical and the same coord
                pmin, pmax = sorted((p1[1], p2[1]))
                qmin, qmax = sorted((q1[1], q2[1]))
                if overlap(pmin, pmax, qmin, qmax):
                    for y in range(max(pmin, qmin), min(pmax, qmax)+1):
                        intersections.append((p1[0],y))
            elif p1[1] == p2[1] and q1[0] == q2[0]: # P is horizontal, Q is vertical
                x1,x2 = sorted((p1[0], p2[0]))
                y = p1[1]
                y1,y2 = sorted((q1[1], q2[1]))
                x = q1[0]
                if x1 <= x <= x2 and y1 <= y <= y2:
                    intersections.append((x,y))
            elif p1[0] == p2[0] and q1[1] == q2[1]: # P is vertical, Q is horizontal
                y1,y2 = sorted((p1[1], p2[1]))
                x = p1[0]
                x1,x2 = sorted((q1[0], q2[0]))
                y = q1[1]
                if x1 <= x <= x2 and y1 <= y <= y2:
                    intersections.append((x,y))
    return intersections

def point_on_line(p1,p2,x,y):
    xmin, xmax = sorted((p1[0], p2[0]))
    ymin, ymax = sorted((p1[0], p2[0]))
    if xmin <= x <= xmax and ymin <= y <= ymax:
        return True
    return False

def length_of_line(p1,p2):
    "length of a line in taxicab metric" 
    # Number of grid squares is length of line + 1, but corners 
    # will be double counted so just add one at the end!
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

def sgn(a):
    if a > 0:
        return 1
    elif a < 0:
        return -1
    return 0

def build_point_list(wire):
    x,y = (0,0)
    yield x,y
    for p1, p2 in window(get_coords(wire)):
        deltax = sgn(p2[0]-p1[0])
        deltay = sgn(p2[1]-p1[1])
        # print(p1,p2)
        while (x,y) != p2:
            # i = input(f"{p1=} -> ({x},{y}) -> {p2=}")
            x += deltax
            y += deltay
            yield x,y

@solution_timer(2019,3,1)
def part_one(data: List[str], verbose=False):
    wire1, wire2 = parse(data)
    intersections = sorted(find_intersections(wire1, wire2), key=lambda x: abs(x[0])+abs(x[1]))
    return abs(intersections[1][0]) + abs(intersections[1][1])

@solution_timer(2019,3,2)
def part_two(data: List[str], verbose=False):
    wire1, wire2 = parse(data)
    intersections = sorted(find_intersections(wire1, wire2), key=lambda x: abs(x[0])+abs(x[1]))
    length_to_intersection = []
    point_list1 = list(build_point_list(wire1))
    point_list2 = list(build_point_list(wire2)) # Not the most elegant solution, but I'm tired and it works reasonably quickly 
    for intersection in intersections[1:]:
        length_to_intersection.append(point_list1.index(intersection)+point_list2.index(intersection))
    return min(length_to_intersection)

if __name__ == "__main__":
    data = read_entire_input(2019,3)
    part_one(data)
    part_two(data)