from datetime import datetime
from typing import Annotated
from uuid import uuid4

from pydantic import Field
from nordic_realm.MongoBaseModel import MongoBaseModel, PyObjectId

class AuthToken(MongoBaseModel[str]):
    
    user_id : str
    created_dt : datetime = Field(default_factory=datetime.utcnow)
    updated_dt : datetime = Field(default_factory=datetime.utcnow)

    @staticmethod
    def create(user_id : str) -> "AuthToken":
        return AuthToken(_id=uuid4().hex + uuid4().hex, user_id=user_id)