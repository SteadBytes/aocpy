import contextlib
from datetime import datetime

import pytest
import pytz
from click.testing import CliRunner
from freezegun import freeze_time

from aocpy.cli import cli

from pathlib import Path
from hypothesis import strategies as st, given


class Runner(CliRunner):
    @contextlib.contextmanager
    def isolated_filesystem(self):
        with super().isolated_filesystem() as f:
            yield Path(f)


@pytest.fixture
def webbrowser_open(mocker):
    return mocker.patch("webbrowser.open")


@pytest.fixture
def home_dir(tmp_path):
    d = tmp_path / "home/steadbytes"
    d.mkdir(parents=True)
    return d


@pytest.fixture
def config_dir(home_dir):
    d = home_dir / ".config/aocd"
    d.mkdir(parents=True)
    return d


@pytest.fixture
def runner(home_dir):
    return Runner(env={"HOME": str(home_dir)})


@freeze_time(datetime(2019, 12, 10, hour=1, tzinfo=pytz.timezone("America/New_York")))
def test_begin(webbrowser_open, runner, config_dir, responses):
    puzzle_url = "https://adventofcode.com/2019/day/10"
    puzzle_input = "some text"
    responses.add(responses.GET, puzzle_url + "/input", body=puzzle_input)
    cookie = "12345"
    with runner.isolated_filesystem() as p:
        result = runner.invoke(cli, ["begin", "-c", cookie])
        assert result.exit_code == 0
        # Puzzle files generated
        assert (p / "10/input.txt").exists()
        assert (p / "10/solution.py").exists()
        # Input is cached
        assert (config_dir / cookie / "2019/10.txt").exists()
        # Browser opened to today's puzzle URL
        webbrowser_open.assert_called_once_with(puzzle_url)


@pytest.mark.parametrize("day", range(26, 32))
def test_begin_uses_day_25_as_max(day, webbrowser_open, runner, config_dir, responses):
    puzzle_url = "https://adventofcode.com/2019/day/25"
    puzzle_input = "some text"
    responses.add(responses.GET, puzzle_url + "/input", body=puzzle_input)
    cookie = "12345"
    with freeze_time(datetime(2019, 12, day)):
        with runner.isolated_filesystem() as p:
            result = runner.invoke(cli, ["begin", "-c", cookie])
            assert result.exit_code == 0
            # Puzzle files generated
            assert (p / "25/input.txt").exists()
            assert (p / "25/solution.py").exists()
            # Input is cached
            assert (config_dir / cookie / "2019/25.txt").exists()
            # Browser opened to today's puzzle URL
            webbrowser_open.assert_called_once_with(puzzle_url)


@pytest.mark.parametrize("month", list(range(1, 12)))
def test_begin_fails_if_not_december(
    month, webbrowser_open, runner, config_dir, responses
):
    cookie = "1234"
    with freeze_time(datetime(2019, month, 10)):
        with runner.isolated_filesystem():
            result = runner.invoke(cli, ["begin", "-c", cookie])
            assert result.exit_code == 1


@freeze_time(datetime(2019, 12, 25, hour=1, tzinfo=pytz.timezone("America/New_York")))
@pytest.mark.parametrize("day", range(1, 25))
def test_begin_specify_day(day, webbrowser_open, runner, config_dir, responses):
    puzzle_url = f"https://adventofcode.com/2019/day/{day}"
    puzzle_input = "some text"
    responses.add(responses.GET, puzzle_url + "/input", body=puzzle_input)
    cookie = "12345"
    with runner.isolated_filesystem() as p:
        result = runner.invoke(cli, ["begin", "-d", day, "-c", cookie])
        assert result.exit_code == 0
        # Puzzle files generated
        assert (p / f"{day:02}/input.txt").exists()
        assert (p / f"{day:02}/solution.py").exists()
        # Input is cached
        assert (config_dir / cookie / f"2019/{day:02}.txt").exists()
        # Browser opened to today's puzzle URL
        webbrowser_open.assert_called_once_with(puzzle_url)


@freeze_time(datetime(2019, 12, 25, hour=1, tzinfo=pytz.timezone("America/New_York")))
@given(st.integers().filter(lambda x: not (1 <= x <= 25)))
def test_begin_specify_fails_if_out_of_range(
    webbrowser_open, runner, config_dir, day
):
    cookie = "12345"
    with runner.isolated_filesystem():
        result = runner.invoke(cli, ["begin", "-d", day, "-c", cookie])
        assert result.exit_code == 2


@freeze_time(datetime(2019, 12, 10, hour=1, tzinfo=pytz.timezone("America/New_York")))
@pytest.mark.parametrize("year", range(2015, 2019))
def test_begin_specify_year(year, webbrowser_open, runner, config_dir, responses):
    day = 10  # matches frozen datetime
    puzzle_url = f"https://adventofcode.com/{year}/day/{day}"
    puzzle_input = "some text"
    responses.add(responses.GET, puzzle_url + "/input", body=puzzle_input)
    cookie = "12345"
    with runner.isolated_filesystem() as p:
        result = runner.invoke(cli, ["begin", "-y", year, "-c", cookie])
        assert result.exit_code == 0
        # Puzzle files generated
        assert (p / f"{day:02}/input.txt").exists()
        assert (p / f"{day:02}/solution.py").exists()
        # Input is cached
        assert (config_dir / cookie / f"{year}/{day:02}.txt").exists()
        # Browser opened to today's puzzle URL
        webbrowser_open.assert_called_once_with(puzzle_url)


@pytest.mark.parametrize("day", range(1, 25))
@pytest.mark.parametrize("year", range(2015, 2019))
def test_begin_specify_day_and_year(
    year, day, webbrowser_open, runner, config_dir, responses
):
    puzzle_url = f"https://adventofcode.com/{year}/day/{day}"
    puzzle_input = "some text"
    responses.add(responses.GET, puzzle_url + "/input", body=puzzle_input)
    cookie = "12345"
    with runner.isolated_filesystem() as p:
        result = runner.invoke(cli, ["begin", "-d", day, "-y", year, "-c", cookie])
        assert result.exit_code == 0
        # Puzzle files generated
        assert (p / f"{day:02}/input.txt").exists()
        assert (p / f"{day:02}/solution.py").exists()
        # Input is cached
        assert (config_dir / cookie / f"{year}/{day:02}.txt").exists()
        # Browser opened to today's puzzle URL
        webbrowser_open.assert_called_once_with(puzzle_url)


@freeze_time(datetime(2019, 12, 10, hour=1, tzinfo=pytz.timezone("America/New_York")))
def test_begin_cached_input(webbrowser_open, runner, config_dir, responses):
    """
    Puzzle input should not be fetched from https://adventofcode.com if it has
    been cached locally. Here, the `responses` fixture will raise an exception if
    any HTTP requests are made.
    """
    puzzle_url = "https://adventofcode.com/2019/day/10"
    cookie = "12345"
    cache_dir = config_dir / cookie / "2019"
    cache_dir.mkdir(parents=True)
    with (cache_dir / "10.txt").open("w") as f:
        f.write("some text")
    with runner.isolated_filesystem() as p:
        result = runner.invoke(cli, ["begin", "-c", cookie])
        assert result.exit_code == 0
        # Puzzle files generated
        assert (p / "10/input.txt").exists()
        assert (p / "10/solution.py").exists()
        # Browser opened to today's puzzle URL
        webbrowser_open.assert_called_once_with(puzzle_url)
