from typing import Annotated, Any, ClassVar, Generic, List, Optional, Type, TypeVar

from bson import ObjectId
from pymongo import MongoClient

from .mongo_base_model import MongoBaseModel, PyObjectId

MODEL = TypeVar('MODEL', bound=MongoBaseModel[Any])
ID_TYPE = TypeVar('ID_TYPE')


class MongoRepository(Generic[MODEL, ID_TYPE]):
    _MONGO_CLIENT: MongoClient
    _DB: Annotated[str, ClassVar]
    _COLLECTION: Annotated[str, ClassVar]

    def _post_init(self):
        self._MONGO = self._MONGO_CLIENT[self._DB][self._COLLECTION]

    def get_all(self) -> List[MODEL]:
        return [self._get_model_type().model_construct(**_result) for _result in self._MONGO.find({})]

    def get_by_id(self, id: ID_TYPE) -> MODEL:
        if (self._get_id_type() == PyObjectId and isinstance(id, str)):
            id = ObjectId(id)  # type: ignore
        _result = list(self._MONGO.find({"_id": id}, limit=2))
        if (len(_result) == 0):
            raise Exception("Document not found")
        if (len(_result) == 2):
            raise Exception("Multiple document found")
        return self._get_model_type().model_construct(**_result[0])

    def find_by_id(self, id: ID_TYPE) -> Optional[MODEL]:
        if (self._get_id_type() == PyObjectId and isinstance(id, str)):
            id = ObjectId(id)  # type: ignore
        _result = list(self._MONGO.find({"_id": id}, limit=2))
        if (len(_result) == 0):
            return None
        if (len(_result) == 2):
            raise Exception("Multiple document found")
        return self._get_model_type().model_construct(**_result[0])

    def save(self, entity: MODEL) -> MODEL:
        if (getattr(entity, "id", None) is None):
            if (self._get_id_type() == PyObjectId):
                entity.id = ObjectId()  # type: ignore
            else:
                raise Exception(f"id was not supposed to be None when type is '{self._get_id_type().__name__}'")
        self._MONGO.update_one({"_id": entity.id}, {"$set": entity.to_bson()}, upsert=True)
        return self._get_model_type()(**entity.to_bson())

    def _get_model_type(self) -> Type[MODEL]:
        return self.__orig_bases__[0].__args__[0]  # type: ignore

    def _get_id_type(self) -> Type[ID_TYPE]:
        # return self._get_model_type().model_fields["id"].annotation.__args__[0]
        return self.__orig_bases__[0].__args__[1]  # type: ignore

    def delete(self, id: ID_TYPE):
        self._MONGO.delete_one({"_id": id})
