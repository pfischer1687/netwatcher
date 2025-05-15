"""Utility functions for unit tests of the Netwatcher CLI."""


def get_mock_batch_ip_data() -> list[dict[str, str]]:
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
            "mobile": "false",
            "proxy": "false",
            "hosting": "false",
            "query": "8.8.8.8",
        },
        {
            "status": "fail",
            "country": "Australia",
            "countryCode": "AU",
            "regionName": "New South Wales",
            "city": "Sydney",
            "isp": "Cloudflare",
            "org": "Cloudflare",
            "asname": "CLOUDFLARENET",
            "mobile": "true",
            "proxy": "true",
            "hosting": "true",
            "query": "1.1.1.1",
        },
    ]
