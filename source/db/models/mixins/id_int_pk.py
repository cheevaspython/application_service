from sqlalchemy import BigInteger, Identity
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from source.types.user_id import ModelIdType


class IdBigIntPkMixin:

    id: Mapped[ModelIdType] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )
