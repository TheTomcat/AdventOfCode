from contextlib import contextmanager
import importlib.util
import pickle
import re
import sys
import time
from types import ModuleType
from typing import Annotated, Literal, Optional, TypedDict
import typer
import os
import glob

from framework.console import console
from config import ROOT_DIR, STORAGE_OBJ_PATH, TEMPLATE_PATH
from framework.exceptions import DataNotFoundError, InvalidDayError, InvalidPartError, ModuleVersionAlreadyOKError, ModuleVersionError, SolutionFileAlreadyExistsError, UnraisableError

app = typer.Typer()

def _get_prefix(year: int, day: int, part: int, version: str) -> str:
    # if not day or not part:
    #     raise ValueError('incorrect values provided for solution timer')

    if version:
        version = f' [yellow]{version}[/yellow]'
    else:
        version = ""

    if False: #RUNNING_ALL:
        prefix = f'[blue]  - day {day:02} part {part:02}[/blue]{version}: '
    else:
        prefix = f'[blue]{year} day {day:02} part {part:02}[/blue]{version}: '

    return prefix

def _handle_version(version: Optional[str]) -> Optional[str]:
    if version is None:
        return None
    if version == 'default':
        return None
    return version

############# COMMANDS

@app.command()
def show_versions(year: Annotated[int, typer.Argument(help="The year to search")], 
                  day: Annotated[int, typer.Argument(help="The day to search")]
                  ):
    versions = get_all_versions(year, day)
    console.print(f"[yellow]Showing {len(versions)} solution version(s) for {year=} {day=}[/yellow]")
    for i, a in enumerate(versions):
        console.print(f"  [{i}] {a[2] if a[2] is not None else 'default'}")
        # print([ for a in versions])
    x = console.input("Run solution: ") 
    if x.isdigit():
        console.print("Attempting to run solution...")
    else:
        console.print("Exiting.")

@app.command()
def create_day(year: Annotated[int, typer.Argument(help="The year to create")], 
               day: Annotated[int, typer.Argument(help="The day to create")],
               version: Annotated[str, typer.Option(help="The version to create. Specify '.' to autogenerate an autoincremented version")] = None
               ):
    
    version = _handle_version(version)
    if version == '.':
        version = get_next_version(year, day)
    try:
        console.print(f"[yellow]Attempting to create solution file for {year=} {day=} {version=}[/yellow]")
        _create_day(year, day, version)

    except SolutionFileAlreadyExistsError as e:
        day_path = build_day_path(year, day, version)
        console.print(f"   [red]The file [blue]{day_path}[/blue] already exists. \n   Try specifying a unique version, or use '.' to autoincrement a new version. [/red]")
        raise typer.Exit()
    
@app.command()
def run(year: Annotated[int, typer.Argument(help="The year to run")], 
        day: Annotated[int, typer.Argument(help="The day to run")] = None, 
        part: Annotated[int, typer.Option(help="The part to run. Omit or set as 0 to run both parts")] = 0, 
        version: Annotated[str, typer.Option(help="The version to run.")] = None,
        verbose: Annotated[bool, typer.Option("--verbose", "-v", help="Verbose output")] = False,
        test: Annotated[bool, typer.Option("--test","-t", help="Use test data rather than the full input.")] = False,
        error: Annotated[bool, typer.Option("--suppress-errror", "-e", help="Suppress error messages")] = False
        # log_results: bool = False
        ):
    # part = None if part == 0 else part
    parts = [1,2] if part == 0 else [part]
    days = get_all_days(year) if day is None else [day]
#     try:
#         results = time_solution(year, day, part=part, version=version, as_test=test, verbose=verbose)
#     except ModuleVersionError:
#         console.print("""[red]Cannot run a version 1 problem in the version 2 solver. Either use the version 1 solver, or modify the solution file by:
#    1. Removing or commenting out the @solution_timer() decorators from each 'part' function
#    2. Adding '__version__ = 2' to the top of the file.[/red]""")
#         raise typer.Exit()
#     except FileNotFoundError:
#         console.print(f"[red]There was no solution found for problem {day} from {year}[/red]")
#         console.print(f"[yellow]Attempting to create template solution...[/yellow]")
#         _create_day(year, day)
#         raise typer.Exit()
    
    with storage_obj() as obj:
        # for part, (solution, time) in enumerate(results):
        for day in days:
            for part in parts:
                prefix = _get_prefix(year, day, part, version)
                console.print(f"{prefix}", end="")
                errorcatch = Exception if error else UnraisableError
                try:
                    solution, runtime = time_solution_part(year, day, part=part, version=version, as_test=test, verbose=verbose)
                except ModuleVersionError:
                    console.print("[red]Cannot run a version 1 problem in the version 2 solver. Either use the version 1 solver, or modify the solution file by:\n" + 
                                "1. Removing or commenting out the @solution_timer() decorators from each 'part' function\n" +
                                "2. Adding '__version__ = 2' to the top of the file.[/red]")
                    raise typer.Exit()
                except FileNotFoundError:
                    console.print(f"[red]There was no solution found for problem {day} from {year}[/red]")
                    console.print(f"[yellow]Attempting to create template solution...[/yellow]")
                    _create_day(year, day)
                    raise typer.Exit()
                except DataNotFoundError:
                    console.print(f"[red]Unable to load {'test ' if test else '' }data from file.[/red]")
                    raise typer.Exit()
                except KeyboardInterrupt:
                    cmd = console.input("[red]Halted[/red] - [yellow][A]bort test run, [S]kip this file: [/yellow]")
                    if cmd in ['A','a', '']:
                        console.print("[red]   Aborting.[/red]")
                        raise typer.Exit()
                    # console.print("[purple] Skipping file[/purple]")
                    continue
                except errorcatch as e:
                    console.print(f"[red]Error! Run without -e flag for details[/red]")
                    raise typer.Exit()

                
                if not solution:
                    console.print(f'No solution found.')
                    continue
                result_count = check_result(obj, solution, year, day, part, test)
                disp = f" - [red]New Solution![/red]" if not result_count else f" - Solution obtained {result_count} time(s) before"
                console.print(f'{solution} in {runtime:.2f} ms{disp}', end="")
                store_time(obj, runtime, year, day, part, version)
                if test:
                    console.print("")
                elif not has_star(obj, year, day, part):
                    to_star = console.input(" [yellow]Add a :star:? [/yellow]")
                    if to_star in ['Y','y']:
                        add_star(obj, year, day, part)
                else:
                    console.print(" :star:")
    # log_results(year, day, results)

@app.command()
def star(year: Annotated[int, typer.Argument(help="The year to star")], 
        day: Annotated[int, typer.Argument(help="The day to star")], 
        part: Annotated[int, typer.Option(help="The part to star. Omit or set as 0 to star both parts")] = 0,
        unstar: Annotated[bool, typer.Option("--unstar", "-u", help="Flag to remove star instead")] = False
        ):
    if part == 0:
        parts = [1,2]
    elif part == 1 or part == 2:
        parts = [part]
    else:
        console.print(f"[red]Invalid part {part}. Must be 0, 1 or 2. 0 for both parts 1 and 2[/red]")
        raise typer.Exit()
    with storage_obj() as obj:
        for part in parts:
            if unstar:
                console.print(f"   [red]Removing :star: from {year}-{day} part {part}[/red]")
                remove_star(obj, year, day, part)
            else:
                console.print(f"   [green]Adding :star: to {year}-{day} part {part}![/green]")
                add_star(obj, year, day, part)

@app.command()
def clear_results(year: Annotated[int, typer.Argument(help="The year to reset the results")], 
                  day: Annotated[int, typer.Argument(help="The day to reset the results")], 
                  part: Annotated[int, typer.Argument(help="The part to reset the results")],
                  test: Annotated[bool, typer.Option("--test","-t",help="Clear test results")] = False,
                  unstar: Annotated[bool, typer.Option("--unstar", "-u", help="Also unstar the problem")] = False):
    with storage_obj() as obj:
        reset_result(obj, year, day, part, test)
        msg = ""
        if unstar:
            remove_star(obj, year, day, part)
            msg = " [red]Star Removed. [/red]"
        console.print(f"[yellow]Resetting reuslt array for {year=} {day=} {part=} {'(test)' if test else ''}[/yellow]{msg}")
        
    

@app.command()
def status(year: Annotated[int, typer.Argument(help="The year to star")] = None, 
        day: Annotated[int, typer.Argument(help="The day to star")] = None, 
        part: Annotated[int, typer.Argument(help="The part to star. Omit or set as 0 to star both parts")] = 0):
    
    years = get_all_years() if year is None else [year]
    day_input = day
    part_input = part
    with storage_obj() as obj:
        # print(years)
        for year in years:
            console.print(f"Year {year}")
            days = get_all_days(year) if day_input is None else [day_input]
            for day in days:
                stars_got = has_star(obj, year, day, 1) + has_star(obj, year, day, 2)
                if stars_got == 0: # No stars got, but solution file exists
                    output = f"   - Day {day:02} - -"
                    part_one_time = f'\n     - part one: No solution'
                    part_two_time = f'\n     - part two: No solution'
                if stars_got >= 1: # Correct solution for 1 but not yet for 2
                    output  = f"   - Day {day:02} :star2: -"
                    part_one_time = f'\n     - part one: {fetch_time(obj, year, day, 1):.3f}ms' if has_star(obj, year, day, 1) else ""
                    part_two_time = f'\n     - part two: No solution'
                if stars_got == 2: # All solutions
                    output  = f"   - Day {day:02} :star2: :star2:"
                    part_two_time = f'\n     - part two: {fetch_time(obj, year, day, 2):.3f}ms' if has_star(obj, year, day, 2) else ""

                # parts = [1,2] if part_input == 0 else [part_input]
                # stars = " ".join(":star2:" if has_star(obj, year, day, part) else " " for part in parts)
                # for part in parts:
                # console.print(f"   - Day {day:02} {stars}{part_one_time}{part_two_time}")
                console.print(f'{output}{part_one_time}{part_two_time}')
            

@app.command()
def convert(year: Annotated[int, typer.Argument(help="The year to convert")], 
        day: Annotated[int, typer.Argument(help="The day to convert. Put year as 0 to convert all.")] = None, 
        version: Annotated[str, typer.Option(help="The version to convert.")] = None,
        overwrite: Annotated[bool, typer.Option(help="Overwrite the old version file")] = False):
    if day is None:
        days = get_all_days(year)
        prompt = console.input(f"Batch convert all {len(days)} solution files for year {year} to version 2 (y/[bold]N[/bold])?")
        if prompt not in ['Y','y']:
            # print(prompt)
            raise typer.Exit()
        for day in days:
            day_path = build_day_path(year, day, version)
            try:
                _convert(day_path, day_path)
            except ModuleVersionAlreadyOKError:
                console.print(f"   [red]Day {day} already version 2[/red]")
                continue
            console.print(f"   [green]Converted day {day}[/green]")
        raise typer.Exit()
    
    day_path = build_day_path(year, day, version)
    if not overwrite:
        new_version = get_next_version(year, day)
        new_day_path = build_day_path(year, day, new_version)
    else:
        new_version = version
        new_day_path = day_path
    console.print(f"[yellow]Attempting to update solution {year=} {day=} {version=} and storing into {new_version=}[/yellow]")
    if overwrite:
        response = console.input("[red]This may mangle your file. Are you sure you want to continue (y/[bold]N[/bold])? ")
        if response not in ['y', 'Y']:
            console.print("[red]Aborting.[/red]")
            raise typer.Exit()
    try:
        success = _convert(day_path, new_day_path)
    except ModuleVersionAlreadyOKError:
        console.print("[red]This solution file already appears to be valid for version 2. Aborting.[/red]")
        raise typer.Exit()
    if success:
        console.print("[green]...Success![/green]")
            
def _convert(from_path: str, to_path: str) -> bool:
    output = ""
    with open(from_path, "r") as f:
            output += '"""Autogenerated solution template, v2"""\n__version__ = 2\n\n'
            for line in f.readlines():
                if line.startswith("__version__") and int(line.split("=")[-1]) == 2:
                    raise ModuleVersionAlreadyOKError(2)
                if line.startswith("@solution"):
                    line = f"#{line}"
                output += line
    with open(to_path, 'w') as g:
        g.write(output)

#################### HELPERS

def _create_day(year: int, day: int, version: Optional[str] = None):
    # console.print(f"[yellow]  Creating the solution file for {year=} day {day=}.")
    if not 0 < day < 25:
        raise InvalidDayError("Day must be between 1 and 25")
    year_path = build_year_path(year)
    day_path = build_day_path(year, day, version)
    # does the year folder exist?
    
    if not os.path.exists(year_path):
        console.print(f"[yellow]  Year directory for {year} not found, creating...")
        os.mkdir(year_path)
    
    if os.path.exists(day_path):
        raise SolutionFileAlreadyExistsError(year, day, version)
    
    # the script does not exist, so copy the template into the directory
    console.print(f"[yellow]  Attempting to create solution template...", end="")
    try:
        with open(TEMPLATE_PATH, "r") as f:
            contents = f.read()
        contents = contents.replace("%YEAR%",f"{year}").replace("%DAY%",f"{day}").replace("%VERSION%", f'{version}')
        console.print(f"[green] solution template found, copying... ", end="")
    except Exception as e:
        console.print(f"[red]  Something went wrong...")
        raise e
    try:
        with open(day_path,"w") as f:
            f.write(contents)
    except Exception as e:
        console.print(f"[red]  Something went wrong...")
        raise e
    console.print(f"[green]  Success!")
    return True


############## Path functions

def get_full_year_paths() -> list[str]:
    """
    Retrieves all directories in the ROOT_DIR that start with 'year_'
    """
    paths = [os.path.join(ROOT_DIR, val) for val in os.listdir(ROOT_DIR) if val.startswith('year_')]
    return sorted(paths, reverse=True)

def get_full_day_paths(year_path: str) -> list[str]:
    """
    Retrieves all files in the ROOT_DIR/year_{year} directory that start with 'day_'
    """
    paths = [os.path.join(year_path, val) for val in os.listdir(year_path) if val.startswith('day_')]
    return sorted(paths)

def get_all_years() -> list[int]:
    """Return a list of all the available years, in reverse order"""
    return [int(val.split("_")[-1]) for val in sorted(os.listdir(ROOT_DIR), reverse=True) if val.startswith('year_')]

def get_all_days(year: int) -> list[int]:
    "Return a list of all days within a year"
    year_path = build_year_path(year)
    days = list(set(int(a.split("_")[1]) for a in os.listdir(year_path) if a.startswith("day_")))
    return days

def get_all_versions(year: int, day: int) -> list[tuple[int,int,Optional[str]]]:
    """Given a year and a day, return a dict of day_paths"""
    base_day = build_day_path(year,day)
    p1 = base_day.split(".")[0]
    files = glob.glob(f"{p1}*")
    return [get_identifiers_from_path(path) for path in files]

def get_next_version(year: int, day: int) -> str:
    "Find the solution files associated with (year, day) and autogenerate a new version number"
    versions: list[str] = [a[2] for a in get_all_versions(year, day)]
    version_numbers = [int(a) for a in versions if a is not None and a.isdigit()]
    if version_numbers == []:
        return "01"
    return f"{max(version_numbers) + 1:02}"

def build_year_path(year: int, create_if_not_exists: bool = True) -> str:
    "Given a year, return the path to the directory for that year"
    directory = f"year_{year}"
    full_directory = os.path.join(ROOT_DIR, directory)
    if not os.path.isdir(full_directory) and create_if_not_exists:
        raise NotImplementedError
        ...
    return full_directory

def build_day_path(year: int, day: int, version: Optional[str] = None, create_if_not_exists: bool = True) -> str:
    """Given a year, day and optionally a version, return the path to that solution module.
    NOTE: There is no guarantee that the file exists, however"""
    year_path = build_year_path(year)
    fversion = f"_{version}" if version is not None else ""
    day_file = f"day_{day:02}_{year}{fversion}.py"
    full_path = os.path.join(year_path, day_file)
    # if not os.path.exists(full_path) and create_if_not_exists:
    #     raise NotImplementedError(f"No file found for solution {year=} {day=} {version=}")
    return full_path

def build_all_day_paths(year: int):
    """
    Retrieves all files in the ROOT_DIR/year_{year} directory that start with 'day_'
    """
    year_path = build_year_path(year)
    paths = [os.path.join(year_path, val) for val in os.listdir(year_path) if val.startswith('day_')]
    return sorted(paths)

def get_identifiers_from_path(day_path: str) -> tuple[int,int,int]:
    "Given a path to a problem file, extract the year, day and version (if exists)"
    # Split path at "_"
    bits = day_path.split(os.sep)[-1].split("_")
    if len(bits) == 3:
        return int(bits[-1][:-3]), int(bits[-2]), None
    elif len(bits) == 4:
        return int(bits[-2]), int(bits[-3]), bits[-1][:-3]
    raise FileNotFoundError(f"{day_path} is an invalid path for a solution module")

########## Database functions

Result = int
Version = str
class StorageObj(TypedDict):
    results: dict[tuple[int,int,int,int], dict[Result, int]]
    times: dict[tuple[int,int,int,Version], int]
    stars: set[tuple[int,int,int]]

def get_module_storage_path():
    return STORAGE_OBJ_PATH # os.path.join(ROOT_DIR, 'db.pickle')

def get_module_storage() -> StorageObj:
    try:
        with open(get_module_storage_path(), 'rb') as f:
            obj: StorageObj = pickle.loads(f.read())
        return obj
    except (EOFError, FileNotFoundError) as e:
        return {
            'results': {},
            'times': {},
            'stars': set()
        }

def save_module_storage(obj: StorageObj):
    path = get_module_storage_path()
    with open(path, 'wb') as f:
        f.write(pickle.dumps(obj))

def add_star(obj: StorageObj, year: int, day: int, part: int):
    obj['stars'].add((year,day,part))
def remove_star(obj:StorageObj, year: int, day: int, part: int):
    obj['stars'].remove((year, day, part))
def has_star(obj: StorageObj, year: int, day: int, part: int) -> bool:
    return (year, day, part) in obj['stars']

def store_time(obj: StorageObj, time: float, year: int, day: int, part: int, version: Version = None):
    if version:
        p = (year, day, part, version)
    else:
        p = (year, day, part)
    obj['times'][p] = time

def fetch_time(obj: StorageObj, year: int, day: int, part: int, version: Version = None) -> float:
    if version:
        p = (year, day, part, version)
    else:
        p = (year, day, part)
    return obj['times'][p]

@contextmanager
def storage_obj():
    try:
        obj = get_module_storage()
        yield obj
    finally:
        save_module_storage(obj)
        
def check_result(obj: StorageObj, result: Result, year: int, day: int, part: int, test: bool) -> int:
    "Check to see if a solution has been obtained before. Return the number of times it has happened (not including this one)"
    iden = (year, day, part, test)
    if iden in obj['results']:
        results = obj['results'][iden]
        if result in results:
            results[result] += 1
            return results[result] - 1
        results[result] = 1
        return results[result] - 1
    else:
        obj['results'][iden] = {result:1}
        return obj['results'][iden][result] - 1
    
def reset_result(obj: StorageObj, year: int, day: int, part: int, test: int):
    iden = (year, day, part, test)
    if iden in obj['results']:
        obj['results'][iden] = {}


##################################

def load_module(year: int, day: int, version: Version=None)-> ModuleType: 
    "Return the module corresponding to a particular year and day"
    module_name = f"day_{day:02}_{year}"
    # module_path = os.path.join(ROOT_DIR, f'year_{year}', module_name+".py")
    
    module_path = build_day_path(year, day, version)
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[module_name] = module
    spec.loader.exec_module(module)
    return module

def time_solution(year: int, day: int, *,version:Optional[Version]=None, part: Optional[int] = None, as_test: Optional[bool] = False, verbose: bool = False):
    module = load_module(year, day, version)
    try:
        if module.__version__ != 2:
            raise ModuleVersionError()
    except AttributeError:
        raise ModuleVersionError()
    if as_test:
        data = module.test
    else:
        data = module.data
    p1, diff1, p2, diff2 = None, None, None, None
    if part is None or part == 1:
        try:
            start = time.perf_counter()
            p1 = module.part_one(data, verbose=verbose)
            end = time.perf_counter()
            diff1 = (end-start)*1000
        except AttributeError:
            p1 = None
            diff1 = None
    if part is None or part == 2:
        try:
            start = time.perf_counter()
            p2 = module.part_two(data, verbose=verbose)
            end = time.perf_counter()
            diff2 = (end-start)*1000
        except AttributeError:
            p2 = None
            diff2 = None
    return (p1, diff1), (p2, diff2)

def time_solution_part(year: int, day: int, part: int, *,version:Optional[Version]=None, as_test: Optional[bool] = False, verbose: bool = False):
    module = load_module(year, day, version)
    try:
        if module.__version__ != 2:
            raise ModuleVersionError()
    except AttributeError:
        raise ModuleVersionError()
    try:
        if as_test:
            data = module.test
        else:
            data = module.data
    except AttributeError:
        raise DataNotFoundError(as_test)
    
    if part != 1 and part != 2:
        raise InvalidPartError(part)
    try:
        start = time.perf_counter()
        if part == 1:
            result = module.part_one(data, verbose=verbose)
        elif part == 2:
            result = module.part_two(data, verbose=verbose)
        end = time.perf_counter()
        runtime = (end-start)*1000
    except AttributeError:
        result = None
        runtime = None
    
    return result, runtime
    
if __name__ == "__main__":
    # typer.run(run)
    app()
