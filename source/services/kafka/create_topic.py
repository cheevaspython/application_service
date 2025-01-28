from aiokafka.admin import AIOKafkaAdminClient, NewTopic

from source.errors.kafka import KafkaRunTimeError
from source.services.logging import logger


async def create_topic_foo(
    kafka_server: str,
    topic_name: str,
) -> None:
    admin_client = AIOKafkaAdminClient(bootstrap_servers=kafka_server)
    await admin_client.start()
    try:
        topic = NewTopic(
            name=topic_name,
            num_partitions=1,
            replication_factor=1,
        )
        await admin_client.create_topics([topic])
        logger.info(f"Topic '{topic_name}' created successfully!")
    except Exception as e:
        raise KafkaRunTimeError(error=str(e))
    finally:
        await admin_client.close()
