from nordic_realm.MongoBaseModel import MongoBaseModel
from nordic_realm.mongo_repository import MongoRepository


class User(MongoBaseModel[str]):

    name : str
    email : str
    password : str