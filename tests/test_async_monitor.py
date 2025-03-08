import pytest
from unittest.mock import call, patch, PropertyMock
from app_monitor.async_monitor import AsyncAppMonitor
import httpx
from app_monitor.app_config import AppConfig
from pytest_httpx import HTTPXMock


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


@pytest.mark.asyncio
@patch.object(AsyncAppMonitor, "RUN", new_callable=PropertyMock)
async def test_supervisor(mocked, app_config, httpx_mock: HTTPXMock, caplog):
    # Setup
    async_monitor = AsyncAppMonitor(app_config)
    mocked.side_effect = [True, False]

    # Two failures for example1.com/status
    httpx_mock.add_exception(
        url="http://example1.com/status",
        method="GET",
        exception=httpx.ConnectError("Connection to server failed"),
    )
    httpx_mock.add_exception(
        url="http://example1.com/status",
        method="GET",
        exception=httpx.ConnectTimeout("Connection to server took too long"),
    )
    # One success for example2.com/status with status code 500
    httpx_mock.add_exception(
        url="http://example2.com/status",
        method="GET",
        exception=httpx.HTTPStatusError(
            request=httpx.Request("GET", "http://example2.com/status"),
            response=httpx.Response(status_code=500),
            message="Internal Server Error",
        )
    )
    # One success for example3.com/status with status code 200
    httpx_mock.add_response(
        url="http://example3.com/status", method="GET", status_code=200
    )

    # Exercise
    await async_monitor.supervisor()

    # Assert
    print(f"my logs:\n{caplog.text}")
    for msg in [
        "ERROR    root:async_monitor.py:57 Endpoint http://example1.com/status "
        "is unreachable: Connection to server took too long",
        "ERROR    root:async_monitor.py:53 Endpoint http://example2.com/status "
        "returned status code 500",
        "WARNING  root:async_monitor.py:61 Endpoint http://example3.com/status "
        "took too long to respond: 0.00 seconds",
    ]:
        assert msg in caplog.text
