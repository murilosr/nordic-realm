from datetime import datetime, timedelta
from uuid import uuid4

from bson import ObjectId
from pydantic import Field

from nordic_realm.mongo.mongo_base_model import MongoBaseModel, PyObjectId


def expiry_dt_factory():
    return datetime.utcnow() + timedelta(days=30)


def token_factory():
    return uuid4().hex + uuid4().hex


class UserSession(MongoBaseModel[PyObjectId]):
    user_id: str
    user_agent: str
    access_token_tid: str = Field(default_factory=token_factory)
    refresh_token_tid: str = Field(default_factory=token_factory)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    expiry_dt: datetime = Field(default_factory=expiry_dt_factory)

    @staticmethod
    def create(user_id: str, user_agent: str) -> "UserSession":
        return UserSession(
            _id=ObjectId(),
            user_id=user_id,
            user_agent=user_agent
        )

    def generate_new_tokens(self):
        self.access_token_tid = token_factory()
        self.refresh_token_tid = token_factory()
        self.created_dt = datetime.utcnow()
        self.expiry_dt = expiry_dt_factory()
