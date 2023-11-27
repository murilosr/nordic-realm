from inspect import isclass
from typing import Dict, Generic, Type, TypeVar

from nordic_realm.di.exceptions import ComponentNotRegistered

T = TypeVar("T")

class ComponentStore(Generic[T]):
    
    def __init__(self):
        self._store : Dict[str, Type] = {}
    
    @classmethod
    def _get_name(cls, clz: Type) -> str:
        return f"{clz.__module__}:{clz.__name__}";
    
    def register(self, clz: Type):
        _key = self._get_name(clz)
        if _key in self._store:
            # print(f"{_key} already registered")
            return
        
        print(f"registered: {clz.__module__}:{clz.__name__}")
        self._store[f"{clz.__module__}:{clz.__name__}"] = clz
        
    def get(self, clazz : T) -> T:
        if(not isclass(clazz)):
            raise TypeError(f"{clazz} is not a class")
        
        _name = self._get_name(clazz)
        try:
            return self._store[_name]
        except KeyError:
            raise ComponentNotRegistered()

    # def get(self):
    #     return self._store