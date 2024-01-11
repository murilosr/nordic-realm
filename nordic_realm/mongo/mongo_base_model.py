from typing import Type

from bson import ObjectId
from pydantic import (AfterValidator, BaseModel, ConfigDict, Field,
                      PlainSerializer, WithJsonSchema)
from pydantic.alias_generators import to_camel
from typing_extensions import Annotated, Any, Dict, Generic, TypeVar, Union


def validate_object_id(v: Any) -> ObjectId:
    if isinstance(v, ObjectId):
        return v
    if ObjectId.is_valid(v):
        return ObjectId(v)
    raise ValueError("Invalid ObjectId")


PyObjectId = Annotated[
    Union[str, ObjectId],
    AfterValidator(validate_object_id),
    PlainSerializer(lambda x: str(x), return_type=str, when_used="json-unless-none"),
    WithJsonSchema({"type": "string"}, mode="serialization"),
]

ID_TYPE = TypeVar('ID_TYPE', default=PyObjectId)


class MongoBaseModel(BaseModel, Generic[ID_TYPE]):
    id: ID_TYPE = Field(alias="_id")
    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="ignore",
        alias_generator=to_camel,
        populate_by_name=True
    )

    def get_id_type(self) -> Type:
        return self.__orig_bases__[0].__args__[0]  # type: ignore

    def to_bson(self) -> Dict[str, Any]:
        _obj = self.model_dump(by_alias=False, exclude_none=True)
        _obj["_id"] = _obj.pop("id")
        return _obj
