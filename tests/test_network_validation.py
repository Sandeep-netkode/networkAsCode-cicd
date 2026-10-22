from python.network_validation import is_valid_ip


def test_valid_ipv4():
    assert is_valid_ip("192.168.1.1")


def test_valid_ipv6():
    assert is_valid_ip("2001:db8::1")


def test_invalid_ip():
    assert not is_valid_ip("999.999.999.999")


def make_device(name, role):
    return {"name": name, "role": {"name": role}}


def test_valid_dev_inventory():
    from python.network_validation import validate_inventory

    devices = [
        make_device("dev-r1", "Router"),
        make_device("dev-switch", "Core switch"),
    ]

    assert validate_inventory("DEV", devices) == []


def test_valid_staging_inventory():
    from python.network_validation import validate_inventory

    devices = [
        make_device("stg-r1", "Router"),
        make_device("stg-csw1", "Core switch"),
        make_device("stg-asw1", "Access switch"),
        make_device("stg-asw2", "Access switch"),
    ]

    assert validate_inventory("STAGING", devices) == []


def test_missing_access_switch_fails():
    from python.network_validation import validate_inventory

    devices = [
        make_device("prod-r1", "Router"),
        make_device("prod-csw1", "Core switch"),
        make_device("prod-asw1", "Access switch"),
    ]

    errors = validate_inventory("PROD", devices)

    assert any("access switch" in error for error in errors)


def test_wrong_environment_fails():
    from python.network_validation import validate_inventory

    errors = validate_inventory("DEVELOPMENT", [])

    assert errors == ["Unsupported environment: DEVELOPMENT"]


def test_duplicate_device_name_fails():
    from python.network_validation import validate_inventory

    devices = [
        make_device("dev-r1", "Router"),
        make_device("dev-r1", "Router"),
        make_device("dev-switch", "Core switch"),
    ]

    errors = validate_inventory("DEV", devices)

    assert "Duplicate device name: dev-r1" in errors