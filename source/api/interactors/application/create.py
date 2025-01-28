from source.api.dependency.kafka.gateway import KafkaGateway
from source.api.interactors.application.input_data import CreateApplicationInputData
from source.api.dependency.application.gateway import ApplicationGateway
from source.common.commiter import Commiter
from source.common.error import ApplicationError
from source.db.models.application import Application
from source.schemas.other.kafka import KafkaMessage


class CreateApplicationInteractor:

    def __init__(
        self,
        application_gateway: ApplicationGateway,
        commiter: Commiter,
        kafka_service: KafkaGateway,
    ):
        self._application_gateway = application_gateway
        self._commiter = commiter
        self._kafka_service = kafka_service

    async def __call__(
        self,
        create_data: CreateApplicationInputData,
    ) -> Application:
        try:
            await self._commiter.begin()
            application = await self._application_gateway.save(
                Application(
                    user_name=create_data.user_name,
                    description=create_data.description,
                ),
            )
            await self._commiter.commit()

            message = KafkaMessage(
                application_id=application.id,
                user_name=application.user_name,
                description=application.description,
                created_at=application.created_date,
            )
            await self._kafka_service.send(
                topic="application",
                message=message,
            )

            return application
        except ApplicationError as e:
            await self._commiter.rollback()
            raise e

    async def create_faststream(
        self,
        create_data: CreateApplicationInputData,
    ) -> Application:
        try:
            await self._commiter.begin()
            application = await self._application_gateway.save(
                Application(
                    user_name=create_data.user_name,
                    description=create_data.description,
                ),
            )
            await self._commiter.commit()

            message = KafkaMessage(
                application_id=application.id,
                user_name=application.user_name,
                description=application.description,
                created_at=application.created_date,
            )
            await self._kafka_service.send_fs(
                message=message,
            )

            return application
        except ApplicationError as e:
            await self._commiter.rollback()
            raise e
