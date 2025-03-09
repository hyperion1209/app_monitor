import pytest
import re

from app_monitor.app_config import AppConfig
from app_monitor.monitor import AppMonitor
import responses
from responses.registries import OrderedRegistry
from unittest.mock import PropertyMock, patch


@pytest.fixture(autouse=True)
def app_config() -> AppConfig:
    return AppConfig(
        check_interval=1,
        warn_threshold=0,
        retries=2,
        endpoints=[
            "http://example1.com/status",
            "http://example2.com/status",
            "http://example3.com/status",
        ],
    )


@responses.activate(registry=OrderedRegistry)
@patch.object(AppMonitor, "RUN", new_callable=PropertyMock)
def test_app_monitor(mocked, app_config, caplog):
    # Setup
    app_monitor = AppMonitor(app_config)
    mocked.side_effect = [True, False]

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
    app_monitor.run()

    # Assert
    print(f"my logs:\n{caplog.text}")
    for msg in [
        re.compile(
            r"WARNING\s+root:monitor.py:\d+ Endpoint http://example1.com/status"
            r" took too long to respond"
        ),
        re.compile(
            r"ERROR\s+root:monitor.py:\d+ Endpoint http://example2.com/status "
            r"returned status code 404"
        ),
        re.compile(
            r"WARNING\s+root:monitor.py:\d+ Endpoint http://example2.com/status"
            r" took too long to respond",
        ),
        re.compile(
            r"ERROR\s+root:monitor.py:\d+ All retries failed when probing "
            r"endpoint http://example3.com/status",
        ),
    ]:
        assert msg.search(caplog.text)
