from source.api.dependency.kafka.gateway import KafkaGateway


class CreateTopicKafkaInteractor:

    def __init__(
        self,
        kafka_service: KafkaGateway,
    ):
        self._kafka_service = kafka_service

    async def create_topic(self, topic: str) -> None:
        await self._kafka_service.create_topic(topic_name=topic)
