import datetime
from pathlib import Path
from string import ascii_letters, digits
from urllib.parse import urlparse

import pytest
import pytz
from freezegun import freeze_time
from hypothesis import given
from hypothesis import strategies as st

from aocpy.exception import AocpyException
from aocpy.puzzle import Puzzle

cookie_strategy = st.text(
    alphabet=st.sampled_from(ascii_letters + digits), min_size=96, max_size=96,
)

year_strategy = st.integers(min_value=2015, max_value=2020)
day_strategy = st.integers(min_value=1, max_value=25)


@st.composite
def puzzle_strategy(draw):
    year, day, cookie = [
        draw(strat) for strat in (year_strategy, day_strategy, cookie_strategy)
    ]
    return Puzzle(year, day, cookie), year, day, cookie


@given(puzzle_strategy())
def test_puzzle_url(p_data):
    puzzle, year, day, cookie = p_data
    o = urlparse(puzzle.url)
    assert o.scheme == "https"
    assert o.netloc == "adventofcode.com"
    assert o.path == f"/{year}/day/{day}"


@given(puzzle_strategy())
def test_puzzle_input_fname(p_data):
    puzzle, year, day, cookie = p_data
    p = Path(puzzle.input_fname)
    assert p == Path().home() / f".config/aocd/{cookie}/{year}/{day}.txt"


@given(year_strategy, day_strategy, cookie_strategy)
def test_puzzle_today(year, day, cookie):
    date = datetime.datetime(
        year, 12, day, hour=1, tzinfo=pytz.timezone("America/New_York")
)
    with freeze_time(date):
        p = Puzzle.today(cookie)
        assert p.year == date.year
        # should use the latest day that has a challenge
        assert p.day == min(date.day, 25)


@given(
    st.datetimes(timezones=st.just(pytz.timezone("America/New_York"))).filter(
        lambda d: d.month != 12
    ),
    cookie_strategy,
)
def test_puzzle_today_raises_when_not_december(date, cookie):
    with freeze_time(date):
        with pytest.raises(AocpyException):
            Puzzle.today(cookie)
