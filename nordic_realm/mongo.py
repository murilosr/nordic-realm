from typing import Any
from bson import ObjectId
from pymongo import MongoClient

from nordic_realm.MongoBaseModel import MongoBaseModel

from collections import abc
from typing import (
    TYPE_CHECKING,
    Any,
    Optional,
    Union,
)

from bson.objectid import ObjectId
from bson.raw_bson import RawBSONDocument
from pymongo.results import InsertOneResult
from pymongo.typings import _DocumentType
from pymongo.collection import Collection
from pymongo.client_session import ClientSession


mongo_client = MongoClient(
    host="mongodb://root:murilo@rs1.mongodb.local:27017/?retryWrites=true&serverSelectionTimeoutMS=5000&connectTimeoutMS=10000&authSource=admin&authMechanism=SCRAM-SHA-1"
)

db = mongo_client["pytest"]
mongo_col = db["test"]

# Collection._original_insert_one = Collection.insert_one
# def custom_insert_one(
#         self,
#         document: Union[_DocumentType, RawBSONDocument, MongoBaseModel],
#         bypass_document_validation: bool = False,
#         session: Optional[ClientSession] = None,
#         comment: Optional[Any] = None,
#     ) -> InsertOneResult:
#     if(isinstance(document, MongoBaseModel)):
#         if document.id is None:
#             document.id = ObjectId()
#             print(document)
#         document = document.model_dump(by_alias=True)
#     return self._original_insert_one(document, bypass_document_validation, session, comment)

# Collection.insert_one = custom_insert_one