from importlib import import_module
from typing import TypeVar, TypeAlias, Annotated, TYPE_CHECKING, Optional

import fastapi
from starlette.authentication import AuthenticationError

from auth_server.interfaces.user_repository_provider import UserRepositoryProvider
from nordic_realm.di.injector import DIInjector
from nordic_realm.mongo import DocumentNotFound

if TYPE_CHECKING:
    from nordic_realm.application.context import ApplicationContext

T = TypeVar("T")

_ApplicationContext: Optional["ApplicationContext"] = None


def use_session(request: fastapi.Request) -> T:
    global _ApplicationContext
    if _ApplicationContext is None:
        _ApplicationContext = import_module("nordic_realm.application.context").ApplicationContext

    user_repo = DIInjector().instance(_ApplicationContext.get().component_store.get(UserRepositoryProvider))
    try:
        return user_repo.get_by_id(request.user.identity)
    except DocumentNotFound:
        raise AuthenticationError("")


AbstractUseSession: TypeAlias = Annotated[T, fastapi.Depends(use_session)]
