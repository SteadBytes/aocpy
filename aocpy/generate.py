from os import makedirs
from os.path import dirname, exists, join
from shutil import copyfile

from aocpy.puzzle import Puzzle


def generate_day(puzzle: Puzzle):
    solution_dirname = f"{puzzle.day:02}"
    solution_fname = join(solution_dirname, "solution.py")

    if exists(solution_fname):
        raise Exception(f"day {puzzle.day:02} already found")

    makedirs(solution_dirname, exist_ok=True)

    copyfile(join(dirname(__file__), "templates/solution.py"), solution_fname)

    puzzle_input_fname = join(solution_dirname, "input.txt")
    with open(puzzle_input_fname, "w") as f:
        f.write(puzzle.puzzle_input)
