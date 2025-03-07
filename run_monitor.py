#!/usr/bin/env python
import argparse
from pathlib import Path
from app_monitor.logger import set_file_handler
from app_monitor.monitor import AppMonitor
from app_monitor.async_monitor import supervisor
from app_monitor.app_config import load_config
import asyncio


def _parse_args():
    parser = argparse.ArgumentParser(description="Web app monitoring tool")
    parser.add_argument(
        "--config",
        type=str.lower,
        help=("Path of the configuration file"),
    )
    parser.add_argument(
        "--log",
        type=str.lower,
        help=("Path of the log file"),
        default="app_monitor.log",
    )
    return parser.parse_args()


# def main(args: argparse.Namespace):
#     app_config = load_config(Path(args.config))

#     # Set up log file
#     log_path = Path(args.log)
#     set_file_handler(log_path)

#     # Start monitor
#     app_monitor = AppMonitor(app_config)
#     app_monitor.start()


def main(args: argparse.Namespace):
    app_config = load_config(Path(args.config))

    # Set up log file
    log_path = Path(args.log)
    set_file_handler(log_path)

    # Start monitor
    coro = supervisor(app_config)
    asyncio.run(coro)


if __name__ == "__main__":
    try:
        main(_parse_args())
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user via keyboard interrupt!")
