from typing import Protocol

from source.db.models.application import Application


class ApplicationGateway(Protocol):

    async def save(self, application: Application) -> None:
        raise NotImplementedError

    async def by_id(self, application_id: int) -> Application | None:
        raise NotImplementedError
