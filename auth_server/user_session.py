from datetime import datetime, timedelta
from typing import TypeAlias, Annotated

from pydantic import Field

from nordic_realm.mongo.mongo_base_model import MongoBaseModel
from nordic_realm.utils import generate_id
from nordic_realm.utils.pydantic.types import DateTimeUTCNow


def refresh_expiry_dt_factory():
    return datetime.utcnow() + timedelta(days=30)


def access_expiry_dt_factory():
    return datetime.utcnow() + timedelta(days=30)


def token_factory():
    return generate_id(32)


TokenType: TypeAlias = Annotated[str, Field(default_factory=token_factory)]


class UserSession(MongoBaseModel[str]):
    user_id: str
    user_agent: str
    access_token_tid: TokenType
    refresh_token_tid: TokenType
    created_dt: DateTimeUTCNow
    access_token_expiry_dt: datetime = Field(default_factory=access_expiry_dt_factory)
    refresh_token_expiry_dt: datetime = Field(default_factory=refresh_expiry_dt_factory)

    @staticmethod
    def create(user_id: str, user_agent: str) -> "UserSession":
        return UserSession(
            id=generate_id(),
            user_id=user_id,
            user_agent=user_agent
        )

    def generate_new_tokens(self):
        self.access_token_tid = token_factory()
        self.refresh_token_tid = token_factory()
        self.access_token_expiry_dt = access_expiry_dt_factory()
        self.refresh_token_expiry_dt = refresh_expiry_dt_factory()
