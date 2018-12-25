import argparse
import os


def input_cli(base_dir):
    default_input = os.path.join(base_dir, "input.txt")
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    parser.add_argument(
        "infile",
        help="specify non-default puzzle input file",
        nargs="?",
        type=argparse.FileType(),
        default=default_input,
    )
    group.add_argument(
        "-e", "--example", help="use example_input.txt if present", action="store_true"
    )
    args = parser.parse_args()
    if args.example:
        with open(os.path.join(base_dir, "example_input.txt")) as f:
            return f
    else:
        return args.infile
