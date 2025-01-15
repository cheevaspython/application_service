import asyncio
import json
from typing import Literal
from dataclasses import asdict

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

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

    async def consume_messages(
        self,
        topic: Literal["application"],
        timeout: int = 1,
    ) -> list:
        consumer = AIOKafkaConsumer(
            topic,
            bootstrap_servers=self.kafka_server,
            auto_offset_reset="earliest",
        )
        await consumer.start()
        result = []
        try:
            try:
                await asyncio.wait_for(
                    self.fetch_messages(
                        consumer=consumer,
                        result=result,
                    ),
                    timeout=timeout,
                )
            except asyncio.TimeoutError:
                raise NotImplementedError
        except Exception as e:
            raise KafkaSendError(error=str(e))
        finally:
            await consumer.stop()
            return result

    async def fetch_messages(
        self,
        consumer: AIOKafkaConsumer,
        result: list[str],
    ) -> None:
        async for message in consumer:
            if message.value:
                result.append(message.value.decode("utf-8"))
