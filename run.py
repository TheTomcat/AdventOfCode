import sys
import os
from typing import List, Tuple, Union
from argparse import ArgumentParser
from util.input_helper import read_entire_input
from util.make_readme import append_new_run_times, _create_completed_text, generate_readme, _find_completed_days
from util.console import console
from config import ROOT_DIR

def run_day(year, day, test=False):#module: str, year: int, day: int):
    """
    Runs given days solution
    """
    
    console.print(f"[green]Attempting to run the solution to problem {day} from {year}...")
    try:
        module = __import__(f"year_{year}.day_{day:02}_{year}", fromlist=['object'])
    except ModuleNotFoundError as e:
        console.print(f"[red]There was no solution found for problem {day} from {year}")
        console.print(f"[yellow]Attempting to create template solution...")
        create_day(year, day)
        return
    if test:
        try:
            data = getattr(module, 'test')
        except AttributeError:
            console.print(f"[red]There was no test data found for problem {day} from {year}")
            return
    else:
        data = read_entire_input(year, day)
    
    try:
        r1, p1 = getattr(module, 'part_one')(data)
    except AttributeError:
        pass

    try:
        r2, p2 = getattr(module, 'part_two')(data)
    except AttributeError:
        pass

    if not test:
        append_new_run_times(r1,p1,r2,p2,day,year)
        # print(_create_completed_text())

        generate_readme() 
        # This will run the solution a second time if the solution is incomplete, which isn't a problem for short 
        # solutions but will be a problem for ones that take a long time.
        # I can't be bothered fixing this right now.

def run():
    year, day, test = _parse_args(sys.argv[1:])
    # if year is None:
    #     year_paths = get_full_year_paths()
    #     pass # run every problem - this will take a long time so alert the user?
    #     return
    # if day == '.':
        

    if day is not None:
        if day > 25:
            console.print(f"[red]I can't run the problem for {year}-{day} because {day}>25")
            return
        run_day(year, day, test)
    else:
        run_day(year, 1, test)
    
    
def create_day(year, day):
    console.print(f"[yellow]  Creating the solution file for year {year} day {day}.")
    
    module_path = os.path.join(ROOT_DIR)
    yeardir = os.path.join(ROOT_DIR,f"year_{year}")
    dayscript = os.path.join(yeardir, f"day_{day:02}_{year}.py")

    # does the year folder exist?
    
    if not os.path.exists(yeardir):
        console.print(f"[yellow]  Year directory for {year} not found, creating...")
        os.mkdir(yeardir)
    
    if os.path.exists(dayscript):
        console.print(f"[red]  The script for problem {day} of year {year} already exists.")
        return
    # the script does not exist, so copy the template into the directory
    console.print(f"[yellow]  Attempting to create solution template...", end="")
    try:
        with open("template/problem.py.txt", "r") as f:
            contents = f.read()
        contents = contents.replace("%YEAR%",f"{year}").replace("%DAY%",f"{day}")
        console.print(f"[green] solution template found, copying... ", end="")
    except Exception as e:
        console.print(f"[red]  Something went wrong...")
        raise e
    try:
        with open(dayscript,"w") as f:
            f.write(contents)
    except Exception as e:
        console.print(f"[red]  Something went wrong...")
        raise e
    console.print(f"[green]  Success!")
    return True

def opt_int(arg: Union[int,str]) -> Union[int,str]:
    if arg == ".":
        return arg
    return int(arg)

def _parse_args(args: List[str]) -> Tuple[int, int]:
    parser = ArgumentParser(description='Add a day')
    parser.add_argument('year', type=opt_int, help='The year of the exercise')
    parser.add_argument('day', type=opt_int, help='The day of the exercise', )
    parser.add_argument('-t', '--test', action='store_true')
    #parser.add_argument('quiet', type=int, help='Suppress errors', default=False)
    parsed = parser.parse_intermixed_args(args)
    return parsed.year, parsed.day, parsed.test#, parsed.quiet

if __name__=="__main__":
    run()
