from datetime import datetime, UTC

from pydantic_core.core_schema import ValidationInfo


class PydanticValidators:

    @staticmethod
    def to_midnight(v: datetime | str, info: ValidationInfo | None):
        if isinstance(v, str):
            v = datetime.fromisoformat(v)
        return v.replace(hour=0, minute=0, second=0, microsecond=0, tzinfo=UTC)
