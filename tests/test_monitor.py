import pytest

from app_monitor.app_config import AppConfig


@pytest.fixture(autouse=True)
def app_config():
    return AppConfig(
        check_interval=10,
        warn_threshold=1.0,
        endpoints=["http://example1.com", "http://example2.com"],
    )
