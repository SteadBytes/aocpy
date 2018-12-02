# aocpy - Advent of Code Automation Tool

Fetch input, submit answers and generate boilerplate files for solving Advent of Code puzzles :christmas_tree:

**Work in progress - API is likely to change**

## Usage

Please see the [Session Cookie Configuration](#session-cookie-configuration) section

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
$ aocpy begin 2017 15
```

### Submit Puzzle Answers

```bash
# submit answer for level 1 of today's puzzle
$ aocpy submit "myanswer" 1

# submit answer for level 2 of today's puzzle
$ aocpy submit "myanswer2" 2

# submit answer for level 1 of a specific puzzle
$ aocpy submit "myanswer" 1 2017 15

# submit answer for level 2 of a specific puzzle
$ aocpy submit "myanswer2" 2 2017 15
```

## Session Cookie Configuration

AoC puzzle inputs differ by user, requiring a browser cookie to determine the current user. `aocpy` requires this cookie and can be supplied in several ways:

- CLI `-c`/`--session-cookie` option (supported by all commands):
  - `$ aocpy begin -c <1234mycookie>`
- Configuration file:
  - Paste the cookie into a file at `~/.config/aocd/token`
  ```
  # ~/.config/aocd/token
  <1234mycookie>
  ```
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
