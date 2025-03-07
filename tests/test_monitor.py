import pytest
import requests

from app_monitor.app_config import AppConfig
from app_monitor.async_monitor import ProbeResult
from app_monitor.monitor import AppMonitor
import responses
from responses.registries import OrderedRegistry


@pytest.fixture(autouse=True)
def app_config() -> AppConfig:
    return AppConfig(
        check_interval=1,
        warn_threshold=0,
        endpoints=[
            "http://example1.com/status",
            "http://example2.com/status",
            "http://example3.com/status",
        ],
    )


@responses.activate(registry=OrderedRegistry)
def test_app_monitor(app_config, caplog):
    # Setup
    app_monitor = AppMonitor(app_config)
    responses.get(
        "http://example1.com/status",
        status=500,
        json={"msg": "server error"},
    )
    responses.get(
        "http://example1.com/status",
        status=200,
        json={"msg": "OK"},
    )
    responses.get(
        "http://example2.com/status",
        status=502,
        json={"msg": "server error"},
    )
    responses.get(
        "http://example2.com/status",
        status=404,
        json={"msg": "not found"},
    )
    responses.get(
        "http://example3.com/status",
        status=502,
        json={"msg": "server error"},
    )
    responses.get(
        "http://example3.com/status",
        status=502,
        json={"msg": "server error"},
    )
    responses.get(
        "http://example3.com/status",
        status=502,
        json={"msg": "server error"},
    )
    responses.get(
        "http://example3.com/status",
        status=502,
        json={"msg": "server error"},
    )

    # Exercise
    # result = app_monitor.probe_endpoint("http://example1.com/status")
    app_monitor.probe_all_endpoints()

    # Assert
    print(f"my stuff: {caplog.text}")
    for msg in [
        "WARNING  root:monitor.py:38 Endpoint http://example1.com/status took too long to respond",
        "Endpoint http://example2.com/status returned status code 404",
        "WARNING  root:monitor.py:38 Endpoint http://example2.com/status took too long to respond",
        "ERROR    root:monitor.py:27 All retries failed when probing endpoint http://example3.com/status",
    ]:
        assert msg in caplog.text
