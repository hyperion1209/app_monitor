import json
from pathlib import Path
import validators
from typing import NamedTuple
from json.decoder import JSONDecodeError


class AppConfig(NamedTuple):
    endpoints: list[str]
    check_interval: int
    warn_threshold: float | int


class ConfigValidationError(Exception):
    """Raised when the configuration is invalid."""


def validate_config(raw_config: dict) -> None:
    if "endpoints" not in raw_config:
        raise ConfigValidationError("Missing 'endpoints' key in configuration")

    if not isinstance(raw_config["endpoints"], list):
        raise ConfigValidationError("'endpoints' must be a list of URLs")

    if not raw_config["endpoints"]:
        raise ConfigValidationError("'endpoints' list must not be empty")

    for endpoint in raw_config["endpoints"]:
        if not validators.url(endpoint):
            raise ConfigValidationError(f"Invalid URL: {endpoint}")

    if "check_interval" not in raw_config:
        raise ConfigValidationError(
            "Missing 'check_interval' key in configuration"
        )

    if not isinstance(raw_config["check_interval"], int):
        raise ConfigValidationError("'check_interval' must be an integer")

    if "warn_threshold" not in raw_config:
        raise ConfigValidationError(
            "Missing 'warn_threshold' key in configuration"
        )

    if not isinstance(raw_config["warn_threshold"], (int, float)):
        raise ConfigValidationError("'warn_threshold' must be a number")


def load_config(config_path: Path) -> AppConfig:
    with open(config_path, "r") as file:
        try:
            raw_config = json.load(file)
        except JSONDecodeError as exc:
            raise ConfigValidationError(
                "Invalid JSON in configuration file"
            ) from exc
        validate_config(raw_config)
        res = AppConfig(**raw_config)
        return res
