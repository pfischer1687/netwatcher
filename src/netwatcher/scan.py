"""Monitor outbound network connections."""

import typer
from loguru import logger

from .logging_config import setup_logging
from .rconn import get_remote_connections

app = typer.Typer()


@app.command()
def scan(
    verbose: int = typer.Option(0, "--verbose", "-v", count=True, help="Increase verbosity (-v, -vv, -vvv)"),
    log_to_file: bool = typer.Option(False, "-l", is_flag=True, help="Whether to log to file or just to stderr."),
) -> None:
    """_summary_.

    Args:
        verbose (int, optional): _description_. Defaults to typer.Option(1, "--verbose", "-v", count=True,
            help="Increase verbosity (-v, -vv, -vvv)").
        log_to_file (bool, optional): _description_. Defaults to typer.Option(False, help="Override default log file
            path").
    """
    setup_logging(verbose, log_to_file)

    logger.info("Getting remote connections.")
    _remote_conns = get_remote_connections()
