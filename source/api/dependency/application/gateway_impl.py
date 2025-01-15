from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from source.db.models.application import Application
from source.errors.application import CannotSaveApplicationError
from source.types.model_id import ModelIdType


class ApplicationGatewayImpl:

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def save(
        self,
        application: Application,
    ) -> Application:
        try:
            self._session.add(application)
            await self._session.flush()
            return application
        except IntegrityError:
            raise CannotSaveApplicationError()

    async def by_id(
        self,
        application_id: ModelIdType,
    ) -> Application | None:
        query = select(Application).where(
            Application.id == application_id,
        )
        result = await self._session.execute(query)
        return result.scalar_one_or_none()
