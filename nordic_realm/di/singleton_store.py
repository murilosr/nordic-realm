import logging
from inspect import isclass
from typing import Any, Dict, Generic, Type, TypeVar

from .exceptions import ComponentNotRegistered

log = logging.getLogger("nordic_realm.di")
T = TypeVar("T")


class SingletonStore(Generic[T]):

    def __init__(self):
        self._store: Dict[str, Type] = {}

    @classmethod
    def _get_name(cls, clz: Type) -> str:
        return f"{clz.__module__}:{clz.__name__}";

    def register(self, obj: Any):
        _key = self._get_name(type(obj))
        if _key in self._store:
            log.debug(f"singleton {_key} already registered")
            return

        log.debug(f"singleton registered: {_key}")
        self._store[_key] = obj

    def get(self, clazz: Type[T]) -> T:
        if (not isclass(clazz)):
            raise TypeError(f"{clazz} is not a class")

        _name = self._get_name(clazz)
        try:
            return self._store[_name]
        except KeyError:
            raise ComponentNotRegistered()

    # def get(self):
    #     return self._store
