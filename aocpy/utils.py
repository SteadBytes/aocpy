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
