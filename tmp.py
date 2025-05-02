import psutil
import requests
import typer
import ipaddress
from typing import List
from collections import defaultdict

app = typer.Typer()

# IP geolocation service URL
IP_API_URL = "http://ipinfo.io/{}/json"

# Local network ranges (IPv4) to exclude
LOCAL_NETWORK_RANGES = [
    ipaddress.ip_network("127.0.0.0/8"),  # Loopback
    ipaddress.ip_network("10.0.0.0/8"),   # Private network
    ipaddress.ip_network("172.16.0.0/12"),  # Private network
    ipaddress.ip_network("192.168.0.0/16"),  # Private network
]

def get_local_ips() -> set:
    """
    Retrieve a set of local IPs assigned to network interfaces on the machine.
    """
    local_ips = set()
    for interface, addrs in psutil.net_if_addrs().items():
        for addr in addrs:
            if addr.family == psutil.AF_INET:
                local_ips.add(addr.address)
    return local_ips

def is_local_ip(ip: str, local_ips: set) -> bool:
    """
    Check if the IP is part of the local network or loopback.
    """
    ip_obj = ipaddress.ip_address(ip)
    for network in LOCAL_NETWORK_RANGES:
        if ip_obj in network or ip in local_ips:
            return True
    return False

def get_remote_ips() -> List[str]:
    """
    Retrieve a list of remote IPs that the system is connected to via TCP connections,
    excluding local IPs.
    """
    local_ips = get_local_ips()  # Get local IP addresses
    remote_ips = set()

    for conn in psutil.net_connections(kind='inet'):
        if conn.raddr:
            remote_ip = conn.raddr.ip
            # Only add remote IPs that are not in the local network
            if not is_local_ip(remote_ip, local_ips):
                remote_ips.add(remote_ip)

    return list(remote_ips)

def get_geo_data(ip: str) -> dict:
    """
    Get geolocation data for an IP address using ipinfo.io API.
    """
    response = requests.get(IP_API_URL.format(ip))
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": f"Failed to get data for {ip}"}

def display_remote_ips_info(remote_ips: List[str]) -> None:
    """
    Display information about remote IPs including location and organization.
    """
    ip_info_map = defaultdict(dict)

    for ip in remote_ips:
        geo_data = get_geo_data(ip)
        ip_info_map[ip] = geo_data

    for ip, info in ip_info_map.items():
        print(f"IP Address: {ip}")
        if 'error' in info:
            print(f"Error: {info['error']}")
        else:
            loc = info.get("loc", "Not available")
            org = info.get("org", "Not available")
            city = info.get("city", "Not available")
            country = info.get("country", "Not available")
            print(f"Location: {city}, {country}")
            print(f"Coordinates: {loc}")
            print(f"Business: {org}")
        print("-" * 40)

@app.command()
def get_info():
    """
    Get remote IP addresses your system is connected to, and print their geographic location and business information.
    Excludes local network IPs.
    """
    remote_ips = get_remote_ips()
    if not remote_ips:
        print("No active remote network connections found.")
        return

    display_remote_ips_info(remote_ips)

if __name__ == "__main__":
    app()