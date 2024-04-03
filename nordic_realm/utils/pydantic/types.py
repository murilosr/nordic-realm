from datetime import datetime
from typing import Annotated, TypeAlias, TypeVar

from pydantic import Field, PlainSerializer, BeforeValidator

from nordic_realm.utils.pydantic_validators import PydanticValidators

T = TypeVar("T")


def as_string_date(v: datetime) -> str:
    return v.strftime("%Y-%m-%d")


JSONDate: TypeAlias = Annotated[
    datetime,
    Field(
        default_factory=datetime.utcnow
    ),
    PlainSerializer(
        func=as_string_date,
        return_type=str,
        when_used="json-unless-none"
    )
]

DateTimeUTCNow: TypeAlias = Annotated[
    datetime,
    Field(
        default_factory=datetime.utcnow
    )
]

DateTimeMidnightToday: TypeAlias = Annotated[
    datetime,
    BeforeValidator(PydanticValidators.to_midnight)
]

MongoIDField: TypeAlias = Annotated[
    T,
    Field(validation_alias="_id", serialization_alias="id")
]
