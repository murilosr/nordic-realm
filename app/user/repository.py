from app.user.user import User
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo.operations import MongoOperations
from nordic_realm.mongo_repository import MongoRepository

@Repository("users", db="pytest")
class UserRepository(MongoRepository[User, str]):
    
    def get_by_email(self, email : str) -> User:
        return MongoOperations.find_one_and_only_one(
            self._MONGO,
            {"email": email},
            User,
            raise_not_found=True
        )
    
    def exists_by_email(self, email : str) -> bool:
        return MongoOperations.exists(
            self._MONGO,
            {"email": email},
        )