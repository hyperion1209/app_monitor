import asyncio
from typing import NamedTuple, Optional

from httpx._transports import AsyncHTTPTransport
from app_monitor.app_config import AppConfig
from app_monitor.logger import LOGGER, send_slack_notification
import httpx


class ProbeResult(NamedTuple):
    endpoint: str
    status_code: int
    response_time: float


class AsyncAppMonitor:
    RUN = True

    def __init__(self, app_config: AppConfig) -> None:
        self._app_config: AppConfig = app_config

    async def probe_endpoint(
        self, client: httpx.AsyncClient, endpoint: str
    ) -> Optional[ProbeResult]:
        attempt = 0
        while attempt < self._app_config.retries:
            try:
                resp = await client.get(endpoint, timeout=5, follow_redirects=True)
                resp.raise_for_status()
                return ProbeResult(
                    endpoint=endpoint,
                    status_code=resp.status_code,
                    response_time=resp.elapsed.total_seconds(),
                )
            except (httpx.ConnectError, httpx.ConnectTimeout):
                attempt += 1
                if attempt == self._app_config.retries:
                    raise

    async def check_endpoint_health(
        self,
        client: httpx.AsyncClient,
        endpoint: str,
        warn_threshold: float | int,
    ) -> None:
        try:
            probe_result = await self.probe_endpoint(client, endpoint)
        except httpx.HTTPStatusError as exc:
            msg = (
                f"Endpoint {endpoint} returned status "
                f"code {exc.response.status_code}"
            )
            LOGGER.error(msg)
            send_slack_notification(msg)
        except (httpx.ConnectError, httpx.ConnectTimeout) as exc:
            msg = f"Endpoint {endpoint} is unreachable: {exc}"
            LOGGER.error(msg)
            send_slack_notification(msg)
        else:
            if probe_result is not None and probe_result.response_time > warn_threshold:
                LOGGER.warning(
                    f"Endpoint {endpoint} took too long to respond: "
                    f"{probe_result.response_time:.2f} seconds"
                )

    async def supervisor(self) -> None:
        transport = AsyncHTTPTransport(retries=3)
        async with httpx.AsyncClient(transport=transport) as client:
            while self.RUN:
                tasks = [
                    self.check_endpoint_health(
                        client, endpoint, self._app_config.warn_threshold
                    )
                    for endpoint in self._app_config.endpoints
                ]
                await asyncio.gather(*tasks)
                await asyncio.sleep(self._app_config.check_interval)
