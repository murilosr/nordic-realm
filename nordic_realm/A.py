import random
from nordic_realm.MongoBaseModel import MongoBaseModel
from pydantic import Field

class A(MongoBaseModel):  
    x : str = Field(default_factory=lambda: str(random.randint(0, 10)))
    
    def save(self) -> "A":
        return super().save()