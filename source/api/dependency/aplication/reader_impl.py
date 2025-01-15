from typing import TYPE_CHECKING

from sqlalchemy import desc, select

from source.api.dependency.aplication.output_data import ApplicationResponseData
from source.db.models.application import Application
from source.filters.application import ApplicationFilters
from source.filters.pagination import Pagination
from source.services.application.convertor import convert_application_to_dataclass

if TYPE_CHECKING:
    from sqlalchemy.ext.asyncio import AsyncSession


class ApplicationReaderImpl:

    def __init__(self, session: "AsyncSession") -> None:
        self._session: "AsyncSession" = session

    async def get_list(
        self,
        filters: ApplicationFilters,
        pagination: Pagination,
    ) -> list[ApplicationResponseData]:

        query = select(Application).order_by(desc(Application.id))
        if filters and filters.user_name:
            query = query.where(Application.user_name == filters.user_name)

        if pagination.offset is not None:
            query = query.offset(pagination.offset)

        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self._session.execute(query)
        client_list = [
            convert_application_to_dataclass(application=application)
            for application in result.scalars()
        ]
        return client_list
