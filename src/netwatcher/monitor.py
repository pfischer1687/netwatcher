"""NetWatcher CLI - Monitor outbound network connections."""

import psutil


def get_active_connections() -> list:
    """Returns active connections.

    Returns:
        list: _description_
    """
    active_connections = psutil.net_connections(kind="inet")
    return active_connections
