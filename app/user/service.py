import random
from uuid import uuid4
from app.auth_server.interfaces.password_hash_provider import PasswordHashProvider
from app.user.repository import UserRepository
from app.user.user import User
from nordic_realm.decorators.controller import Service
from nordic_realm.mongo.operations import MongoOperations


@Service()
class UserService:
    
    user_repo : UserRepository
    password_hash_provider : PasswordHashProvider

    def get_user_by_email(self, email : str) -> User:
        return self.user_repo.get_by_email(email)

    def create(self) -> User:
        rand = random.randint(0,10)
        email = f"{rand}@test.com"
        if(self.user_repo.exists_by_email(email)):
            raise Exception("Email already exists")
        return self.user_repo.save(
            User(
                _id=uuid4().hex,
                name=str(rand),
                email=email,
                password=self.password_hash_provider.hash("123456")
            )
        )