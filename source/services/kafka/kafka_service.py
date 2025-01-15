import json
from typing import Literal
from dataclasses import asdict

from aiokafka import AIOKafkaProducer

from source.errors.kafka import KafkaProducerError, KafkaSendError
from source.schemas.other.kafka import KafkaMessage


class KafkaServiceImpl:

    def __init__(self, kafka_server: str):
        self.kafka_server = kafka_server

    async def start(self) -> None:
        self.producer = AIOKafkaProducer(bootstrap_servers=self.kafka_server)
        await self.producer.start()

    async def stop(self) -> None:
        if self.producer:
            await self.producer.stop()

    async def send(
        self,
        topic: Literal["application"],
        message: KafkaMessage,
    ) -> None:
        if not self.producer:
            raise KafkaProducerError()
        try:
            await self.producer.send_and_wait(
                topic,
                json.dumps(asdict(message)).encode("utf-8"),
            )
        except Exception as e:
            raise KafkaSendError(f"Failed to send message: {str(e)}")
