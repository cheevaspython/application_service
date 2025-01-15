from dataclasses import dataclass

from source.api.dependency.aplication.output_data import ApplicationResponseData
from source.api.dependency.aplication.reader import ApplicationReader
from source.filters.application import ApplicationFilters
from source.filters.pagination import Pagination


@dataclass(slots=True, frozen=True)
class GetApplications:
    application_reader: ApplicationReader

    async def __call__(
        self,
        filters: ApplicationFilters,
        pagination: Pagination,
    ) -> list[ApplicationResponseData]:

        applications = await self.application_reader.get_list(
            filters=filters,
            pagination=pagination,
        )

        return applications
