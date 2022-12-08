from typing import List, Any, Tuple
from util.helpers import solution_timer
from util.input_helper import read_entire_input

from collections import defaultdict

data = read_entire_input(2022,7)
test = """$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k""".split("\n")
def parse(data: List[str]) -> Any:
    return data

def build_directory(shell_output):
    dirs = defaultdict(list) # path: contents. Contents can be either a list of 
    path = ['']
    for line in shell_output:
        if line.startswith("$ cd "):
            if line.endswith(".."):
                path.pop()
            elif line.endswith("/"):
                path = ['']
            else:
                path.append(line[5:])
        elif line.startswith("$ ls"):
            continue
        else:
            size, name = line.split(" ")
            if size != 'dir':
                size = int(size)
            dirs[tuple(path)].append((size, name))
    return dirs

def calculate_directory_size(dirs, path):
    total = 0
    to_parse = [path]
    while len(to_parse)>0:
        path = to_parse.pop()
        try:
            for s, name in dirs[path]:
                if s == 'dir':
                    to_parse.append(path + (name,))
                else:
                    total += s
        except KeyError as e:
            print(f"Unable to find path {path}. It does not exist.")
    return total

@solution_timer(2022,7,1)
def part_one(data: List[str]):
    shell_output = parse(data)
    directories = build_directory(shell_output)
    sizes = [(path, calculate_directory_size(directories, path)) for path in directories]
    return sum([size for path,size in sizes if size < 100000])

@solution_timer(2022,7,2)
def part_two(data: List[str]):
    shell_output = parse(data)
    directories = build_directory(shell_output)
    sizes = [(path, calculate_directory_size(directories, path)) for path in directories]
    total_space = 70000000
    required_space = 30000000
    sizes.sort(key=lambda x: x[1])
    used_space = sizes[-1][-1]
    free_space = total_space - used_space
    margin = required_space - free_space
    return next((s for p,s in sizes if s > margin), None)

if __name__ == "__main__":
    data = read_entire_input(2022,7)
    part_one(data)
    part_two(data)