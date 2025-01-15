from typing import TYPE_CHECKING

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from source.db.models.application import Application
from source.errors.application import CannotSaveApplicationError


class ApplicationGatewayImpl:

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def save(
        self,
        application: Application,
    ) -> None:
        try:
            self._session.add(application)
            await self._session.flush()
        except IntegrityError:
            raise CannotSaveApplicationError()

    async def by_id(
        self,
        application_id: int,
    ) -> Application | None:
        query = select(Application).where(
            Application.id == application_id,
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
