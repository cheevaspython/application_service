from typing import Protocol

from source.filters.application import ApplicationFilters
from source.filters.pagination import Pagination


class ApplicationReader(Protocol):

    async def get_list(
        self,
        filters: ApplicationFilters,
        pagination: Pagination,
    ):
        raise NotImplementedError
