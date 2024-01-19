from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class DefaultBaseModel(BaseModel):

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra="ignore",
        alias_generator=to_camel,
        populate_by_name=True
    )
