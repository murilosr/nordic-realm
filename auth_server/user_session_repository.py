from auth_server.user_session import UserSession
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo import MongoRepository


@Repository(collection="user_session")
class UserSessionRepository(MongoRepository[UserSession, str]):

    def delete_all_by_user_id(self, user_id: str):
        self._MONGO.delete_many({"user_id": user_id})
