import time
from typing import List, Any, Tuple
from collections import defaultdict

from framework.helpers import solution_timer
from framework.input_helper import read_entire_input
from framework.console import console
from lib.shared import sgn
from year_2019.intcode import IntCode, parse

display = False

data = read_entire_input(2019,13)

def render(screen, score):
    tiles = {0:" ",1:f'[white]{chr(9608)}', 2:"[green]#", 3: "-", 4: "[red]O"}
    xmin = min(i[0] for i in screen.keys())
    xmax = max(i[0] for i in screen.keys())
    ymin = min(i[1] for i in screen.keys())
    ymax = max(i[1] for i in screen.keys())
    image = '\n'.join(''.join(tiles[screen[(i,j)]] for i in range(xmin, xmax+1)) for j in range(ymin, ymax+1))
    return image+'\n'+"-"*20 + f'{score:05d}' + "-"*20

@solution_timer(2019,13,1)
def part_one(data: List[str], verbose=False):
    instructions = parse(data)
    game = IntCode(instructions)
    screen = {}
    while not game.halted:
        x, y, tile = game.run([]), game.run([]), game.run([])
        screen[(x,y)] = tile
    if display:
        console.print(render(screen, 0))
    return sum(1 for _, tile in screen.items() if tile == 2)

@solution_timer(2019,13,2)
def part_two(data: List[str], verbose=False):
    render_screen = False
    instructions = parse(data)
    instructions[0] = 2
    game = IntCode(instructions)
    screen = {}
    inputs = []
    while not game.halted:
        x = game.run(inputs)
        y = game.run(inputs)
        tile = game.run(inputs)
        if (x,y) == (-1,0):
            score = tile
        else:
            screen[(x,y)] = tile
        # if (x,y) == 
        ball = [position for position, tile in screen.items() if tile == 4]
        paddle = [position for position, tile in screen.items() if tile == 3]
        if ball and paddle:
            inputs = [sgn(ball[0][0]-paddle[0][0])]
        # if tile == 4:
        #     render_screen = True
        if display and render_screen:
            console.print("\33[2J")
            console.print(render(screen, score))
            # print(f"score: {score}")
            render_screen = False
            #time.sleep(0.05)
            i = input()
    return score
if __name__ == "__main__":
    data = read_entire_input(2019,13)
    part_one(data)
    part_two(data)