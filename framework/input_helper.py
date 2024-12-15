import os
from typing import List
import requests

def get_input(year: int, day: int) -> None:
    "Reads the input from adventofcode.com and stores it to a file"    
    session = _read_session()
    data = _download_input(year, day, session)
    _save_input(data, year, day)

def _download_input(year: int, day: int, session: str) -> bytes:
    """
    Downloads the input as text from the advent of code site
    """
    cookies = {'session': session}
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    resp = requests.get(url, cookies=cookies)
    #try:
    resp.raise_for_status()
    #except HTTPError as e:

    return resp.content  # type: ignore

def _read_session() -> str:
    # target = os.path.join(ROOT_DIR, '.session')
    path = os.path.abspath('.session')
    with open(path) as f:
        return f.read()

def _save_input(data: bytes, year: int, day: int) -> None:
    inputs_path = os.path.join('inputs')
    year_path = os.path.join(inputs_path, str(year))
    if not os.path.exists(year_path):
        os.mkdir(year_path)

    with open(os.path.join(year_path, f'day_{day:02}.txt'), 'wb') as file:
        file.write(data)
def _build_problem_path(year: int, day: int):
    inputs_path = os.path.join('inputs')
    year_path = os.path.join(inputs_path, str(year))
    problem_path = os.path.join(year_path, f'day_{day:02}.txt')
    return problem_path

def read_input(i):
    print("depreciated. Please use read_input_by_line")
    with open(f'2020/{i}/input.txt', 'r') as f:
        for line in f:
            yield line

def read_input_by_line(year: int, day: int):
    problem_path = _build_problem_path(year, day)
    if not os.path.exists(problem_path):
        get_input(year, day)
    with open(problem_path, 'r') as f:
        for line in f:
            yield line[:-1]

def read_entire_input(year: int, day: int) -> List[str]:
    """Reads the file corresponding to the problem specified. If it does not exist, attempt to download it.
    Output is a list of strings, each one line of the file.
    """
    problem_path = _build_problem_path(year, day)
    if not os.path.exists(problem_path):
        get_input(year, day)
    with open(problem_path, 'r') as f:
        data = f.read().splitlines()
        return data
    
def read_entire_input_str(year: int, day: int) -> str:
    """Reads the file corresponding to the problem specified. If it does not exist, attempt to download it.
    Output is a string containing the whole input.
    """
    problem_path = _build_problem_path(year, day)
    if not os.path.exists(problem_path):
        get_input(year, day)
    with open(problem_path, 'r') as f:
        data = f.read()
        return data