import os
from datetime import datetime

import pytz

AOC_TZ = pytz.timezone("America/New_York")
CONFIG_FNAME = os.path.expanduser("~/.config/aocd/token")


def current_year():
    """ Returns the most recent AOC year available
    """
    now = datetime.now(tz=AOC_TZ)
    year = now.year
    return year - 1 if now.month < 12 else year


def current_day(now):
    """ Returns the current day number

    Raises Exception if not currently December
    """
    now = datetime.now(tz=AOC_TZ)
    if now.month != 12:
        raise Exception("must be December")

    return min(now.day, 25)


def get_session_cookie():
    cookie = os.environ.get("AOC_SESSION_COOKIE")
    if cookie is not None:
        return cookie
    try:
        with open(CONFIG_FNAME) as f:
            cookie = f.read().strip()
    except (OSError, IOError) as err:
        pass
    if cookie:
        return cookie

    raise Exception("unable to get AOC session cookie")
