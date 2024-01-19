from typing import Any

from nordic_realm.decorators.controller import Component


@Component()
class UserRepositoryProvider:

    def get_by_id(self, id: Any):
        raise NotImplementedError("This must be overriden")
