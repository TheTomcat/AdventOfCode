import cProfile
import os
import pstats
import time
from typing import Callable, Dict, Any
from functools import wraps

from config import RUNNING_ALL
from framework.console import console
from framework.exceptions import SolutionNotFoundException
from framework.make_readme import load_module_times, put_result_in_nested_dict


# def _get_year_from_segment(segment: str) -> int:
#     if not segment.startswith('year_'):
#         raise ValueError(f'invalid year segment received: {segment}')

#     return int(segment[5:])


# def get_year_from_file(file: str):
#     """
#     Pass __file__ as parameter to get the year the file is in.

#     Should not be used outside of a year_* module
#     """
#     segments = os.path.dirname(os.path.realpath(file)).split(os.sep)
#     year_segment = segments[-1]
#     return _get_year_from_segment(year_segment)


def _get_prefix(year: int, day: int, part: int, version: str) -> str:
    if not day or not part:
        raise ValueError('incorrect values provided for solution timer')

    if version:
        version = f' [yellow]{version}[/yellow]'

    if RUNNING_ALL:
        prefix = f'[blue]  - day {day:02} part {part:02}[/blue]{version}: '
    else:
        prefix = f'[blue]{year} day {day:02} part {part:02}[/blue]{version}: '

    return prefix


def solution_timer(year: int, day: int, part: int, version: str = ''):  # noqa: C901, type: ignore
    prefix = _get_prefix(year, day, part, version)

    def decorator(func: Callable):  # type: ignore
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                start = time.perf_counter()
                solution = func(*args, **kwargs)

                if solution is None:
                    raise SolutionNotFoundException(year, day, part)

                diff = (time.perf_counter() - start) * 1000
                times, results = load_module_times()

                ## New Solution Identifier - not working :(
                # put_result_in_nested_dict(results, solution, year, day, part)
                # solution_description = ''
                # if results[year][day][part][solution] == 1:
                #     solution_description = f' - [red]New Solution[/red]'
                # console.print(f'{prefix}{solution} in {diff:.2f} ms{solution_description}')
                console.print(f'{prefix}{solution} in {diff:.2f} ms')
                
            except SolutionNotFoundException:
                console.print(f'{prefix}[red]solution not found[/red]')
            except (ValueError, ArithmeticError, TypeError):
                console.print_exception()
            else:
                return solution, diff

        return wrapper

    return decorator


def solution_profiler(year: int, day: int, part: int, version: str = '', stats_amount: int = 10,
                      sort='time'):# Literal['time', 'cumulative'] = 'time'):  # noqa: C901, type: ignore
    prefix = _get_prefix(year, day, part, version)

    def decorator(func: Callable):  # type: ignore
        @wraps(func)
        def wrapper(*args, **kwargs):
            with cProfile.Profile() as profiler:
                func(*args, **kwargs)

            stats = pstats.Stats(profiler)

            if sort == 'time':
                stats.sort_stats(pstats.SortKey.TIME)
            elif sort == 'cumulative':
                stats.sort_stats(pstats.SortKey.CUMULATIVE)
            else:
                raise ValueError('only "time" and "cumulative" are supported')

            stats.sort_stats(pstats.SortKey.TIME)
            console.print(f'{prefix} profiling')
            stats.print_stats(stats_amount)

        return wrapper

    return decorator


def memoize(func: Callable):  # type: ignore
    cache: Dict[Any, Any] = dict()

    def memoized_func(*args):
        if args in cache:
            return cache[args]

        result = func(*args)
        cache[args] = result
        return result

    return memoized_func
