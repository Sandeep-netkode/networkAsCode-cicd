
"""Validate a selected environment's NetBox inventory."""

import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT))

from python.netbox_client import client_from_environment
from python.network_validation import validate_inventory


def main() -> int:
    load_dotenv(PROJECT_ROOT / ".env")

    target_env = __import__("os").environ.get("TARGET_ENV", "DEV").upper()
    print(f"Validating NetBox inventory for {target_env}...")

    client = client_from_environment()
    devices = client.get_devices()

    print(f"NetBox API connection successful. Devices found: {len(devices)}")

    for device in devices:
        name = device.get("name") or "(unnamed)"
        role = (device.get("role") or {}).get("name", "No role")
        status = (device.get("status") or {}).get("label", "Unknown")
        print(f"- {name} | Role: {role} | Status: {status}")

    errors = validate_inventory(target_env, devices)

    if errors:
        print("\nINVENTORY VALIDATION FAILED:")
        for error in errors:
            print(f"- {error}")
        return 1

    print(f"\nINVENTORY VALIDATION PASSED for {target_env}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
