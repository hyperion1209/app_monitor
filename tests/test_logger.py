import logging
from pathlib import Path
from app_monitor.logger import set_file_handler, LOGGER
import tempfile


def test_set_file_handler():
    # Setup
    tmp_file = tempfile.NamedTemporaryFile()

    # Exercise
    set_file_handler(log_path=Path(tmp_file.name))

    # Assert
    for handler in LOGGER.handlers:
        if isinstance(handler, logging.FileHandler):
            assert handler.baseFilename == tmp_file.name
