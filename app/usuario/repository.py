from app.usuario.usuario import Usuario
from auth_server.interfaces.user_repository_provider import UserRepositoryProvider
from nordic_realm.decorators.controller import Implement, Repository
from nordic_realm.mongo import MongoOperations, MongoRepository
from nordic_realm.mongo.exceptions import DocumentNotFound


@Implement(UserRepositoryProvider)
@Repository("users")
class UsuarioRepository(MongoRepository[Usuario, str]):
    def get_by_email(self, email: str) -> Usuario:
        return MongoOperations.find_one_and_only_one(
            self._MONGO, {"email": email}, Usuario, raise_not_found=True
        )  # type: ignore

    def exists_by_email(self, email: str) -> bool:
        return MongoOperations.exists(
            self._MONGO,
            {"email": email},
        )

    def find_by_email(self, email: str) -> Usuario | None:
        try:
            return self.get_by_email(email)
        except DocumentNotFound:
            return None
