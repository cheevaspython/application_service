from dataclasses import dataclass

from source.common.error import ApplicationError


@dataclass(eq=False)
class KafkaProducerError(ApplicationError):

    @property
    def message(self):
        return "Kafka producer is not started."
