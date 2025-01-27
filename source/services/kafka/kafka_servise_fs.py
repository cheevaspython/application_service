from faststream.kafka.fastapi import KafkaRouter

from source.config.settings import settings
from source.schemas.other.kafka import KafkaMessage

# from source.services.kafka.faststream import KafkaMessagePydantic

kafka_router = KafkaRouter(
    bootstrap_servers=settings.kafka.connections[0],
)


class KafkaServiceImplFast:

    def __init__(
        self,
        kafka_router: KafkaRouter,
    ):
        self._kafka_router = kafka_router

    async def send_fs(
        self,
        message: KafkaMessage,
    ) -> str:
        self._kafka_router.publisher(topic=settings.kafka.topic)
        return f"App: {message.application_id} - {message.user_name} sended"
