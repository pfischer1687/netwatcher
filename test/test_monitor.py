"""NetWatcher CLI - Monitor outbound network connections."""

from src.netwatcher.monitor import get_active_connections


def test_get_active_connections() -> None:
    """_summary_."""
    get_active_connections()
