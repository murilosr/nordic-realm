import random
from uuid import uuid4
from auth_server.interfaces.password_hash_provider import PasswordHashProvider
from app.user.repository import UserRepository
from app.user.user import User
from nordic_realm.decorators.controller import Service
from nordic_realm.mongo.exceptions import DocumentNotFound
from nordic_realm.mongo.operations import MongoOperations


@Service()
class UserService:
    
    user_repo : UserRepository
    password_hash_provider : PasswordHashProvider

    def get_user_by_email(self, email : str) -> User:
        return self.user_repo.get_by_email(email)

    def find_user_by_email(self, email : str) -> User | None:
        try:
            return self.user_repo.get_by_email(email)
        except DocumentNotFound:
            return None

    def create(self, name : str, email : str) -> User:
        return self.user_repo.save(
            User(
                _id=uuid4().hex,
                name=name,
                email=email,
                password=self.password_hash_provider.hash("123456")
            )
        )