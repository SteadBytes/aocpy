import logging
import os
import webbrowser

import requests
from bs4 import BeautifulSoup

from aocpy.exception import (
    AocpyException,
    RepeatSubmissionError,
    IncorrectSubmissionError,
    RateLimitError,
)
from aocpy.utils import current_day, current_year

logger = logging.getLogger(__name__)

URL = "https://adventofcode.com/{year}/day/{day}"
INPUT_FNAME = "{session_cookie}/{year}/{day}.txt"
GLOBAL_CACHE_DIR = os.path.expanduser("~/.config/aocd")


class Puzzle:
    def __init__(self, year, day, session_cookie, global_cache=True):
        self.year = year
        self.day = day
        self.session_cookie = session_cookie

        self.url = URL.format(year=year, day=day)

        input_fname = INPUT_FNAME.format(
            session_cookie=session_cookie, year=year, day=day
        )
        self.input_fname = os.path.join(
            GLOBAL_CACHE_DIR if global_cache else "", input_fname
        )
        self.is_input_cached = os.path.isfile(self.input_fname)

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
        if self.is_input_cached:
            with open(self.input_fname) as f:
                return f.read()
        else:
            return self._fetch_input()

    def submit(self, answer, level):
        if level not in [1, 2, "1", "2"]:
            raise Exception("submit level must be 1 or 2")

        r = requests.post(
            self.url + "/answer",
            cookies={"session": self.session_cookie},
            data={"level": level, "answer": answer},
        )

        if not r.ok:
            logger.error(f"got {r.status_code} status code")
            logger.error(r.content)
            raise AocpyException(f"Non-200 response for POST: {r}")

        soup = BeautifulSoup(r.text, "html.parser")
        message = soup.article.text
        if "Thats the right answer!" in message:
            webbrowser.open(r.url)
        elif "Did you already complete it" in message:
            raise RepeatSubmissionError(message, answer, level, self.year, self.day)
        elif "That's not the right answer" in message:
            raise IncorrectSubmissionError(message, answer, level, self.year, self.day)
        elif "You gave an answer too recently" in message:
            raise RateLimitError(message, answer, level, self.year, self.day)
        return r

    def _fetch_input(self):
        r = requests.get(self.url + "/input", cookies={"session": self.session_cookie})
        if not r.ok:
            msg = f"got {r.status_code} fetching day {self.day} year {self.year}"
            logger.error(msg)
            logger.error(r.content)
            raise AocpyException(msg)

        data = r.text.rstrip("\r\r")

        if not self.is_input_cached:
            self._cache_input(data)

        return data

    def _cache_input(self, puzzle_input):
        os.makedirs(os.path.dirname(self.input_fname), exist_ok=True)
        logger.info(f"caching puzzle input for {self}")
        with open(self.input_fname, "w") as f:
            f.write(puzzle_input)
