from app.user.repository import UserRepository
from app.user.user import User
from auth_server.interfaces.password_hash_provider import PasswordHashProvider
from nordic_realm.decorators.controller import Service
from nordic_realm.mongo.exceptions import DocumentNotFound
from nordic_realm.utils import generate_id


@Service()
class UserService:
    user_repo: UserRepository
    password_hash_provider: PasswordHashProvider

    def get_user_by_email(self, email: str) -> User:
        return self.user_repo.get_by_email(email)

    def find_user_by_email(self, email: str) -> User | None:
        try:
            return self.user_repo.get_by_email(email)
        except DocumentNotFound:
            return None

    def create(self, name: str, email: str) -> User:
        return self.user_repo.save(
            User(
                id=generate_id(),
                name=name,
                email=email,
                password=self.password_hash_provider.hash("123456")
            )
        )
