import bcrypt
from starlette.authentication import AuthenticationError

from nordic_realm.decorators.controller import Component


@Component()
class PasswordHashProvider:

    def hash(self, plaintext_password: str) -> str:
        return bcrypt.hashpw(plaintext_password.encode("utf-8"), bcrypt.gensalt(12)).decode("utf-8")

    def verify(self, hashed_password: str | None, possible_plaintext_password: str) -> bool:
        if hashed_password is None:
            raise AuthenticationError("Password login not available for user")
        return bcrypt.checkpw(
            possible_plaintext_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
