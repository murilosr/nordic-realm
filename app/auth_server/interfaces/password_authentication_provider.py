from nordic_realm.decorators.controller import Component
from starlette.authentication import BaseUser, UnauthenticatedUser

class LoginError(Exception):
    pass

class IncorrectPassword(LoginError):
    pass

class UserNotFound(LoginError):
    pass

class AuthUser(BaseUser):
    def __init__(self, id : str, username: str) -> None:
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


@Component()
class PasswordAuthenticationProvider:

    def authenticate(self, username : str, password : str) -> BaseUser:
        raise NotImplementedError("This must be overriden")