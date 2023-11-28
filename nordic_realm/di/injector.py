from pickletools import int4
from typing import Annotated, Any, Dict, Generic, Optional, Type, TypeVar
from nordic_realm.application.context import ApplicationContext
from inspect import isclass

from nordic_realm.di.exceptions import ComponentNotRegistered

T = TypeVar("T")

class DIInjector(Generic[T]):
    
    def __init__(self, app_context : Optional[ApplicationContext] = None):
        self.app_context = app_context if app_context is not None else ApplicationContext.get()
        
    @classmethod
    def _get_name(cls, clz: Type) -> str:
        return f"{clz.__module__}:{clz.__name__}"
    
    def _get_object(self, annotation_type : Type):
        _clazz : type
        if(isinstance(annotation_type, Annotated)):
            #print(f"{annotation_type} is annotated")
            _clazz = annotation_type.__args__[0]
        elif(isclass(annotation_type)):
            #print(f"{annotation_type} is class")
            _clazz = annotation_type
        else:
            raise Exception(f"not supposed to be here {annotation_type}")
        
        # Check if it is singleton
        try:
            _singleton_obj = self.app_context.singleton_store.get(_clazz)
            # print(f"{annotation_type} is a singleton")
            return _singleton_obj
        except ComponentNotRegistered:
            # print(f"{annotation_type} not a singleton")
            pass
        
        try:
            _clazz = ApplicationContext.get().component_store.get(_clazz)
            # print(f"{annotation_type} is a component")
        except ComponentNotRegistered as err:
            # print(f"{annotation_type} not a component")
            raise err
        _new_subobject = self.instance(_clazz)
        
        if(hasattr(_new_subobject, "_post_init") and callable(_new_subobject._post_init)):
            _new_subobject._post_init()
        
        return _new_subobject
            
    
    def instance(self, clazz : Type[T], _new_obj : T | None = None) -> T:
        if(_new_obj is None):
            #print(f"Injector: instancing a new object of type {clazz}")
            _new_obj : T = ApplicationContext.get().component_store.get(clazz)()
        
        if(hasattr(clazz, "__annotations__")):
            for _ank, _anv in clazz.__annotations__.items():
                # print(f"Field {_ank} - ", end="")
                try:
                    # print(f"{self._get_object(_anv)}")
                    setattr(_new_obj, _ank, self._get_object(_anv))
                except ComponentNotRegistered:
                    # print("Not registered")
                    continue
        
        for _parent_class in clazz.mro()[1:]:
            self.instance(_parent_class, _new_obj)
        
        return _new_obj
    