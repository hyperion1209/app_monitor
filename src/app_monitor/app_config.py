import json
from pathlib import Path
import validators
from typing import NamedTuple


class AppConfig(NamedTuple):
    endpoints: list[str]
    check_interval: int
    warn_threshold: float | int


def validate_config(raw_config: dict) -> None:
    if "endpoints" not in raw_config:
        raise ValueError("Missing 'endpoints' key in configuration")

    if not isinstance(raw_config["endpoints"], list):
        raise ValueError("'endpoints' must be a list of URLs")

    for endpoint in raw_config["endpoints"]:
        if not validators.url(endpoint):
            raise ValueError(f"Invalid URL: {endpoint}")

    if "check_interval" not in raw_config:
        raise ValueError("Missing 'check_interval' key in configuration")

    if not isinstance(raw_config["check_interval"], int):
        raise ValueError("'check_interval' must be an integer")

    if "warn_threshold" not in raw_config:
        raise ValueError("Missing 'warn_threshold' key in configuration")

    if not isinstance(raw_config["warn_threshold"], (int, float)):
        raise ValueError("'warn_threshold' must be a number")


def load_config(config_path: Path) -> AppConfig:
    with open(config_path, "r") as file:
        raw_config = json.load(file)
        print(raw_config)
        validate_config(raw_config)
        res = AppConfig(**raw_config)
        return res
