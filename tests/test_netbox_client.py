
from unittest.mock import Mock, patch

from python.netbox_client import NetBoxClient


def test_get_devices_returns_results_and_follows_pagination():
    client = NetBoxClient("http://netbox.example", "dummy-token")

    first_page = Mock()
    first_page.json.return_value = {
        "results": [{"name": "dev-r1"}],
        "next": "http://netbox.example/api/dcim/devices/?offset=1",
    }
    first_page.raise_for_status.return_value = None

    second_page = Mock()
    second_page.json.return_value = {
        "results": [{"name": "dev-sw1"}],
        "next": None,
    }
    second_page.raise_for_status.return_value = None

    with patch.object(
        client.session,
        "get",
        side_effect=[first_page, second_page],
    ) as mocked_get:
        devices = client.get_devices()

    assert [device["name"] for device in devices] == ["dev-r1", "dev-sw1"]
    assert mocked_get.call_count == 2


def test_client_requires_url_and_token(monkeypatch):
    monkeypatch.setenv("TARGET_ENV", "DEV")
    monkeypatch.delenv("NETBOX_DEV_URL", raising=False)
    monkeypatch.delenv("NETBOX_DEV_TOKEN", raising=False)

    from python.netbox_client import client_from_environment

    try:
        client_from_environment()
    except RuntimeError as exc:
        assert "NETBOX_DEV_URL" in str(exc)
        assert "NETBOX_DEV_TOKEN" in str(exc)
    else:
        raise AssertionError("Expected missing environment variables to fail")