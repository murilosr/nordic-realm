from typing import Any, Dict

from pymongo import MongoClient


class MongoConnections:

    def __init__(self):
        self._connections: Dict[str, MongoClient] = {}

    def get(self, name: str | None = None) -> MongoClient:
        if name is None:
            name = "__default"
        return self._connections[name]

    def register(self, name: str | None, params: Dict[Any, Any]):
        if name is None:
            name = "__default"
        self._connections[name] = MongoClient(**params, tz_aware=True)
