from typing import Any

from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel
from typing_extensions import Generic, TypeVar, Literal, TypeAlias

REF_MODEL = TypeVar("REF_MODEL")
ID_TYPE = TypeVar("ID")
IncEx: TypeAlias = 'set[int] | set[str] | dict[int, Any] | dict[str, Any] | None'


class MongoRefModel(BaseModel, Generic[REF_MODEL, ID_TYPE]):
    id: ID_TYPE
    IS_REF: Literal[True] = Field(default=True, alias="__ref")

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="ignore",
        alias_generator=to_camel,
        populate_by_name=True
    )

    @classmethod
    def create(cls, entity: REF_MODEL):
        data = {"__ref": True}
        for _field, _fieldData in cls.model_fields.items():
            data[_field] = getattr(entity, _field, None)
        return cls(**data)

    def model_dump(
            self,
            *,
            mode: Literal['json', 'python'] | str = 'python',
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: Literal[True] = True,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> dict[str, Any]:
        return {
            **super().model_dump(
                mode=mode,
                include=include,
                exclude=exclude,
                by_alias=True,
                exclude_unset=exclude_unset,
                exclude_defaults=exclude_defaults,
                exclude_none=exclude_none,
                round_trip=round_trip,
                warnings=warnings
            )
        }

    def model_dump_json(
            self,
            *,
            indent: int | None = None,
            include: IncEx = None,
            exclude: IncEx = None,
            by_alias: Literal[True] = True,
            exclude_unset: bool = False,
            exclude_defaults: bool = False,
            exclude_none: bool = False,
            round_trip: bool = False,
            warnings: bool = True,
    ) -> str:
        return super().model_dump_json(indent=indent, include=include, exclude=exclude, by_alias=by_alias,
                                       exclude_unset=exclude_unset, exclude_defaults=exclude_defaults,
                                       exclude_none=exclude_none, round_trip=round_trip, warnings=warnings)
