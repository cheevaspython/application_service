from typing import Protocol

from source.db.models.application import Application
from source.types.model_id import ModelIdType


class ApplicationGateway(Protocol):

    async def save(
        self,
        application: Application,
    ) -> Application:
        raise NotImplementedError

    async def by_id(
        self,
        application_id: ModelIdType,
    ) -> Application | None:
        raise NotImplementedError
