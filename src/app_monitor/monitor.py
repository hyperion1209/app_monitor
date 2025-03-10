"""Module contains the logic for the serial application monitor."""

import requests
import time
from requests.adapters import Retry
from app_monitor.app_config import AppConfig
from app_monitor.logger import LOGGER, send_slack_notification


class AppMonitor:
    """Serial application monitor"""

    RUN = True

    def __init__(self, app_config: AppConfig) -> None:
        self._app_config: AppConfig = app_config

    def _setup_session(self) -> requests.Session:
        """Set up a session with retries

        Returns:
            requests.Session: The session object
        """
        session = requests.Session()
        adapter = requests.adapters.HTTPAdapter(
            max_retries=Retry(
                total=self._app_config.retries, status_forcelist=[500, 502]
            )
        )
        session.mount("http://", adapter)
        return session

    def probe_endpoint(self, endpoint: str) -> None:
        """Probe an endpoints and log the result

        Args:
            endpoint (str): The endpoint to probe
        """
        session = self._setup_session()

        t = time.time()
        try:
            response = session.get(endpoint)
        except requests.exceptions.RetryError:
            LOGGER.error(f"All retries failed when probing endpoint {endpoint}")
            return

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

    def probe_all_endpoints(self) -> None:
        """Probe all endpoints"""
        for endpoint in self._app_config.endpoints:
            self.probe_endpoint(endpoint)
        time.sleep(self._app_config.check_interval)

    def run(self) -> None:
        """Run the monitor"""
        while self.RUN:
            self.probe_all_endpoints()
