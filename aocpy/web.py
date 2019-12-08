import logging
from typing import NewType, Union, Tuple

import requests

from aocpy.exception import AocpyException

logger = logging.getLogger(__name__)


AuthSession = NewType("AuthSession", requests.Session)


def session(session_cookie) -> AuthSession:
    s = requests.Session()
    s.cookies["session"] = session_cookie
    return s


def fetch_puzzle_input(session: AuthSession, puzzle_url: str) -> str:
    r = session.get(puzzle_url + "/input")
    if not r.ok:
        msg = f"got {r.status_code} fetching {puzzle_url}"
        logger.error(msg)
        logger.error(r.content)
        raise AocpyException(msg)

    return r.text.rstrip("\r\r")


def submit_answer(
    session: AuthSession, puzzle_url: str, answer: str, level: Union[int, str]
) -> Tuple[str, str]:
    if level not in [1, 2, "1", "2"]:
        raise ValueError("Submit level must be 1 or 2")
    r = session.post(puzzle_url + "/answer", data={"level": level, "answer": answer},)
    if not r.ok:
        logger.error(f"got {r.status_code} status code")
        logger.error(r.content)
        raise AocpyException(f"Non-200 response for POST: {r}")
    return r.text, r.url
