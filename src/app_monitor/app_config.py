import json
from pathlib import Path
from dataclasses import dataclass


@dataclass
class AppConfig:
    endpoints: list[str]
    check_interval: int
    warn_threshold: int


def load_config(config_path: Path) -> AppConfig:
    with open(config_path, "r") as file:
        raw_config = json.load(file)
        return AppConfig(**raw_config)
