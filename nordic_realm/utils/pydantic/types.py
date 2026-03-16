from datetime import datetime
from typing import Annotated, TypeAlias, TypeVar

from pydantic import BeforeValidator, Field, PlainSerializer

from nordic_realm.utils.pydantic_validators import PydanticValidators

T = TypeVar("T")

import pytz

UTC = pytz.timezone("UTC")


def as_string_date(v: datetime) -> str:
    return v.strftime("%Y-%m-%d")


JSONDate: TypeAlias = Annotated[
    datetime,
    Field(default_factory=datetime.now),
    PlainSerializer(func=as_string_date, return_type=str, when_used="json-unless-none"),
]

DateTimeNow = Field(default_factory=datetime.now)
DateTimeNowExcluded = Field(default_factory=datetime.now, exclude=True)

DateTimeUTCNow: TypeAlias = Annotated[
    datetime, Field(default_factory=lambda: datetime.now(UTC))
]

DateTimeMidnightToday: TypeAlias = Annotated[
    datetime, BeforeValidator(PydanticValidators.to_midnight)
]

MongoIDField: TypeAlias = Annotated[
    T, Field(validation_alias="_id", serialization_alias="id")
]
