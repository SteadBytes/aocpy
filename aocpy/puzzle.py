import logging
import os
import webbrowser

# TODO: Remove repeated parameter passing (NamedTuple?)
from dataclasses import dataclass, field

import requests
from bs4 import BeautifulSoup

from aocpy.exception import (
    AocpyException,
    IncorrectSubmissionError,
    RateLimitError,
    RepeatSubmissionError,
    SubmissionError,
)
from aocpy.utils import current_day, current_year

logger = logging.getLogger(__name__)

URL = "https://adventofcode.com/{year}/day/{day}"
INPUT_FNAME = "{session_cookie}/{year}/{day}.txt"
GLOBAL_CACHE_DIR = os.path.expanduser("~/.config/aocd")


def session(session_cookie):
    s = requests.Session()
    s.cookies["session"] = session_cookie
    return s


@dataclass
class PuzzleData:
    year: int
    day: int
    session_cookie: str
    url: str = field(init=False)

    def __post_init__(self):
        setattr(self, "url", URL.format(year=self.year, day=self.day))


def check_submission_response_text(text: str):
    soup = BeautifulSoup(text, "html.parser")
    message = soup.article.text
    if "Thats the right answer!" in message:
        return True
    elif "Did you already complete it" in message:
        raise RepeatSubmissionError(message)
    elif "That's not the right answer" in message:
        raise IncorrectSubmissionError(message)
    elif "You gave an answer too recently" in message:
        raise RateLimitError(message)
    return False


def _fetch_puzzle_input(session, year, day):
    url = URL.format(year=year, day=day) + "/input"
    r = session.get(url)
    if not r.ok:
        msg = f"got {r.status_code} fetching day {day} year {year}"
        logger.error(msg)
        logger.error(r.content)
        raise AocpyException(msg)

    return r.text.rstrip("\r\r")


def _puzzle_input_path(year, day, session_cookie, global_cache: bool):
    fname = INPUT_FNAME.format(session_cookie=session_cookie, year=year, day=day)
    return os.path.join(GLOBAL_CACHE_DIR if global_cache else "", fname)


def get_puzzle_input(session, year, day, session_cookie, global_cache=True):
    path = _puzzle_input_path(year, day, session_cookie, global_cache=global_cache)
    if os.path.isfile(path):
        with open(path) as f:
            return f.read()
    else:
        puzzle_input = _fetch_puzzle_input(session, year, day)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            f.write(puzzle_input)
        return puzzle_input


def submit_answer(session, answer, level, year, day):
    if level not in [1, 2, "1", "2"]:
        raise ValueError("Submit level must be 1 or 2")
    url = URL.format(year=year, day=day) + "/answer"

    r = session.post(url, data={"level": level, "answer": answer},)
    if not r.ok:
        logger.error(f"got {r.status_code} status code")
        logger.error(r.content)
        raise AocpyException(f"Non-200 response for POST: {r}")
    return r.text, r.url


class Puzzle:
    def __init__(self, year, day, session_cookie, global_cache=True):
        self.year = year
        self.day = day
        self.session_cookie = session_cookie
        self.global_cache = global_cache

        self.url = URL.format(year=year, day=day)
        self.session = session(session_cookie)

    def __str__(self):
        return f"Puzzle Day {self.day}, {self.year}"

    def __repr__(self):
        return f"Puzzle({self.year}, {self.day}, {self.session_cookie})"

    def browse(self):
        webbrowser.open(self.url)

    @staticmethod
    def today(session_cookie):
        """ Create a Puzzle instance for the current day.
        """
        year = current_year()
        day = current_day()
        return Puzzle(year, day, session_cookie)

    @property
    def puzzle_input(self):
        return get_puzzle_input(
            self.session,
            self.year,
            self.day,
            session_cookie=self.session_cookie,
            global_cache=self.global_cache,
        )

    def submit(self, answer, level):
        text, redirect_url = submit_answer(
            self.session, answer, level, self.year, self.day
        )
        if check_submission_response_text(text):
            webbrowser.open(redirect_url)
        else:
            raise SubmissionError(f"Unable to parse submission response text: {text}")
