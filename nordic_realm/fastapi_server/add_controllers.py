import inspect
import re

from starlette.routing import compile_path

from nordic_realm.application.context import ApplicationContext
from nordic_realm.di.injector import DIInjector


def instance_obj_endpoint(clz, method, context: ApplicationContext):
    def wrapper_sync(*args, **kwargs):  # pragma: nocover
        c = DIInjector(context).instance(clz)
        return getattr(c, method.__name__)(*args, **kwargs)

    async def wrapper_async(*args, **kwargs):  # pragma: nocover
        c = DIInjector(context).instance(clz)
        return await getattr(c, method.__name__)(*args, **kwargs)

    wrapper = wrapper_sync
    if inspect.iscoroutinefunction(method):  # pragma: nocover
        wrapper = wrapper_async

    method_sig = inspect.signature(method)
    new_parameters = [p for (p_name, p,) in method_sig.parameters.items() if p_name != "self"]
    wrapper_sig = inspect.signature(wrapper).replace(parameters=new_parameters)
    wrapper.__signature__ = wrapper_sig

    return wrapper


def add_controllers(context: ApplicationContext):
    app = context.fastapi_app
    app._NR_public_paths = [re.compile("/docs[$|/*$]"), re.compile("/openapi.json")]  # type: ignore
    for _v in context.component_store._store.values():
        if isinstance(_v, type):
            if "_NR_type" in _v.__dict__ and _v._NR_type == "controller":
                base_path = _v._NR_path  # type: ignore

                sorted_routes = []
                for _controller_method in _v.__dict__.values():
                    """Here it is identified which methods are annotated with nordic-realm's decorators, and 
                    added to sorted_routes together with the index of the first {, which is the signal that a Path
                    parameter exists. After this, it is sorted to add the paths that don't have Path parameters first
                    """
                    if callable(_controller_method):
                        if "_NR_type" in dir(_controller_method):
                            if _controller_method._NR_type == "controller_method":
                                sorted_routes.append((_controller_method._NR_path.find("{"), _controller_method,))
                sorted_routes.sort(key=lambda _item: _item[0])

                for _, _controller_method in sorted_routes:
                    method_path = _controller_method._NR_path
                    full_path = f"{base_path}{method_path}"
                    method_http_method = _controller_method._NR_method
                    response_status_code = _controller_method._NR_response_code

                    extra_kwargs = {}
                    if hasattr(_controller_method, "_NR_response_model"):
                        extra_kwargs["response_model"] = _controller_method._NR_response_model

                    if method_http_method == "WEBSOCKET":
                        app.add_websocket_route(
                            path=full_path,
                            route=instance_obj_endpoint(_v, _controller_method, context),
                        )
                    else:
                        app.add_api_route(
                            path=full_path,
                            endpoint=instance_obj_endpoint(_v, _controller_method, context),
                            methods=[method_http_method, "OPTIONS"],
                            status_code=response_status_code,
                            **extra_kwargs
                        )
                        if (hasattr(_controller_method,
                                    "_NR_public_path") and _controller_method._NR_public_path):
                            app._NR_public_paths.append(compile_path(full_path)[0])  # type: ignore
