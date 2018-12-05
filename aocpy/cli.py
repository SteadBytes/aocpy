import click

from aocpy.exception import (
    RepeatSubmissionError,
    IncorrectSubmissionError,
    RateLimitError,
)
from aocpy.generate import generate_day
from aocpy.puzzle import Puzzle
from aocpy.utils import current_day, current_year, get_session_cookie


def begin_day(p: Puzzle):
    click.echo(f"Initialising {p.year}, day {p.day:02} puzzle...")
    generate_day(p)
    click.echo("Opening puzzle page in browser...")
    p.browse()


@click.group()
def cli():
    pass


@cli.command()
@click.option("-y", "--year", default=current_year, type=click.INT)
@click.option("-d", "--day", default=current_day, type=click.IntRange(1, 25))
@click.option(
    "-c",
    "--session-cookie",
    default=get_session_cookie,
    type=click.STRING,
    envvar="AOC_SESSION_COOKIE",
)
def begin(year, day, session_cookie):
    p = Puzzle(year, day, session_cookie)
    begin_day(p)


@cli.command()
@click.argument("answer")
@click.argument("level", type=click.IntRange(1, 2))
@click.option("-y", "--year", default=current_year, type=click.INT)
@click.option("-d", "--day", default=current_day, type=click.IntRange(1, 25))
@click.option(
    "-c",
    "--session-cookie",
    default=get_session_cookie,
    type=click.STRING,
    envvar="AOC_SESSION_COOKIE",
)
def submit(answer, level, year, day, session_cookie):
    p = Puzzle(year, day, session_cookie)
    try:
        p.submit(answer, level)
    except RepeatSubmissionError as err:
        click.echo(f"{p} level {err.level} is already complete")
    except IncorrectSubmissionError as err:
        click.echo(f"Incorrect answer {err.answer} for {p} level {err.level}")
    except RateLimitError as err:
        click.echo(err)


if __name__ == "__main__":
    cli()
