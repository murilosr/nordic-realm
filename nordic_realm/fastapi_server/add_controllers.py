import inspect
import re
from typing import List

from starlette.routing import compile_path

from nordic_realm.application.context import ApplicationContext
from nordic_realm.di.injector import DIInjector


def instance_obj_endpoint(clz, method):
    def wrapper(*args, **kwargs):
        c = DIInjector().instance(clz)
        return getattr(c,method.__name__)(*args, **kwargs)
    
    method_sig = inspect.signature(method)
    new_parameters = [p for (p_name, p,) in method_sig.parameters.items() if p_name != "self"]
    wrapper_sig = inspect.signature(wrapper).replace(parameters=new_parameters)
    wrapper.__signature__ = wrapper_sig
    
    return wrapper

def add_controllers():
    app = ApplicationContext.get().fastapi_app
    app._NR_public_paths = [re.compile("/docs[$|/*$]"), re.compile("/openapi.json")] # type: ignore
    for _v in ApplicationContext.get().component_store._store.values():
        if isinstance(_v, type):
            if("_NR_type" in _v.__dict__):
                if(_v._NR_type == "controller"): # type: ignore
                    base_path = _v._NR_path # type: ignore
                    for _controller_method in _v.__dict__.values():
                        if(callable(_controller_method)):
                            if("_NR_type" in dir(_controller_method)):
                                if(_controller_method._NR_type == "controller_method"):
                                    method_path = _controller_method._NR_path
                                    full_path = f"{base_path}{method_path}"
                                    method_http_method = _controller_method._NR_method
                                    response_status_code = _controller_method._NR_response_code
                                    app.add_api_route(
                                        path=full_path,
                                        endpoint=instance_obj_endpoint(_v, _controller_method),
                                        methods=[method_http_method, "OPTIONS"],
                                        status_code=response_status_code
                                    )
                                    if(hasattr(_controller_method, "_NR_public_path") and _controller_method._NR_public_path):
                                        app._NR_public_paths.append(compile_path(full_path)[0]) # type: ignore