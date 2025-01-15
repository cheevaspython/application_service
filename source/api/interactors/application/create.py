from source.api.interactors.application.input_data import CreateApplicationInputData
from source.api.dependency.application.gateway import ApplicationGateway
from source.common.commiter import Commiter
from source.db.models.application import Application


class CreateApplicationInteractor:

    def __init__(
        self,
        application_gateway: ApplicationGateway,
        commiter: Commiter,
    ):
        self._application_gateway = application_gateway
        self._commiter = commiter

    async def __call__(
        self,
        create_data: CreateApplicationInputData,
    ):
        await self._application_gateway.save(
            Application(
                user_name=create_data.user_name,
                description=create_data.description,
            )
        )
        await self._commiter.commit()
