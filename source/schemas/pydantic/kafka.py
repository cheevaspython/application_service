from pydantic import BaseModel, ConfigDict

from source.types.model_id import ModelIdType


class KafkaOutPutBase(BaseModel):
    application_id: ModelIdType
    user_name: str
    description: str
    created_at: str


class KafkaOutPutScheme(KafkaOutPutBase):
    model_config = ConfigDict(from_attributes=True)
