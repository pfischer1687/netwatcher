"""Monitor outbound network connections."""

from __future__ import annotations

from pathlib import Path
from sys import stderr

import loguru
import typer
from loguru import logger
from rich.progress import Progress, SpinnerColumn, TextColumn

from .rconn import get_remote_connections

SCAN_LOGGER_ROTATION = "500 MB"
LOGGER_FILE_FORMAT = "{time:YYYY-MM-DD at HH:mm:ss} | {level} | {message}"
LOGGER_FILEPATH = Path("logs/scan_{time:YYYY-MM-DD-HH-mm-ss}.log").resolve()

app = typer.Typer()


def stderr_fmt(record: loguru.Record) -> str:
    """_summary_.

    Args:
        record (loguru.Record): _description_

    Returns:
        str: _description_
    """
    if record["level"].no >= 40:
        return "<green>{time}</> - {level} - <red>{thread}</> - <lvl>{message}</>\n{exception}"
    else:
        return "<green>{time}</> - {level} - <lvl>{message}</lvl>\n{exception}"


@app.command()
def scan(
    verbose: int = typer.Option("--verbose", "-v", count=True, help="Increase verbosity (-v, -vv, -vvv)"),
    log_to_file: bool = typer.Option("-l", is_flag=True, help="Whether to log to file or just to stderr."),
) -> None:
    """_summary_.

    Args:
        verbose (int, optional): _description_. Defaults to typer.Option(1, "--verbose", "-v", count=True,
            help="Increase verbosity (-v, -vv, -vvv)").
        log_to_file (bool, optional): _description_. Defaults to typer.Option(False, help="Override default log file
            path").
    """
    logger.remove()
    logger.add(sink=stderr, format=stderr_fmt, colorize=True, level=verbose, backtrace=True, diagnose=True)
    if log_to_file:
        logger.add(
            sink=LOGGER_FILEPATH,
            level=verbose,
            format=LOGGER_FILE_FORMAT,
            serialize=True,
            backtrace=True,
            diagnose=True,
            rotation=SCAN_LOGGER_ROTATION,
        )

    logger.info("Getting remote connections.")
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        progress.add_task(description="Getting remote connections...", total=None)
        _remote_conns = get_remote_connections()
