from typing import Optional
from typing_extensions import Annotated

from pydantic import BaseModel, ConfigDict, Field
from nordic_realm.MongoBaseModel import MongoBaseModel, PyObjectId


class Test(MongoBaseModel[PyObjectId]):
    
    x : int
    y : str | None
    z : str | None