from sqlalchemy import Result, desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from source.api.dependency.application.output_data import (
    ApplicationListPaginated,
    ApplicationResponseData,
)
from source.db.models.application import Application
from source.filters.application import ApplicationFilters
from source.filters.pagination import Pagination


class ApplicationReaderImpl:

    def __init__(self, session: AsyncSession) -> None:
        self._session: AsyncSession = session

    async def get_list(
        self,
        filters: ApplicationFilters,
        pagination: Pagination,
    ) -> ApplicationListPaginated:

        query = select(
            Application,
            func.count().over().label("total_count"),
        ).order_by(desc(Application.id))

        if filters and filters.user_name:
            query = query.where(Application.user_name == filters.user_name)

        if pagination.offset is not None:
            query = query.offset(pagination.offset)

        if pagination.limit is not None:
            query = query.limit(pagination.limit)

        result = await self._session.execute(query)
        return self._load_applications(result=result)

    def _load_applications(self, result: Result) -> ApplicationListPaginated:
        rows = result.all()
        total_count = rows[0].total_count if rows else 0
        applications = []
        for row in rows:
            application = ApplicationResponseData(
                id=row.Application.id,
                user_name=row.Application.user_name,
                description=row.Application.description,
                created_date=row.Application.created_date,
            )
            applications.append(application)

        return ApplicationListPaginated(
            count=total_count,
            results=applications,
        )
