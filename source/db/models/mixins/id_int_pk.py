from sqlalchemy import BigInteger, Identity
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)


class IdBigIntPkMixin:

    id: Mapped[int] = mapped_column(
        BigInteger,
        Identity(),
        primary_key=True,
    )
