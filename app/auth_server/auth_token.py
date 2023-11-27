from datetime import datetime
from typing import Annotated

from pydantic import Field
from nordic_realm.MongoBaseModel import MongoBaseModel, PyObjectId

class AuthToken(MongoBaseModel[str]):
    
    user_id : str
    created_dt : datetime = Field(default_factory=datetime.utcnow)
    updated_dt : datetime = Field(default_factory=datetime.utcnow)