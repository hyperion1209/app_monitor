import asyncio
from typing import NamedTuple
from app_monitor.app_config import AppConfig
from app_monitor.logger import LOGGER, send_slack_notification
import httpx


class ProbeResult(NamedTuple):
    endpoint: str
    status_code: int
    response_time: float


async def probe_endpoint(
    client: httpx.AsyncClient, endpoint: str
) -> ProbeResult:
    resp = await client.get(endpoint, timeout=5, follow_redirects=True)
    resp.raise_for_status()
    return ProbeResult(
        endpoint=endpoint,
        status_code=resp.status_code,
        response_time=resp.elapsed.total_seconds(),
    )


async def check_endpoint_health(
    client: httpx.AsyncClient, endpoint: str, warn_threshold: float | int
) -> None:
    try:
        probe_result = await probe_endpoint(client, endpoint)
    except httpx.HTTPStatusError as exc:
        msg = (
            f"Endpoint {endpoint} returned status "
            f"code {exc.response.status_code}"
        )
        LOGGER.error(msg)
        send_slack_notification(msg)
    else:
        if probe_result.response_time > warn_threshold:
            LOGGER.warning(
                f"Endpoint {endpoint} took too long to respond: "
                f"{probe_result.response_time:.2f} seconds"
            )


async def supervisor(app_config: AppConfig) -> None:
    async with httpx.AsyncClient() as client:
        while True:
            tasks = [
                check_endpoint_health(
                    client, endpoint, app_config.warn_threshold
                )
                for endpoint in app_config.endpoints
            ]
            await asyncio.gather(*tasks)
            await asyncio.sleep(app_config.check_interval)
