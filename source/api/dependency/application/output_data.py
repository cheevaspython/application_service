from collections.abc import Sequence
from datetime import datetime
from dataclasses import dataclass

from source.types.model_id import ModelIdType


@dataclass(slots=True)
class ApplicationResponseData:
    id: ModelIdType
    user_name: str
    description: str
    created_date: datetime | str

    def __post_init__(self):
        if isinstance(self.created_date, datetime):
            self.created_date = self.created_date.strftime("%m/%d/%Y, %H:%M:%S")


@dataclass(slots=True, frozen=True)
class ApplicationListPaginated:
    count: int
    results: Sequence[ApplicationResponseData]
