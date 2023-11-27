from app.auth_server.auth_token import AuthToken
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo_repository import MongoRepository

@Repository(collection="auth_token", db="pytest")
class AuthTokenRepository(MongoRepository[AuthToken, str]):
    pass