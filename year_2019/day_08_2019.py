from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input
from util.shared import grouper

data = read_entire_input(2019,8)

def parse(data: List[str]) -> Any:
    return data[0]

def split_layers(chunk_size, pixels):
    for chunk in grouper(chunk_size, pixels):
        yield chunk

WIDTH = 25
HEIGHT = 6

def first(iterable, condition):
    "Return the first item in iterable that matches condition"
    return next((x for x in iterable if condition(x)), None)

@solution_timer(2019,8,1)
def part_one(data: List[str]):
    pixels = parse(data)
    output = []
    for chunk in split_layers(WIDTH*HEIGHT, pixels):
        output.append([chunk.count(i) for i in ['0','1','2']])
    os = sorted(output)
    return os[0][1] * os[0][2]

@solution_timer(2019,8,2)
def part_two(data: List[str]):
    pixels = parse(data)
    chunks = list(split_layers(WIDTH*HEIGHT, pixels))
    image = []
    non_transparent = lambda x: x!='2'
    for pixel in zip(*chunks):
        image.append(first(pixel,non_transparent))
    image = ''.join(image).replace("1",chr(9608)).replace("0", " ")
    image = '\n'.join([''.join(i) for i in grouper(WIDTH, image)])
    return '\n'+image

if __name__ == "__main__":
    data = read_entire_input(2019,8)
    part_one(data)
    part_two(data)
