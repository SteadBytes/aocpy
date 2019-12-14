import logging
import os
from dataclasses import dataclass, field
from typing import TypeVar

from bs4 import BeautifulSoup

from aocpy import web
from aocpy.exception import (
    IncorrectSubmissionError,
    RateLimitError,
    RepeatSubmissionError,
    SubmissionError,
)
from aocpy.utils import current_day, current_year

logger = logging.getLogger(__name__)

URL = "https://adventofcode.com/{year}/day/{day}"
INPUT_FNAME = "{session_cookie}/{year}/{day:02}.txt"
GLOBAL_CACHE_DIR = "~/.config/aocd"


T = TypeVar("T", bound="Puzzle")


@dataclass(frozen=True)
class Puzzle:
    year: int
    day: int
    session_cookie: str
    url: str = field(init=False)
    input_fname: str = field(init=False)

    def __post_init__(self):
        object.__setattr__(self, "url", URL.format(year=self.year, day=self.day))
        object.__setattr__(
            self,
            "input_fname",
            os.path.join(
                os.path.expanduser(GLOBAL_CACHE_DIR),
                INPUT_FNAME.format(
                    session_cookie=self.session_cookie, year=self.year, day=self.day
                ),
            ),
        )

    @staticmethod
    def today(session_cookie: str) -> T:
        """ Create a Puzzle instance for the current day.
        """
        year = current_year()
        day = current_day()
        return Puzzle(year, day, session_cookie)


def check_submission_response_text(text: str):
    soup = BeautifulSoup(text, "html.parser")
    try:
        message = soup.article.text
    except AttributeError:
        raise SubmissionError(f"Unable to parse submission response text: {text}")
    else:
        if "Thats the right answer!" in message:
            return
        elif "Did you already complete it" in message:
            raise RepeatSubmissionError(message)
        elif "That's not the right answer" in message:
            raise IncorrectSubmissionError(message)
        elif "You gave an answer too recently" in message:
            raise RateLimitError(message)
        else:
            raise SubmissionError(f"Unable to parse submission response text: {text}")


def get_puzzle_input(session: web.AuthSession, puzzle: Puzzle):
    if os.path.isfile(puzzle.input_fname):
        with open(puzzle.input_fname) as f:
            return f.read()
    else:
        puzzle_input = web.fetch_puzzle_input(session, puzzle.url)
        os.makedirs(os.path.dirname(puzzle.input_fname), exist_ok=True)
        with open(puzzle.input_fname, "w") as f:
            f.write(puzzle_input)
        return puzzle_input
