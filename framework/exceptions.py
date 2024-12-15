class SolutionNotFoundException(Exception):
    def __init__(self, year: int, day: int, part: int):
        message = f'solution not found for {year} day {day:02} part {part}'
        super().__init__(message)

class SolutionFileAlreadyExistsError(Exception):
    def __init__(self, year: int, day: int, version: str = ""):
        message = f'solution file already exists {year=} {day=} {version=}'
        super().__init__(message)

class ModuleVersionError(Exception):
    def __init__(self):
        message = f"Cannot use version 2 solver on a version 1 problem. Remove decorator and add '__version__ = 2'" 
        super().__init__(message)

class ModuleVersionAlreadyOKError(Exception):
    def __init__(self, version):
        super().__init__(f"The solution file appears to already be version {version}")