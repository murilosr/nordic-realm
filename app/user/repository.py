from app.user.user import User
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo import MongoRepository, MongoOperations


@Repository("users")
class UserRepository(MongoRepository[User, str]):

    def get_by_email(self, email: str) -> User:
        return MongoOperations.find_one_and_only_one(
            self._MONGO,
            {"email": email},
            User,
            raise_not_found=True
        )  # type: ignore

    def exists_by_email(self, email: str) -> bool:
        return MongoOperations.exists(
            self._MONGO,
            {"email": email},
        )
