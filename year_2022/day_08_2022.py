from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

data = read_entire_input(2022,8)
test = """30373
25512
65332
33549
35390""".split("\n")

def parse(data: List[str]) -> Any:
    heights = {}
    for y, row in enumerate(data):
        for x, height in enumerate(row):
            heights[(x,y)] = height
    return heights, len(data[0]), len(data)

def is_visible(heights, W, H, x, y):
    this_height = heights[(x,y)]
    visible = [-1] * 4
    for i,( dx,dy) in enumerate(((1,0),(0,1),(-1,0),(0,-1))):
        cx, cy = x+dx,y+dy
        while 0 <= cx < W and 0 <= cy < H:
            if heights[cx,cy] >= this_height:
                visible[i] = (dx,dy)
                #return visible
            cx += dx
            cy += dy
    return visible


@solution_timer(2022,8,1)
def part_one(data: List[str]):
    heights, W, H = parse(data)
    c = 0
    for x in range(W):
        for y in range(H):
            if any(i==-1 for i in is_visible(heights, W, H, x, y)):
                c+=1
    return c

def calculate_scenic_score(heights, W, H, x, y):
    this_height = heights[(x,y)]
    dist = [0] * 4
    if x==0 or x==W-1 or y==0 or y==H-1:
        return 0
    for i,( dx,dy) in enumerate(((1,0),(0,1),(-1,0),(0,-1))):
        cx, cy = x+dx,y+dy
        while 0 <= cx < W and 0 <= cy < H:
            if heights[cx,cy] >= this_height:
                dist[i] = max(abs(cx-x), abs(cy-y))
                break
            cx += dx
            cy += dy
        else:
            dist[i] = max(abs(cx-x), abs(cy-y))-1
    return dist[0]*dist[1]*dist[2]*dist[3]
    

@solution_timer(2022,8,2)
def part_two(data: List[str]):
    heights, W, H = parse(data)
    scores = {}
    for y in range(H):
        for x in range(W):
            scores[(x,y)] = calculate_scenic_score(heights, W, H, x, y)
    return max(scores.values())

if __name__ == "__main__":
    data = read_entire_input(2022,8)
    part_one(data)
    part_two(data)