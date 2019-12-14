import webbrowser

import click

from aocpy import web
from aocpy.exception import (
    IncorrectSubmissionError,
    RateLimitError,
    RepeatSubmissionError,
)
from aocpy.generate import generate_day
from aocpy.puzzle import (
    Puzzle,
    check_submission_response_text,
    get_puzzle_input,
)
from aocpy.utils import current_day, current_year, get_session_cookie


def begin_day(session: web.AuthSession, p: Puzzle):
    click.echo(f"Initialising {p.year}, day {p.day:02} puzzle...")
    puzzle_input = get_puzzle_input(session, p)
    # TODO: handle already exists error better
    generate_day(p.day, puzzle_input)
    click.echo("Opening puzzle page in browser...")
    webbrowser.open(p.url)


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
    begin_day(web.session(session_cookie), p)


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
    text, redirect_url = web.submit_answer(
        web.session(session_cookie), p.url, answer, level
    )
    try:
        check_submission_response_text(text)
    except RepeatSubmissionError:
        click.echo(f"{p} level {level} is already complete")
    except IncorrectSubmissionError:
        click.echo(f"Incorrect answer {answer} for {year} day {day} level {level}")
    except RateLimitError as err:
        # TODO: Clean up this error message - remove '[Return to Day 13]' line
        click.echo(err)


if __name__ == "__main__":
    cli()
