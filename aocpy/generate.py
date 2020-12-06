from os import makedirs
from os.path import dirname, exists, join
from pathlib import Path
from shutil import copyfile
from typing import Iterable

from aocpy.exception import AocpyException


def generate_day(day: int, puzzle_input: Iterable[str]):
    solution_dirname = f"{day:02}"
    solution_fname = join(solution_dirname, "solution.py")

    if exists(solution_fname):
        raise AocpyException(f"day {day:02} already found")

    makedirs(solution_dirname, exist_ok=True)

    if Path(".aocpy/solution.py").exists():
        copyfile(str(Path(".aocpy/solution.py")), solution_fname)
    else:
        copyfile(join(dirname(__file__), "templates/solution.py"), solution_fname)

    test_fname = join(solution_dirname, f"test_day{solution_dirname}.py")
    if Path(".aocpy/test_solution.py").exists():
        copyfile(str(Path(".aocpy/test_solution.py")), test_fname)
    else:
        copyfile(join(dirname(__file__), "templates/test_solution.py"), test_fname)

    puzzle_input_fname = join(solution_dirname, "input.txt")
    with open(puzzle_input_fname, "w") as f:
        f.write(puzzle_input)
