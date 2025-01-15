from dataclasses import dataclass

from source.common.error import ApplicationError
from source.services.logging import logger


@dataclass(eq=False)
class KafkaProducerError(ApplicationError):

    @property
    def message(self):
        logger.warning("Kafka producer is not started.")
        return "Kafka producer is not started."


@dataclass(eq=False)
class KafkaSendError(ApplicationError):
    error: str

    @property
    def message(self):
        logger.warning(f"Kafka send error: {self.error}.")
        return f"Kafka send error: {self.error}."


@dataclass(eq=False)
class KafkaTopicError(ApplicationError):
    topic: str

    @property
    def message(self):
        logger.warning(f"Topic '{self.topic}' does not exist.")
        return f"Topic '{self.topic}' does not exist."


@dataclass(eq=False)
class KafkaTimeError(ApplicationError):

    @property
    def message(self):
        logger.warning("Timeout reached, no more messages received.")
        return "Timeout reached, no more messages received."
