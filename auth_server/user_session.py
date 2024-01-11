from datetime import datetime, timedelta
from uuid import uuid4

from bson import ObjectId
from pydantic import Field

from nordic_realm.mongo.mongo_base_model import MongoBaseModel, PyObjectId


def refresh_expiry_dt_factory():
    return datetime.utcnow() + timedelta(days=30)


def access_expiry_dt_factory():
    return datetime.utcnow() + timedelta(days=30)


def token_factory():
    return uuid4().hex + uuid4().hex


class UserSession(MongoBaseModel[PyObjectId]):
    user_id: str
    user_agent: str
    access_token_tid: str = Field(default_factory=token_factory)
    refresh_token_tid: str = Field(default_factory=token_factory)
    created_dt: datetime = Field(default_factory=datetime.utcnow)
    access_token_expiry_dt: datetime = Field(default_factory=access_expiry_dt_factory)
    refresh_token_expiry_dt: datetime = Field(default_factory=refresh_expiry_dt_factory)

    @staticmethod
    def create(user_id: str, user_agent: str) -> "UserSession":
        return UserSession(
            _id=str(ObjectId()),
            user_id=user_id,
            user_agent=user_agent
        )

    def generate_new_tokens(self):
        self.access_token_tid = token_factory()
        self.refresh_token_tid = token_factory()
        self.access_token_expiry_dt = access_expiry_dt_factory()
        self.refresh_token_expiry_dt = refresh_expiry_dt_factory()
