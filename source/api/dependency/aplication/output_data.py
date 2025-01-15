from datetime import datetime
from dataclasses import dataclass

from source.types.user_id import ModelIdType


@dataclass(slots=True, frozen=True)
class ApplicationResponseData:
    id: ModelIdType
    user_name: str
    description: str
    created_date: datetime
