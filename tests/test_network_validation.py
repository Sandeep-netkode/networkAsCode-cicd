from python.network_validation import is_valid_ip


def test_valid_ipv4():
    assert is_valid_ip("192.168.1.1")


def test_valid_ipv6():
    assert is_valid_ip("2001:db8::1")


def test_invalid_ip():
    assert not is_valid_ip("999.999.999.999")
