#!/usr/bin/env python
import argparse
import logging
from pathlib import Path
import sys
from app_monitor.logger import set_file_handler, set_logging_level
from app_monitor.monitor import AppMonitor
from app_monitor.async_monitor import AsyncAppMonitor
from app_monitor.app_config import load_config
import asyncio


def _build_parser():
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
    parser.add_argument(
        "--no-async",
        action="store_true",
        help=("Toggle between serial and async monitoring"),
        default=False,
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help=("Toggle debug mode"),
        default=False,
    )
    return parser


def main(args: argparse.Namespace):
    app_config = load_config(Path(args.config))

    # Set up logging
    log_path = Path(args.log)
    set_file_handler(log_path)
    if args.debug:
        set_logging_level(logging.DEBUG)

    # Start monitor
    if args.no_async:
        app_monitor = AppMonitor(app_config)
        app_monitor.run()
    else:
        app_monitor = AsyncAppMonitor(app_config)
        coro = app_monitor.supervisor()
        asyncio.run(coro)


if __name__ == "__main__":
    try:
        parser = _build_parser()
        args = parser.parse_args()

        if not args.config:
            parser.print_help()
            sys.exit(1)

        main(args)
    except KeyboardInterrupt:
        raise SystemExit("Aborted by user via keyboard interrupt!")
