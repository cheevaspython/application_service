from pydantic import BaseModel, ConfigDict

from source.types.model_id import ModelIdType


class ApplicationBase(BaseModel):
    user_name: str
    description: str


class ApplicationCreate(ApplicationBase):
    pass


class ApplicationScheme(ApplicationBase):
    model_config = ConfigDict(from_attributes=True)

    id: ModelIdType
