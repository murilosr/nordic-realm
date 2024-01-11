from nordic_realm.mongo import MongoBaseModel


class User(MongoBaseModel[str]):
    name: str
    email: str
    password: str
