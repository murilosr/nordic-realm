from http import HTTPStatus
from typing_extensions import Literal, Type, Callable, Any

def Component(*args, **kwargs):
    def wrapper(*args2, **kwargs2):
        print(args, kwargs, args2, kwargs2)
        args2[0]._NR_component = True
        return args2[0]
    return wrapper

def Controller(path: str, *args, **kwargs):
    def wrapper(*args2, **kwargs2):
        Component()(args2[0])
        args2[0]._NR_path = path
        args2[0]._NR_type = "controller"
        return args2[0]
    return wrapper

def Service(*args, **kwargs):
    def wrapper(*args2, **kwargs2):
        Component()(args2[0])
        args2[0]._NR_type = "service"
        return args2[0]
    return wrapper

def Repository(collection : str, db : str, *args, **kwargs):
    def wrapper(*args2, **kwargs2):
        Component()(args2[0])
        args2[0]._NR_type = "repository"
        args2[0].mro()[0]._DB = db
        args2[0].mro()[0]._COLLECTION = collection
        return args2[0]
    return wrapper

def MethodRouteMap(method: Literal["GET"] | Literal["POST"]):
    def outer_wrapper(
        path : str,
        response_model : Type = None,
        response_code : HTTPStatus | int | None = None,
        public : bool = False
    ):
        def wrapper(f : Callable[..., Any], *args2, **kwargs2):
            f._NR_path = path
            f._NR_method = method
            f._NR_type = "controller_method"
            if response_model is not None:
                f._NR_response_model = response_model
            f._NR_response_code = response_code
            f._NR_public_path = public
            return f
        return wrapper
    return outer_wrapper

def Get(
    path : str,
    response_model : Type = None,
    response_code : HTTPStatus | int | None = None,
    public : bool = False
):
    return MethodRouteMap("GET")(path, response_model, response_code, public)

def Post(
    path : str,
    response_model : Type = None,
):
    return MethodRouteMap("POST")(path, response_model)