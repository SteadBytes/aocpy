import click

from aocpy.generate import generate_day
from aocpy.puzzle import Puzzle
from aocpy.utils import current_day, current_year, get_session_cookie


def init_day(p: Puzzle):
    click.echo(f"Initialising {p.year}, day {p.day:02} puzzle...")
    generate_day(p)
    click.echo("Opening puzzle page in browser...")


@click.group()
def cli():
    pass


@cli.command()
@click.option(
    "-c",
    "--session-cookie",
    default=get_session_cookie,
    type=click.STRING,
    envvar="AOC_SESSION_COOKIE",
)
def today(session_cookie):
    p = Puzzle.today(session_cookie)
    init_day(p)


@cli.command()
@click.argument("year", type=click.INT)
@click.argument("day", type=click.IntRange(1, 25))
@click.option(
    "-c",
    "--session-cookie",
    default=get_session_cookie,
    type=click.STRING,
    envvar="AOC_SESSION_COOKIE",
)
def init(year, day, session_cookie):
    p = Puzzle(year, day, session_cookie)
    init_day(p)


if __name__ == "__main__":
    cli()
