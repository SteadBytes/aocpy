import os
from datetime import datetime

import pytz

from aocpy.exception import AocpyException

AOC_TZ = pytz.timezone("America/New_York")
CONFIG_DIRNAME = "~/.config/aocpy"


def current_year():
    """ Returns the most recent AOC year available
    """
    now = datetime.now(tz=AOC_TZ)
    year = now.year
    return year - 1 if now.month < 12 else year


def current_day():
    """ Returns the latest puzzle day number. Returns 25 if current day of month
    is > 25.

    Raises:
        `AocpyException` if not currently December
    """
    now = datetime.now(tz=AOC_TZ)
    if now.month != 12:
        raise AocpyException("must be December")

    return min(now.day, 25)


def get_session_cookie():
    cookie = os.environ.get("AOC_SESSION_COOKIE")
    if cookie is not None:
        return cookie
    try:
        with open(os.path.join(os.path.expanduser(CONFIG_DIRNAME), "token")) as f:
            cookie = f.read().strip()
    except (OSError, IOError):
        pass
    if cookie:
        return cookie

    raise AocpyException("unable to get AOC session cookie")
