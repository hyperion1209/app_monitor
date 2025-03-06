import requests
import time
from retry.api import retry_call
from app_monitor.app_config import AppConfig
from app_monitor.logger import LOGGER, send_slack_notification


class AppMonitor:
    def __init__(self, app_config: AppConfig) -> None:
        self._app_config: AppConfig = app_config

    def probe_endpoint(self, endpoint: str) -> None:
        t = time.time()
        response = retry_call(
            requests.get,
            fargs=[endpoint],
            tries=3,
        )
        response_time = time.time() - t
        status_code = response.status_code
        if status_code != 200:
            msg = f"Endpoint {endpoint} returned status code {status_code}"
            LOGGER.error(msg)
            send_slack_notification(msg)
        if response_time > self._app_config.warn_threshold:
            LOGGER.warning(
                f"Endpoint {endpoint} took too long to respond: "
                f"{response_time:.2f} seconds"
            )

    def start(self) -> None:
        while True:
            for endpoint in self._app_config.endpoints:
                self.probe_endpoint(endpoint)
            time.sleep(self._app_config.check_interval)
