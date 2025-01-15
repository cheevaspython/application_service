from source.api.dependency.application.gateway import ApplicationGateway
from source.db.models.application import Application
from source.errors.notexists import CustomDoesNotExist


class GetApplication:

    def __init__(
        self,
        application_gateway: ApplicationGateway,
    ):
        self._application_gateway = application_gateway

    async def by_id(self, application_id: int) -> Application:
        application = await self._application_gateway.by_id(
            application_id=application_id
        )
        if not application:
            raise CustomDoesNotExist(
                model_id=application_id,
                class_name="Application",
            )
        return application
