import ipaddress


def is_valid_ip(address: str) -> bool:
    """Return True if the supplied string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False
