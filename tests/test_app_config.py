from pathlib import Path
import pytest
import tempfile

from app_monitor.app_config import AppConfig, ConfigValidationError, load_config


@pytest.mark.parametrize(
    "config, expected",
    [
        (  # Valid configuration
            """
            {
                "check_interval": 10,
                "warn_threshold": 1.0,
                "endpoints": [
                    "http://example1.com",
                    "http://example2.com"
                ]
            }
            """,
            AppConfig(
                check_interval=10,
                warn_threshold=1.0,
                endpoints=["http://example1.com", "http://example2.com"],
            ),
        ),
        (
            """
            bad config
            """,
            ConfigValidationError,
        ),
        (  # Missing endpoints
            """
            {
                "check_interval": 10,
                "warn_threshold": 1.0
            }
            """,
            ConfigValidationError,
        ),
        (  # Endpoints is not a list
            """
            {
                "check_interval": 10,
                "warn_threshold": 1.0,
                "endpoints": "http://example1.com"
            }
            """,
            ConfigValidationError,
        ),
        (  # Endpoints list is empty
            """
            {
                "check_interval": 10,
                "warn_threshold": 1.0,
                "endpoints": []
            }
            """,
            ConfigValidationError,
        ),
        (  # Invalid URL
            """
            {
                "check_interval": 10,
                "warn_threshold": 1.0,
                "endpoints": [
                    "http://example1",
                    "http://example2.com"
                ]
            }
            """,
            ConfigValidationError,
        ),
        (  # Missing check_interval
            """
            {
                "warn_threshold": 1.0,
                "endpoints": [
                    "http://example1.com",
                    "http://example2.com"
                ]
            }
            """,
            ConfigValidationError,
        ),
        (  # check_interval is not an integer
            """
            {
                "check_interval": "string",
                "warn_threshold": 1.0,
                "endpoints": [
                    "http://example1.com",
                    "http://example2.com"
                ]
            }
            """,
            ConfigValidationError,
        ),
        (  # Missing warn_threshold
            """
            {
                "check_interval": 10,
                "endpoints": [
                    "http://example1.com",
                    "http://example2.com"
                ]
            }
            """,
            ConfigValidationError,
        ),
        (  # warn_threshold is not a number
            """
            {
                "check_interval": 10,
                "warn_threshold": "string",
                "endpoints": [
                    "http://example1.com",
                    "http://example2.com"
                ]
            }
            """,
            ConfigValidationError,
        ),
    ],
)
def test_load_config(config, expected):
    # Setup
    test_cfg_file = tempfile.NamedTemporaryFile(mode="w+")
    with open(test_cfg_file.name, "w") as f:
        f.write(config)

    # Exercise
    if isinstance(expected, AppConfig):
        result = load_config(Path(test_cfg_file.name))

        # Assert
        assert result == expected
    else:
        with pytest.raises(expected):
            load_config(Path(test_cfg_file.name))
