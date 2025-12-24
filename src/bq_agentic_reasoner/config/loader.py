from pathlib import Path
from typing import Dict, Any
import yaml


_CONFIG_FILES = [
    "hf_models",
    "thresholds",
    "security",
    "firestore",
    "pipeline",
    "learning_weights",
]


class ConfigLoader:
    """
    Loads and merges configuration files.
    """

    def __init__(self, base_dir: Path):
        self.base_dir = base_dir

    def _load_yaml(self, path: Path) -> Dict[str, Any]:
        if not path.exists():
            return {}
        with open(path, "r") as f:
            return yaml.safe_load(f) or {}

    def load(self, override_dir: str | None = None) -> Dict[str, Dict[str, Any]]:
        config: Dict[str, Dict[str, Any]] = {}
        for name in _CONFIG_FILES:
            config[name] = self._load_yaml(self.base_dir / f"{name}.yaml")
        if override_dir:
            override_path = Path(override_dir)
            for name in _CONFIG_FILES:
                override = self._load_yaml(override_path / f"{name}.yaml")
                if override:
                    config[name].update(override)

        return config


def load_config(override_dir: str | None = None) -> Dict[str, Dict[str, Any]]:
    """
    Public API to load configuration.

    override_dir:
        Optional directory containing YAML overrides.
    """
    base_dir = Path(__file__).parent
    loader = ConfigLoader(base_dir)
    return loader.load(override_dir)
