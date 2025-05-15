"""Unit tests for IPThreatAssessment model and logic."""

from netwatcher.ip_api_client import IPApiResponse
from netwatcher.ip_threat_assessment import IPThreatAssessment

from .utils import get_mock_batch_ip_data


def get_mock_reasons() -> list[list[str]]:
    """Return mock reason lists for testing IP threat assessment output.

    Returns:
        list[list[str]]: A list containing:
            - An empty list representing a non-suspicious IP.
            - A list of sample threat reasons representing a suspicious IP.
    """
    return [
        [],
        [
            "Lookup failed",
            "Proxy or VPN detected",
            "Hosting provider or data center",
            "Mobile network",
            "IP origin country (AU) is different from user's country (US)",
        ],
    ]


def test_get_reasons_returns_expected_threat_flags() -> None:
    """Test that get_reasons returns correct threat indicators for different IP inputs."""
    no_threat_data_raw, threat_data_raw = get_mock_batch_ip_data()
    no_threat_data = IPApiResponse.model_validate(no_threat_data_raw)
    threat_data = IPApiResponse.model_validate(threat_data_raw)

    expected_no_threat, expected_threat = get_mock_reasons()

    no_threat_result = IPThreatAssessment.get_reasons(no_threat_data, country_code="US")
    threat_result = IPThreatAssessment.get_reasons(threat_data, country_code="US")

    assert no_threat_result == expected_no_threat
    assert threat_result == expected_threat


def test_from_batch_ip_data_returns_enriched_assessments() -> None:
    """Test that from_batch_ip_data properly flags IPs and includes correct reasons."""
    raw_ip_data = get_mock_batch_ip_data()
    parsed_data = [IPApiResponse.model_validate(entry) for entry in raw_ip_data]

    assessments = IPThreatAssessment.from_batch_ip_data(parsed_data, country_code="US")
    expected_reasons = get_mock_reasons()

    assert len(assessments) == 2

    # First IP should not be suspicious
    assert assessments[0].is_suspicious is False
    assert assessments[0].reasons == expected_reasons[0]

    # Second IP should be flagged
    assert assessments[1].is_suspicious is True
    assert assessments[1].reasons == expected_reasons[1]
