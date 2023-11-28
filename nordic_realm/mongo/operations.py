from typing import Any, Dict, Generic, Type, TypeVar

from pymongo.collection import Collection

from .exceptions import DocumentNotFound, MultipleDocumentFound

T = TypeVar("T")

class MongoOperations(Generic[T]):

    @staticmethod
    def find_one_and_only_one(
        collection : Collection,
        filter : Dict[Any, Any],
        expected_class : Type[T],
        raise_not_found : bool = False
    ) -> T | None:
        _result = list(collection.find(filter, limit = 2))

        if(len(_result) == 1):
            return expected_class(**_result[0])
        if(len(_result) == 0):
            if(raise_not_found):
                raise DocumentNotFound()
            return None
        raise MultipleDocumentFound()
    
    @staticmethod
    def exists(
        collection : Collection,
        filter : Dict[Any, Any],
    ) -> bool:
        _result = list(collection.find(filter, limit = 1, projection={"_id":1}))
        return len(_result) == 1
    