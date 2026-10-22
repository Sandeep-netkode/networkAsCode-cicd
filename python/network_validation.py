
"""Validation utilities for network inventory and IP addresses."""

import ipaddress
from collections import Counter

EXPECTED_ROLES = {
    "DEV": {
        "router": 1,
        "core switch": 1,
    },
    "STAGING": {
        "router": 1,
        "core switch": 1,
        "access switch": 2,
    },
    "PROD": {
        "router": 1,
        "core switch": 1,
    },
}


def is_valid_ip(address: str) -> bool:
    """Return True if the supplied string is a valid IPv4 or IPv6 address."""
    try:
        ipaddress.ip_address(address)
        return True
    except ValueError:
        return False


def validate_inventory(
    target_env: str,
    devices: list[dict],
) -> list[str]:
    """Return validation errors for a NetBox environment inventory."""
    environment = target_env.strip().upper()

    if environment not in EXPECTED_ROLES:
        return [f"Unsupported environment: {target_env}"]

    errors = []
    device_names = []
    role_counts = Counter()

    for device in devices:
        name = device.get("name")
        role_data = device.get("role") or {}
        role = role_data.get("name", "").strip().lower()

        if not name:
            errors.append("Found a device without a name.")
        else:
            device_names.append(name)

        if role:
            role_counts[role] += 1
        else:
            errors.append(
                f"Device '{name or '(unnamed)'}' has no role."
            )

    duplicates = sorted(
        name for name, count in Counter(device_names).items()
        if count > 1
    )
    for name in duplicates:
        errors.append(f"Duplicate device name: {name}")

    expected = EXPECTED_ROLES[environment]

    for role, required_count in expected.items():
        actual_count = role_counts[role]
        if actual_count != required_count:
            errors.append(
                f"{environment} requires {required_count} "
                f"'{role}' device(s), found {actual_count}."
            )

    unexpected_roles = sorted(set(role_counts) - set(expected))
    for role in unexpected_roles:
        errors.append(f"Unexpected role in {environment}: '{role}'.")

    return errors
