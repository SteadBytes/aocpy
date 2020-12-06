# aocpy - Advent of Code Automation Tool

[![PyPI version shields.io](https://img.shields.io/pypi/v/aocpy.svg)](https://pypi.python.org/pypi/aocpy/)

Fetch input, submit answers and generate boilerplate files for solving Advent of Code puzzles :christmas_tree:

## Installation

Install via pip:
`pip install aocpy`

## Usage

**N.B** Please see the [Session Cookie Configuration](#session-cookie-configuration) section

### Begin a Puzzle

`begin` fetches the puzzle input and generates boilerplate files with the following structure:

```
<day_number>/
  solution.py
  input.txt
```

```bash
# fetch input and generate boilerplate for today's challenge
$ aocpy begin

# fetch input and generate boilerplate for a specific puzzle
$ aocpy begin -y 2017 -d 15
$ aocpy begin -d 15 # uses current puzzle year
```

### Submit Puzzle Answers

```bash
# submit answer for level 1 of today's puzzle
$ aocpy submit "myanswer" 1

# submit answer for level 2 of today's puzzle
$ aocpy submit "myanswer2" 2

# submit answer for level 1 of a specific puzzle
$ aocpy submit "myanswer" 1 -y 2017 -d 15

# submit answer for level 2 of a specific puzzle
$ aocpy submit "myanswer2" 2 -y 2017 -d 15
```

### Running Solutions

The solution template files include a small CLI to read input files.

```bash
$ cd <puzzle_day_dir>

# Default - run with aocpy generated input.txt file
$ python solution.py

# Run with example_input.txt if present
$ python solution.py -e

# Run with specified input file
$ python solution.py /path/to/my/file.txt
```

## Session Cookie Configuration

AoC puzzle inputs differ by user, requiring a browser cookie to determine the current user. `aocpy` requires this cookie and can be supplied in several ways:

- CLI `-c`/`--session-cookie` option (supported by all commands):
  - `$ aocpy begin -c <1234mycookie>`
- Configuration file:
  - Paste the cookie into a file at `~/.config/aocpy/token`
      ```
      # ~/.config/aocpy/token
      <1234mycookie>
      ```
  - or set it via cli `aocpy set-cookie <1234mycookie>`
- Environment variable:
  - `$ export AOC_SESSION_COOKIE=<1234mycookie>`

### Finding Your Session Cookie

1. Open Advent of Code in a web browser and log in
2. Open the browser's developer console

- i.e. Right click -> Inspect or `F12`

3. Select the `Network` tab
4. Navigate to any puzzle input page i.e. adventofcode.com/2018/day/1/input
5. Click on the request that shows up in the `Network` tab
6. The cookie will be in the `Request Headers` section with the format `Cookie: session=<1234mycookie>`

## Use custom solution and test_solution templates

You can override the default templates in a `.aocpy` folder.

```
.
├── 01
│   ├── input.txt
│   ├── solution.py
│   └── test_solution.py
├── 02
│   ├── input.txt
│   ├── solution.py
│   └── test_solution.py
├── README.md
├── poetry.lock
├── pyproject.toml
├── tinker_regex.py
└── .aocpy
    ├── solution.py         # override solution template
    └── test_solution.py    # override test_solution template
```
