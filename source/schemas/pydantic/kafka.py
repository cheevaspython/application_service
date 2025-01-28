from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

from source.types.model_id import ModelIdType


class KafkaOutPutBase(BaseModel):
    application_id: ModelIdType
    user_name: str
    description: str
    created_at: str


class KafkaOutPutScheme(KafkaOutPutBase):
    model_config = ConfigDict(from_attributes=True)


class KafkaMessagePydantic(BaseModel):
    application_id: ModelIdType = Field(..., examples=["1"])
    user_name: str = Field(..., examples=["John"])
    description: str = Field(..., examples=["Some description"])
    created_at: datetime
