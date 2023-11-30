import logging
from inspect import isclass
from typing import Annotated, Generic, Optional, Type, TypeVar, ClassVar
from typing_extensions import _AnnotatedAlias

from nordic_realm.application import ApplicationContext

from .annotations import Config
from .exceptions import ComponentNotRegistered, IgnoreInjection

T = TypeVar("T")
log = logging.getLogger("nordic_realm.di")

class DIInjector(Generic[T]):
    
    def __init__(self, app_context : Optional[ApplicationContext] = None):
        self.app_context = app_context if app_context is not None else ApplicationContext.get()
        
    @classmethod
    def _get_name(cls, clz: Type) -> str:
        return f"{clz.__module__}:{clz.__name__}"
    
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
        
        # Check if it is singleton
        try:
            _singleton_obj = self.app_context.singleton_store.get(_clazz)
            log.debug(f"{annotation_type} is a singleton")
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
        
        return _new_subobject
            
    
    def instance(self, clazz : Type[T], _new_obj : T | None = None) -> T: # type: ignore
        if(_new_obj is None):
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
        
        return _new_obj
    