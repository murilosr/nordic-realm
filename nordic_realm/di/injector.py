from datetime import datetime
import logging
from inspect import isclass
import time
from typing import Annotated, Any, Generic, Optional, Type, TypeVar, ClassVar, Dict
from typing_extensions import _AnnotatedAlias

from nordic_realm.application import ApplicationContext

from .annotations import Config
from .exceptions import ComponentNotRegistered, IgnoreInjection

T = TypeVar("T")
log = logging.getLogger("nordic_realm.di")

class DIInjector(Generic[T]):
    
    def __init__(self, app_context : Optional[ApplicationContext] = None, use_cache : bool = True):
        self.app_context = app_context if app_context is not None else ApplicationContext.get()
        self._use_cache = use_cache
        self._obj_cache : Dict[str, Any] = {}
        
    @classmethod
    def _get_name(cls, clz: Type) -> str:
        return f"{clz.__module__}:{clz.__name__}"
    
    def _is_cached(self, class_name : str) -> Any:
        return class_name in self._obj_cache
    
    def _set_cache(self, class_name : str, obj : Any):
        if(self._use_cache):
            self._obj_cache[class_name] = obj
    
    def _get_object(self, annotation_type : Type):
        _clazz : Type
        
        if(isinstance(annotation_type, Annotated)):
            log.debug(f"{annotation_type} is annotated")
            _clazz : Type = annotation_type.__args__[0]
            for _ann in annotation_type.__args__[1:]:
                if(isinstance(_ann, Config)):
                    return self.app_context.config_store.get(_ann.path)
                elif(_ann == ClassVar):
                    raise IgnoreInjection()
        elif(isinstance(annotation_type, _AnnotatedAlias)):
            _clazz = annotation_type.__args__[0]
            for _ann in annotation_type.__metadata__:
                if(isinstance(_ann, Config)):
                    return self.app_context.config_store.get(_ann.path)
                elif(_ann == ClassVar):
                    raise IgnoreInjection()
        elif(isclass(annotation_type)):
            log.debug(f"{annotation_type} is class")
            _clazz = annotation_type
        else:
            raise Exception(f"not supposed to be here {annotation_type}")
        
        clazz_name = self._get_name(_clazz)
        if self._use_cache and self._is_cached(clazz_name):
            return self._obj_cache[clazz_name]
        
        # Check if it is singleton
        try:
            _singleton_obj = self.app_context.singleton_store.get(_clazz)
            log.debug(f"{annotation_type} is a singleton")
            self._set_cache(clazz_name, _singleton_obj)
            return _singleton_obj
        except ComponentNotRegistered:
            log.debug(f"{annotation_type} not a singleton")
            pass
        
        try:
            _clazz = ApplicationContext.get().component_store.get(_clazz)
            log.debug(f"{annotation_type} is a component")
        except ComponentNotRegistered as err:
            log.debug(f"{annotation_type} not a component")
            raise err
        
        _new_subobject = self.instance(_clazz)
        
        if(hasattr(_new_subobject, "_post_init") and callable(_new_subobject._post_init)): # type: ignore
            _new_subobject._post_init() # type: ignore
        
        self._set_cache(clazz_name, _new_subobject)
        return _new_subobject
            
    
    def instance(self, clazz : Type[T], _new_obj : T | None = None) -> T: # type: ignore
        _is_root = False
        if(_new_obj is None):
            _is_root = True
            log.debug(f"Injector: instancing a new object of type {clazz}")
            _new_obj : T = ApplicationContext.get().component_store.get(clazz)()
        
        if(hasattr(clazz, "__annotations__")):
            for _ank, _anv in clazz.__annotations__.items():
                log.debug(f"Field {_ank} - ")
                try:
                    log.debug(f"{self._get_object(_anv)}")
                    setattr(_new_obj, _ank, self._get_object(_anv))
                except ComponentNotRegistered:
                    log.debug("Not registered")
                    continue
                except IgnoreInjection:
                    continue
        
        for _parent_class in clazz.mro()[1:]:
            self.instance(_parent_class, _new_obj) # type: ignore

        if _is_root:
            if hasattr(_new_obj, "_post_init") and callable(_new_obj._post_init):  # type: ignore
                _new_obj._post_init()  # type: ignore
        
        return _new_obj
    