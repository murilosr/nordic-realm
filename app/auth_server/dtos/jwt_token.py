from datetime import datetime
from typing import Literal
from pydantic import BaseModel


class JWTToken(BaseModel):
    
    type : Literal["access"] | Literal["refresh"]
    sid : str
    tid : str
    exp : datetime
