import json
import logging

from pathlib import Path
from typing import Any

logger: logging.Logger = logging.getLogger(__name__)


class ConfigError(Exception):
    """Configuration error."""


def load_json_config(path: str) -> dict[str, Any]:
    """
    Load JSON config file.

    Raises:
        ConfigError: If config cannot be loaded.
    """

    config_file = Path(path)
    try:
        if not config_file.exists():
            raise ConfigError(f"Config file not found: {path}.")

        with config_file.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            ConfigError(
                f"Error: {path} must contain a JSON object, got {type(data).__name__}"
            )
        logger.debug(f"Loaded config: {path}")
        return data

    except json.JSONDecodeError as e:
        raise ConfigError(f"Error encoding JSON in {path}: {e}") from e
    except PermissionError as e:
        raise ConfigError(f"Permission denied reading {path}: {e}") from e
    except OSError as e:
        raise ConfigError(f"Error reading file {path}: {e}") from e
