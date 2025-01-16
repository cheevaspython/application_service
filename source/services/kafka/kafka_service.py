import asyncio
import json
from typing import Literal
from dataclasses import asdict

from aiokafka import AIOKafkaProducer, AIOKafkaConsumer
from aiokafka.client import KafkaConnectionError

from source.errors.kafka import (
    KafkaConnectionCustomError,
    KafkaProducerError,
    KafkaRunTimeError,
    KafkaSendError,
)
from source.schemas.other.kafka import KafkaMessage


class KafkaServiceImpl:

    def __init__(self, kafka_servers: list[str]):
        """
        Инициализирует KafkaServiceImpl с массивом серверов Kafka.

        :param kafka_servers: Список серверов Kafka (например, ["kafka-0:9092", "kafka-1:9092"])
        """
        self.kafka_servers = kafka_servers
        self.producer = None

    async def start(self) -> None:
        """
        Запускает подключение к Kafka. Если первый сервер недоступен, переключается на следующий.
        """
        for server in self.kafka_servers:
            try:
                self.producer = AIOKafkaProducer(bootstrap_servers=server)
                await self.producer.start()
                return
            except KafkaConnectionError as e:
                raise KafkaConnectionCustomError(server=server, error=str(e))

        raise KafkaRunTimeError()

    async def _start_consumer(
        self,
        topic: Literal["application"],
    ) -> AIOKafkaConsumer:
        """
        Запускает подключение к Consumer Kafka. Если первый сервер недоступен, переключается на следующий.
        """
        for server in self.kafka_servers:
            try:
                consumer = AIOKafkaConsumer(
                    topic,
                    bootstrap_servers=server,
                    auto_offset_reset="earliest",
                )
                await consumer.start()
                return consumer
            except KafkaConnectionError as e:
                raise KafkaConnectionCustomError(server=server, error=str(e))

        else:
            raise KafkaRunTimeError()

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
            raise KafkaSendError(error=str(e))

    async def consume_messages(
        self,
        topic: Literal["application"],
        timeout: int = 1,
    ) -> list:

        consumer = await self._start_consumer(topic=topic)
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
