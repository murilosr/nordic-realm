from datetime import datetime
from bson import ObjectId
from pymongo import MongoClient
from app.models.test import Test
from app.repositories.test_repository import TestRepository
from nordic_realm.MongoBaseModel import MongoBaseModel, PyObjectId
from nordic_realm.mongo import mongo_client

TestRepository._MONGO_CLIENT = mongo_client

test_repo = TestRepository()
test_obj = Test(x=999)
test_obj = test_repo.save(test_obj)
if(test_obj.id is not None):
    test_obj_find = test_repo.get_by_id("6556788acfa8b406ac29663c")
    test_obj_find = test_repo.find_by_id("6556788acfa8b406ac29663c")
    print(test_obj_find)