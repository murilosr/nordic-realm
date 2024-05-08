from importlib import import_module
from typing import Annotated, Any, ClassVar, Generic, List, Optional, Type, TypeVar, TYPE_CHECKING

from bson import ObjectId
from pymongo import MongoClient

from nordic_realm.mongo.exceptions import DocumentNotFound, MultipleDocumentFound
from nordic_realm.mongo.mongo_base_model import MongoBaseModel, PyObjectId

if TYPE_CHECKING:
    from nordic_realm.application import ApplicationContext

MODEL = TypeVar('MODEL', bound=MongoBaseModel[Any])
ID_TYPE = TypeVar('ID_TYPE')

_ApplicationContext: Optional["ApplicationContext"] = None


class MongoRepository(Generic[MODEL, ID_TYPE]):
    _MONGO_CLIENT: MongoClient
    _DB: Annotated[str, ClassVar]
    _COLLECTION: Annotated[str, ClassVar]

    def _post_init(self):
        global _ApplicationContext

        if _ApplicationContext is None:
            _ApplicationContext = import_module("nordic_realm.application.context").ApplicationContext

        db = self.__class__._DB
        if db is None:
            db = _ApplicationContext.get().config_store.get("mongodb.db")
            if not isinstance(db, str):
                raise ValueError("Provide a database via 'db' parameter or via mongodb.db in secrets.yaml")

        self._MONGO = self._MONGO_CLIENT[db][self._COLLECTION]

    def get_all(self) -> List[MODEL]:
        return [self._get_model_type()(**_result) for _result in self._MONGO.find({})]

    def get_by_id(self, id: ID_TYPE) -> MODEL:
        if self._get_id_type() == PyObjectId and isinstance(id, str):
            id = ObjectId(id)  # type: ignore
        _result = list(self._MONGO.find({"_id": id}, limit=2))
        if len(_result) == 0:
            raise DocumentNotFound("Document not found")
        if len(_result) == 2:
            raise MultipleDocumentFound("Multiple document found")
        return self._get_model_type()(**_result[0])

    def find_all_by_custom_filter(self, _filter: dict) -> list[MODEL]:
        return self._construct_response(self._MONGO.find(_filter))

    def find_by_id(self, id: ID_TYPE) -> Optional[MODEL]:
        if self._get_id_type() == PyObjectId and isinstance(id, str):
            id = ObjectId(id)  # type: ignore
        _result = list(self._MONGO.find({"_id": id}, limit=2))
        if len(_result) == 0:
            return None
        if len(_result) == 2:
            raise MultipleDocumentFound("Multiple document found")
        return self._get_model_type()(**_result[0])

    def save(self, entity: MODEL) -> MODEL:
        if getattr(entity, "id", None) is None:
            if self._get_id_type() == PyObjectId:
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
        return self._MONGO.delete_one({"_id": id}).deleted_count

    def _construct_response(self, result: Any) -> List[MODEL]:
        return [self._get_model_type()(**_item) for _item in result]

    def _construct_single_response(self, result: Any) -> MODEL | None:
        _result = list(result)
        if len(_result) == 0:
            return None
        if len(_result) == 2:
            raise MultipleDocumentFound("Multiple document found")
        return self._get_model_type()(**_result[0])

    def drop_repository(self):
        self._MONGO.drop()

    def bulk_save(self, insert_data: List[MODEL]) -> List[ID_TYPE]:
        _documents = [_item.to_bson() for _item in insert_data]
        return self._MONGO.insert_many(_documents).inserted_ids
