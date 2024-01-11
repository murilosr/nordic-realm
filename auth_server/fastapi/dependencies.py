import fastapi
from starlette.authentication import AuthenticationError

from app.user.repository import UserRepository
from app.user.service import UserService
from app.user.user import User
from nordic_realm.di.injector import DIInjector
from nordic_realm.mongo import DocumentNotFound


def use_session(request: fastapi.Request) -> User:
    user_repo = DIInjector().instance(UserRepository)
    try:
        return user_repo.get_by_id(request.user.identity)
    except DocumentNotFound:
        raise AuthenticationError("")
