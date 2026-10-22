
"""Read inventory data from a NetBox instance."""

import os

import requests


class NetBoxClient:
    """Minimal read-only NetBox REST API client."""

    def __init__(self, base_url: str, token: str, timeout: int = 10) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "Authorization": f"Bearer {token}",
                "Accept": "application/json",
            }
        )

    def get_devices(self) -> list[dict]:
        """Return all devices, following NetBox API pagination."""
        url = f"{self.base_url}/api/dcim/devices/"
        devices: list[dict] = []

        while url:
            response = self.session.get(url, timeout=self.timeout)
            response.raise_for_status()
            payload = response.json()

            devices.extend(payload.get("results", []))
            url = payload.get("next")

        return devices

def client_from_environment() -> NetBoxClient:
    """Build a NetBox client for the selected environment."""
    target_env = os.environ.get("TARGET_ENV", "DEV").upper()

    if target_env not in {"DEV", "STAGING", "PROD"}:
        raise ValueError(
            "TARGET_ENV must be DEV, STAGING, or PROD"
        )

    base_url = os.environ.get(f"NETBOX_{target_env}_URL")
    token = os.environ.get(f"NETBOX_{target_env}_TOKEN")

    if not base_url or not token:
        raise RuntimeError(
            f"NETBOX_{target_env}_URL and "
            f"NETBOX_{target_env}_TOKEN must be set"
        )

    return NetBoxClient(base_url, token)
