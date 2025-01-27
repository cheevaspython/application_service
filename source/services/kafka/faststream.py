from datetime import datetime
from pydantic import BaseModel, Field

from source.types.model_id import ModelIdType


class KafkaMessagePydantic(BaseModel):
    application_id: ModelIdType = Field(..., examples=["1"])
    user_name: str = Field(..., examples=["John"])
    description: str = Field(..., examples=["Some description"])
    created_at: datetime  #  = Field(..., examples=["Some description"])
