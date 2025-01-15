from dataclasses import dataclass
from datetime import datetime

from source.types.model_id import ModelIdType


@dataclass(slots=True)
class KafkaMessage:
    application_id: ModelIdType
    user_name: str
    description: str
    created_at: datetime | str

    def __post_init__(self):
        if isinstance(self.created_at, datetime):
            self.created_at = self.created_at.strftime("%m/%d/%Y, %H:%M:%S")
