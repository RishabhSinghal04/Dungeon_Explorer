import json
from pathlib import Path
from typing import Any


def load_json_config(path: str) -> Any:
    config_file = Path(path)
    with config_file.open() as f:
        return json.load(f)
