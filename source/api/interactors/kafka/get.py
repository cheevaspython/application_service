import json

from source.api.dependency.kafka.gateway import KafkaGateway
from source.schemas.pydantic.kafka import KafkaOutPutBase


class GetKafkaMessagesInteractor:

    def __init__(
        self,
        kafka_service: KafkaGateway,
    ):
        self._kafka_service = kafka_service

    async def get_messages(self) -> list[KafkaOutPutBase]:
        messages_list = await self._kafka_service.consume_messages("application")
        return [KafkaOutPutBase(**row) for row in map(json.loads, messages_list)]
