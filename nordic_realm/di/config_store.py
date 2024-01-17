from functools import reduce
from typing import Any, Dict, List

import yaml


def _get_value_from_dict_path_internal(_d: Dict[str, Any], _k: str) -> Any:
    return _d.get(_k)


def get_value_from_dict_path(path: str, initial: Dict[str, Any]) -> Any:
    return reduce(_get_value_from_dict_path_internal, path.split('.'), initial)


class ConfigStore:

    def __init__(self, files: List[str] | None = None):
        self._files = files if files is not None else ["./config.yaml", "./secrets.yaml"]
        self._store = self._read_files()
        self._overrides = {}

    def _read_files(self) -> Dict[str, Any]:
        _store: Dict[str, Any] = {}
        for _filename in self._files:
            with open(_filename, 'rt') as file:
                _store.update(yaml.safe_load(file))
        return _store

    def get(self, path: str) -> Any:
        if path in self._overrides:
            return self._overrides[path]

        try:
            return get_value_from_dict_path(path, self._store)
        except (TypeError, KeyError):
            raise KeyError(f"{path} not found in config.yaml")

    def register_override(self, key: str, value: Any):
        self._overrides[key] = value
