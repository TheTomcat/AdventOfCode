import os, sys
import re
import pickle
import importlib.util
import datetime
from typing import Dict, List

from config import ROOT_DIR
from framework.console import nostdout
from framework.input_helper import read_entire_input

def store_nested_dict(dictionary, value, *keys):
    val = dictionary
    for key in keys[:-1]:
        try:
            val = val[key]
        except KeyError as e:
            val[key] = {}
            val = val[key]
    val[keys[-1]] = value
    return dictionary

def generate_readme():
    path = os.path.join(ROOT_DIR, 'README.md')
    readme_file = os.path.abspath(path)

    with open(readme_file, encoding="utf8") as f:
        current_readme = f.read()
    
    completed_days = _find_completed_days()
    
    readme = _replace_between_tags(
        current_readme,
        _create_completed_text(),
        '<!-- start completed section -->',
        '<!-- end completed section -->'
    )

    readme = _replace_between_tags(
        readme,
        f"Last updated {datetime.datetime.now().strftime('%H:%M on %A %d %B, %Y')}",
        '<!-- Last updated -->',
        '<!-- End last updated -->'
    )

    readme = _update_stars(readme)

    with open(readme_file, 'w', encoding="utf8") as f:
        f.write(readme)

def get_module_time_path():
    return os.path.join(ROOT_DIR, 'times.pickle')

def load_module_times() -> Dict:
    path = get_module_time_path()
    try:
        with open(path, 'rb') as f:
            times = pickle.loads(f.read())
        return times
    except (EOFError, FileNotFoundError) as e:
        return {}

def store_module_times(times):
    path = get_module_time_path()
    with open(path, 'wb') as f:
        f.write(pickle.dumps(times))

def _replace_between_tags(readme: str, content: str, start: str, end: str) -> str:
    content = '\n'.join([start, content, end])

    return re.sub(
        pattern=rf'{start}.*?{end}',
        repl=content,
        string=readme,
        flags=re.DOTALL,
    )


def _update_stars(readme: str) -> str:
    star_count = _count_stars()

    return re.sub(
        pattern=r'&message=\d+',
        repl=f'&message={star_count}',
        string=readme,
        flags=re.DOTALL,
    )

def _count_stars() -> int:
    found = _find_completed_days()
    return sum([1 for days in found.values() for parts in days.values() for val in parts.values()])


def _create_completed_text() -> str:
    found = _find_completed_days()

    text = ['## Completed ⭐️']
    for year, days in found.items():
        text.append(f'\n### {year}\n')

        for day, parts in days.items():
            part_one_star = '⭐️' if parts and 1 in parts and parts[1] else ' - '
            part_two_star = '⭐️' if parts and 2 in parts and parts[2] else ' - '
            part_one_time = f'\n  - part one: {parts[1]:.3f}ms' if part_one_star != " - " else ""
            part_two_time = f'\n  - part two: {parts[2]:.3f}ms' if part_two_star != " - " else ""
            text.append(f'- day {day:02}: {part_one_star} {part_two_star}{part_one_time}{part_two_time}')

    text.append('')
    return '\n'.join(text)

def append_new_run_times(ret1, time1, ret2, time2, day, year):
    times = load_module_times()
    changed=False
    if ret1:
        store_nested_dict(times, time1, year, day, 1)
        changed=True
    if ret2:
        store_nested_dict(times, time2, year, day, 2)
        changed=True
    if changed:
        store_module_times(times)

def get_full_year_paths() -> List[str]:
    """
    Retrieves all directories in the ROOT_DIR that start with 'year_'
    """
    paths = [os.path.join(ROOT_DIR, val) for val in os.listdir(ROOT_DIR) if val.startswith('year_')]
    return sorted(paths, reverse=True)

def get_full_day_paths(year_path: str) -> List[str]:
    """
    Retrieves all files in the ROOT_DIR/year_{year} directory that start with 'day_'
    """
    paths = [os.path.join(year_path, val) for val in os.listdir(year_path) if val.startswith('day_')]
    return sorted(paths)

def get_year_and_day_from_day_path(day_path: str) -> tuple[int]:
    # print(day_path)
    # day_path = day_path.split(os.sep)[0]
    return int(day_path.split("_")[-1][:-3]), int(day_path.split("_")[-2])

def get_module(year: int, day: int): 
    "Return the module corresponding to a particular year and day"
    module_name = f"day_{day:02}_{year}"
    module_path = os.path.join(ROOT_DIR, f'year_{year}', module_name+".py")
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def time_module(module, year, day):
    with nostdout():
        try:
            r1, p1 = module.part_one(module.data)
        except AttributeError:
            p1=None
            r1=False
        try:
            r2, p2 = module.part_two(module.data)
        except AttributeError:
            p2=None
            r2=False
    
    # r1, p1 = module.part_one(read_entire_input(year, day))
    # r2, p2 = module.part_two(read_entire_input(year, day))
    p1 = p1 if r1 else r1
    p2 = p2 if r2 else r2
    return p1, p2

def _find_completed_days(rerun=None):
    items = {}
    saved_times = load_module_times()
    changed = False
    for year_path in get_full_year_paths():
        # print(f'{year_path}: ',end="")
        year = int(year_path.split(os.sep)[-1][len('year_'):])
        items[year] = {}

        for day_file in get_full_day_paths(year_path):
            
            day = int(day_file.split("_")[-2])
            items[year][day] = {}

            try:
                p1 = saved_times[year][day][1]
            except KeyError as e:
                p1=None
            try:
                p2 = saved_times[year][day][2]
            except KeyError as e:
                p2 = None

            if False: # THIS CODE MIGHT NOT BE NECESSARY? 
                if p1 is None or p2 is None or rerun is True or (rerun and (year,day) in rerun):
                    module = get_module(year, day)
                    p1, p2 = time_module(module, year, day)
                    changed = True

            # print(f"{day}, ",end="")
            # print(p1,p2)
            if p1:
                items[year][day][1] = p1
            if p2:
                items[year][day][2] = p2
    if changed:
        store_module_times(items)
    return items