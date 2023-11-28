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
        is_override = False
        _key : str
        if(hasattr(clz, "_NR_base_component")):
            _key = self._get_name(clz=clz._NR_base_component)
            print(f"{self._get_name(clz)} override {_key}")
        else:
            _key = self._get_name(clz)
            if _key in self._store and hasattr(self._store[_key], "_NR_base_component"):
                return
        
        print(f"registered: {_key}")
        self._store[f"{_key}"] = clz
        
    def get(self, clazz : T) -> T:
        if(not isclass(clazz)):
            raise TypeError(f"{clazz} is not a class")
        
        _name : str
        if hasattr(clazz, "_NR_base_component"):
            _name = self._get_name(clazz._NR_base_component)
        else:
            _name = self._get_name(clazz)

        try:
            return self._store[_name]
        except KeyError:
            raise ComponentNotRegistered()

    # def get(self):
    #     return self._store