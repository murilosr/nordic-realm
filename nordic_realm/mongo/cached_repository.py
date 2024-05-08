from typing import Generic

from nordic_realm.mongo.mongo_repository import MongoRepository, MODEL, ID_TYPE


class CachedRepository(Generic[MODEL, ID_TYPE]):

    def __init__(self, mongo_repository: MongoRepository):
        self._repo = mongo_repository
        self._cache = {}

    def get(self, id: ID_TYPE) -> MODEL:
        if id not in self._cache:
            self._cache[id] = self._repo.get_by_id(id)

        return self._cache[id]
