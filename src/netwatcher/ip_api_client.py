"""Aynchronous HTTP client for querying the IP-API batch endpoint."""

from enum import Enum
from types import TracebackType
from typing import Self

from httpx import AsyncClient, HTTPStatusError, RequestError, TimeoutException
from loguru import logger
from pydantic import BaseModel, ValidationError
from pydantic_settings import BaseSettings
from yarl import URL


class Iso639LanguageCode(str, Enum):
    """ISO 639 language codes supported by the IP-API service."""

    EN = "en"
    DE = "de"
    ES = "es"
    PTBR = "pt-BR"
    FR = "fr"
    JA = "ja"
    ZHCN = "zh-CN"
    RU = "ru"


class Settings(BaseSettings):
    """Configuration settings for interacting with the IP-API batch endpoint.

    Attributes:
        fields (int | str): Fields to return in the response, defaults to bitmask for `status,message,country,
            countryCode,regionName,city,isp,org,asname,proxy,hosting,query` (21161499).
        ip_api_batch_json_base_url (URL): Base URL for the batch JSON endpoint.
        ip_api_lang (Iso639LanguageCode): Language code for localizing response messages.
        max_batch_size (int): Maximum number of queries in the IP-API batch endpoint before rate-limiting occurs.
        timeout (float): Timeout (in seconds) for the HTTP requests.
    """

    fields: int | str = 21161499
    ip_api_batch_json_base_url: URL = URL("http://ip-api.com/batch")
    ip_api_lang: Iso639LanguageCode = Iso639LanguageCode.EN
    max_batch_size: int = 100
    timeout: float = 5.0

    def get_ip_api_batch_json_url(self) -> str:
        """Construct the full IP-API batch endpoint URL with query parameters.

        Returns:
            str: Fully formatted URL with `fields` and `ip_api_lang` parameters applied.
        """
        url = self.ip_api_batch_json_base_url.update_query({"fields": self.fields, "lang": self.ip_api_lang.value})
        return str(url)


class IPApiResponse(BaseModel):
    """Schema for a single IP-API batch response entry."""

    status: str | None = None
    message: str | None = None
    country: str | None = None
    country_code: str | None = None
    region_name: str | None = None
    city: str | None = None
    isp: str | None = None
    org: str | None = None
    asname: str | None = None
    proxy: bool | None = None
    hosting: bool | None = None
    query: str | None = None


class IPApiClient:
    """Aynchronous HTTP client for querying the IP-API batch endpoint.

    Attributes:
        client (AsyncClient): The underlying async HTTP client.
        settings (Settings): A validated settings object containing configuration.
    """

    def __init__(self, settings: Settings) -> None:
        """Initialize the client with a settings object.

        Args:
            settings (Settings): Configuration for the client.
        """
        self.client = AsyncClient(timeout=settings.timeout)
        self.settings = settings

    async def __aenter__(self) -> Self:
        """Enter the asynchronous context manager.

        Returns:
            Self: The IPApiClient instance, ready to use in an async context.
        """
        return self

    async def __aexit__(
        self, _exc_type: type[BaseException] | None, _exc_val: BaseException | None, _exc_tb: TracebackType | None
    ) -> None:
        """Exit the asynchronous context manager, ensuring the client is closed."""
        await self.aclose()

    async def fetch_batch_ip_data(self, ips: list[str]) -> list[IPApiResponse]:
        """Perform a batch geolocation lookup asynchronously.

        Args:
            ips (list[str]): List of IP addresses to look up.

        Returns:
            list[IPApiResponse]: Parsed API responses.

        Raises:
            RuntimeError: When the API call fails or response is malformed.
        """
        url = self.settings.get_ip_api_batch_json_url()
        logger.debug(f"Sending batch IP request to {url} with {len(ips)} IPs.")

        try:
            if len(ips) > self.settings.max_batch_size:
                logger.warning(
                    f"{len(ips)} IP addresses are listed, only querying for the first {self.settings.max_batch_size} "
                    "due to rate limits."
                )
                ips = ips[: self.settings.max_batch_size]

            response = await self.client.post(url, json=ips)
            response.raise_for_status()
            results = response.json()

            if not isinstance(results, list):
                logger.error("Unexpected response format from IP API.")
                raise RuntimeError("Expected a list of results from IP API.")

            parsed_results = []
            for item in results:
                try:
                    response = IPApiResponse.model_validate(item)
                    parsed_results.append(response)
                except ValidationError as e:
                    logger.warning(f"Skipping invalid response item: {e}")

            logger.info(f"Received {len(parsed_results)} valid responses from IP API.")
            return parsed_results

        except HTTPStatusError as e:
            logger.error("HTTP error from IP API: {e.response.status_code} - {e.response.text}")
            raise RuntimeError(f"IP API request failed with status {e.response.status_code}") from e

        except (RequestError, TimeoutException) as e:
            logger.error("Request to IP API failed: {e}")
            raise RuntimeError("Request to IP API failed.") from e

        except Exception as e:
            logger.error("Unexpected error during IP API request.")
            raise RuntimeError("Unexpected error during IP API request.") from e

    async def aclose(self) -> None:
        """Close the underlying HTTP client to release resources."""
        logger.debug("Closing HTTP client session.")
        await self.client.aclose()
