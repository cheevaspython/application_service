from typing import Literal, Protocol

from source.schemas.other.kafka import KafkaMessage


class KafkaGateway(Protocol):

    async def start(self) -> None:
        raise NotImplementedError

    async def stop(self) -> None:
        raise NotImplementedError

    async def send(
        self,
        topic: Literal["application"],
        message: KafkaMessage,
    ) -> None:
        raise NotImplementedError

    async def consume_messages(
        self,
        topic: Literal["application"],
        timeout: int = 10,
    ) -> list:
        raise NotImplementedError

    async def send_fs(
        self,
        message: KafkaMessage,
    ) -> None:
        raise NotImplementedError

    async def create_topic(
        self,
        topic_name: str,
    ) -> None:
        raise NotImplementedError
