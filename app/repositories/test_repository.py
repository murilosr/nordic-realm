from app.models.test import Test
from nordic_realm.MongoBaseModel import PyObjectId
from nordic_realm.decorators.controller import Repository
from nordic_realm.mongo_repository import MongoRepository

@Repository(collection="test_save", db="pytest")
class TestRepository(MongoRepository[Test, PyObjectId]):
    pass