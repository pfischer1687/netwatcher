"""Monitor outbound network connections and fetch IP geolocation data."""

import asyncio
from typing import Annotated

from loguru import logger
from typer import Exit, Option, Typer

from .ip_api_client import IPApiClient, Iso639LanguageCode, Settings
from .logging_config import setup_logging
from .rconn import get_remote_connections

app = Typer()


async def fetch_batch_ip_data(ips: list[str], settings: Settings):
    """Fetch geolocation data for a batch of IP addresses.

    Args:
        ips (list[str]): A list of IP addresses to query.
        settings (Settings): Configuration settings for the IP-API client.

    Returns:
        list[IPApiResponse]: List of parsed responses from the IP-API batch JSON post request.
    """
    async with IPApiClient(settings) as client:
        return await client.fetch_batch_ip_data(ips)


@app.command()
def scan(
    ip_api_lang: Annotated[str, Option("-l", "--lang", help="Language code for the IP API response.")] = "en",
    log_to_file: Annotated[
        bool, Option("-f", "--log-to-file", is_flag=True, help="Whether to log to file or just to stderr.")
    ] = False,
    verbose: Annotated[int, Option("-v", "--verbose", count=True, help="Increase verbosity (-v, -vv, -vvv)")] = 1,
) -> None:
    """Scan IP addresses using IP-API with configurable logging and language support.

    Args:
        ip_api_lang (str): Language code for the IP API response. Defaults to `en`.
        log_to_file (bool): Whether to write logs to a file instead of stderr. Defaults to `False`.
        verbose (int): Verbosity level (-v, -vv, -vvv). Defaults to 0.
    """
    setup_logging(verbose, log_to_file)

    logger.info(f"Initializing scan with ip_api_lang={ip_api_lang}, log_to_file={log_to_file}, verbose={verbose}")

    try:
        iso_language_code = Iso639LanguageCode(ip_api_lang)
        settings = Settings(ip_api_lang=iso_language_code)
    except ValueError as e:
        logger.error("Invalid language: {language}. Must be one of: {[i.value for i in Iso639LanguageCode]}")
        raise Exit(code=1) from e

    logger.info("Getting remote connections.")
    remote_conns = get_remote_connections()
    ips = [str(remote_conn.remote_ip) for remote_conn in remote_conns]

    if not ips:
        logger.warning("No remote IPs found. Exiting.")
        raise Exit()

    logger.info(f"Querying IP-API for {len(ips)} IPs")
    try:
        _batch_ip_data = asyncio.run(fetch_batch_ip_data(ips, settings))
    except RuntimeError as e:
        logger.error("Failed to fetch IP data: {e.response.status_code} - {e.response.text}")
        raise Exit(code=1) from e
