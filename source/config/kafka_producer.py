import json
from typing import Literal
from dataclasses import asdict

from aiokafka import AIOKafkaProducer

from source.errors.kafka import KafkaProducerError
from source.schemas.other.kafka import KafkaMessage


class KafkaProducer:

    def __init__(self, kafka_server: str):
        self.kafka_server = kafka_server
        self.producer = None

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
        await self.producer.send_and_wait(
            topic,
            json.dumps(asdict(message)).encode("utf-8"),
        )
