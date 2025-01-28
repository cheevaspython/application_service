from fastapi import HTTPException
from faststream.kafka.fastapi import KafkaRouter
from aiokafka.errors import UnknownTopicOrPartitionError

from source.common.error import ApplicationError
from source.config.settings import settings
from source.schemas.other.kafka import KafkaMessage
from source.services.kafka.create_topic import create_topic_foo

response_topic = "response_app"
kafka_server = settings.kafka.connections[0]
router_kafka = KafkaRouter(kafka_server)


@router_kafka.subscriber(settings.kafka.topic)
@router_kafka.publisher(response_topic)
async def applications_listen(
    message: KafkaMessage,
):
    try:
        return {
            "response": f"message geted for appilcation_id: {message.application_id}."
        }
    except UnknownTopicOrPartitionError:
        try:
            await create_topic_foo(
                kafka_server=kafka_server,
                topic_name=response_topic,
            )
        except ApplicationError as e:
            raise HTTPException(
                status_code=404,
                detail={"message": e.message},
            )
