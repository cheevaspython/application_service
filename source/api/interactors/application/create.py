from source.api.interactors.application.input_data import CreateApplicationInputData
from source.api.dependency.application.gateway import ApplicationGateway
from source.common.commiter import Commiter
from source.db.models.application import Application
from source.schemas.other.kafka import KafkaMessage
from source.services.kafka.common import KafkaService


class CreateApplicationInteractor:

    def __init__(
        self,
        application_gateway: ApplicationGateway,
        kafka_service: KafkaService,
        commiter: Commiter,
    ):
        self._application_gateway = application_gateway
        self._commiter = commiter
        self._kafka_service = kafka_service

    async def __call__(
        self,
        create_data: CreateApplicationInputData,
    ) -> Application:
        application = await self._application_gateway.save(
            Application(
                user_name=create_data.user_name,
                description=create_data.description,
            )
        )
        await self._commiter.commit()

        message = KafkaMessage(
            application_id=application.id,
            user_name=application.user_name,
            description=application.description,
            created_at=str(application.created_date),  # TODO
        )
        await self._kafka_service.send("application", message)
        return application
