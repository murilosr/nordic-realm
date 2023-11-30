from app.auth_server.user_session import UserSession
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo import MongoRepository
from nordic_realm.mongo.mongo_base_model import PyObjectId


@Repository(collection="user_session")
class UserSessionRepository(MongoRepository[UserSession, PyObjectId]):
    pass