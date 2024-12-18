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

class InvalidPartError(Exception):
    def __init__(self, part):
        super().__init__(f"There is no part {part}. Part must be 1 or 2")

class InvalidDayError(Exception):
    def __init__(self, message):
        super().__init__(message)

class DataNotFoundError(Exception):
    def __init__(self, test_data):
        super().__init__(f"Unable to load {'test ' if test_data else '' }data from file.")

class UnraisableError(Exception):
    def __init__(self):
        super().__init__("Unraisable error")