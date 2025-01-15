from dataclasses import dataclass

from source.common.error import ApplicationError


@dataclass(eq=False)
class KafkaProducerError(ApplicationError):

    @property
    def message(self):
        return "Kafka producer is not started."


@dataclass(eq=False)
class KafkaSendError(ApplicationError):
    error: str

    @property
    def message(self):
        return f"Kafka send error: {self.error}."


@dataclass(eq=False)
class KafkaTopicError(ApplicationError):
    topic: str

    @property
    def message(self):
        return f"Topic '{self.topic}' does not exist."


@dataclass(eq=False)
class KafkaTimeError(ApplicationError):

    @property
    def message(self):
        return "Timeout reached, no more messages received."
