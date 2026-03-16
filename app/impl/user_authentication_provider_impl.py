from app.usuario import (
    Usuario,
    UsuarioRepository,
)
from auth_server.interfaces.password_hash_provider import PasswordHashProvider
from auth_server.interfaces.user_authentication_provider import (
    AuthUser,
    IncorrectPassword,
    UserAuthenticationProvider,
    UserNotFound,
)
from nordic_realm.decorators.controller import Implement
from nordic_realm.mongo.exceptions import DocumentNotFound


@Implement(base_class=UserAuthenticationProvider)
class UserAuthenticationProviderImpl:
    password_hash_provider: PasswordHashProvider
    usuario_repo: UsuarioRepository

    def authenticate_by_password(self, username: str, password: str):
        try:
            user = self.usuario_repo.get_by_email(username)
            assert user.id is not None
        except DocumentNotFound:
            raise UserNotFound("User not found")

        if not self.password_hash_provider.verify(user.senha, password):
            raise IncorrectPassword("Incorrect password")

        return AuthUser(user.id, user.email)

    def find_user_by_email(self, email: str) -> Usuario | None:
        return self.usuario_repo.find_by_email(email)
