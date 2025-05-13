"""Unit tests for the IPApiClient asynchronous HTTP client."""

from unittest.mock import MagicMock, patch

import pytest

from netwatcher.ip_api_client import IPApiClient, IPApiResponse, Settings


@pytest.fixture
def mock_settings():
    """Fixture that returns a default `Settings` object..

    Returns:
        Settings: A settings object configured for testing.
    """
    return Settings()


def get_mock_return_value() -> list[dict[str, str]]:
    """Gets a mock API response.

    Returns:
        list[dict[str, str]]: A simulated IP-API batch JSON endpoint response.
    """
    return [
        {
            "status": "success",
            "country": "United States",
            "countryCode": "US",
            "regionName": "California",
            "city": "Mountain View",
            "isp": "Google LLC",
            "org": "Google LLC",
            "asname": "GOOGLE",
            "proxy": "false",
            "hosting": "false",
            "query": "8.8.8.8",
        },
        {
            "status": "success",
            "country": "Australia",
            "countryCode": "AU",
            "regionName": "New South Wales",
            "city": "Sydney",
            "isp": "Cloudflare",
            "org": "Cloudflare",
            "asname": "CLOUDFLARENET",
            "proxy": "false",
            "hosting": "false",
            "query": "1.1.1.1",
        },
    ]


@pytest.mark.asyncio
async def test_fetch_batch_ip_data(mock_settings: Settings):
    """Test `IPApiClient.fetch_batch_ip_data` with a valid successful response.

    Args:
        mock_settings (Settings): A fixture providing configuration for the API client.

    Asserts:
        - The response list contains exactly two entries.
        - Each entry is an instance of `IPApiResponse`.
        - The expected IP addresses and country values are returned correctly.
    """
    ips = ["8.8.8.8", "1.1.1.1"]

    mock_post_response = MagicMock()
    mock_post_response.status_code = 200
    mock_post_response.json.return_value = get_mock_return_value()
    mock_post_response.raise_for_status = MagicMock()

    client = IPApiClient(mock_settings)

    with patch("httpx.AsyncClient.post", return_value=mock_post_response):
        results = await client.fetch_batch_ip_data(ips)

    assert len(results) == 2
    assert all(isinstance(r, IPApiResponse) for r in results)
    assert results[0].query == "8.8.8.8"
    assert results[1].country == "Australia"

    await client.aclose()
