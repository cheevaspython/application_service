from datetime import datetime
from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class KafkaMessage:
    application_id: int
    user_name: str
    description: str
    created_at: datetime
