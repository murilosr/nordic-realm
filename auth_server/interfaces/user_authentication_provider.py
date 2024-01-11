from starlette.authentication import BaseUser

from auth_server.dtos.open_id_profile import OpenIdProfile
from nordic_realm.decorators.controller import Component


class LoginError(Exception):
    pass


class IncorrectPassword(LoginError):
    pass


class UserNotFound(LoginError):
    pass


class AuthUser(BaseUser):
    def __init__(self, id: str, username: str) -> None:
        self.id = id
        self.username = username

    @property
    def is_authenticated(self) -> bool:
        return True

    @property
    def display_name(self) -> str:
        return self.username

    @property
    def identity(self) -> str:
        return self.id


class UserInterface:
    id: str
    name: str
    email: str
    password: str


@Component()
class UserAuthenticationProvider:

    def authenticate_by_password(self, username: str, password: str) -> BaseUser:
        raise NotImplementedError("This must be overriden")

    def find_user_by_email(self, email: str) -> UserInterface | None:
        raise NotImplementedError("This must be overriden")

    def create_user(self, profile: OpenIdProfile) -> UserInterface:
        raise NotImplementedError("This must be overriden")
