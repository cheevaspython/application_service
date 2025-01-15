from typing import TYPE_CHECKING

from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase

from source.db.models.base import Base
from source.db.models.mixins.id_int_pk import IdBigIntPkMixin
from source.types.user_id import UserIdType

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class User(Base, IdBigIntPkMixin, SQLAlchemyBaseUserTable[UserIdType]):
    __table_args__ = {"extend_existing": True}

    @classmethod
    def get_db(cls, session: "AsyncSession"):
        return SQLAlchemyUserDatabase(session, cls)

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        return str(self)
