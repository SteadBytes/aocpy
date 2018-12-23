def part_1():
    pass


def part_2():
    pass


def main(puzzle_input_f):
    lines = puzzle_input_f.readlines()
    print("Part 1: ", part_1())
    print("Part 2: ", part_2())


if __name__ == "__main__":
    import os

    base_dir = os.path.dirname(__file__)
    with open(os.path.join(base_dir, "input.txt")) as f:
        main(f)
