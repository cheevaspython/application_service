from typing import AsyncIterable

from aiokafka.admin import AIOKafkaAdminClient
from dishka import Provider, Scope, make_async_container, from_context, provide
from faststream.kafka.fastapi import KafkaRouter
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from source.api.dependency.application.gateway import ApplicationGateway
from source.api.dependency.application.gateway_impl import ApplicationGatewayImpl
from source.api.dependency.application.reader import ApplicationReader
from source.api.dependency.application.reader_impl import ApplicationReaderImpl
from source.api.dependency.kafka.gateway import KafkaGateway
from source.api.dependency.kafka.kafka_service import KafkaServiceImpl
from source.api.interactors.application.create import CreateApplicationInteractor
from source.api.interactors.application.get import GetApplication
from source.api.interactors.kafka.create import CreateTopicKafkaInteractor
from source.api.interactors.kafka.get import GetKafkaMessagesInteractor
from source.api.queries.application.get_many import GetApplications
from source.common.commiter import Commiter
from source.db.db_helper import db_helper
from source.config.settings import Settings, settings
from source.db.sa_commiter import SACommiter


class AppProvider(Provider):
    config = from_context(
        provides=Settings,
        scope=Scope.APP,
    )

    @provide(scope=Scope.APP)
    async def provide_kafka(
        self,
        config: Settings,
    ) -> KafkaRouter:
        kafka_router = KafkaRouter(
            bootstrap_servers=config.kafka.connections[0],
        )
        await kafka_router.broker.connect()
        return kafka_router

    @provide(scope=Scope.APP)
    def provide_session_maker(self) -> async_sessionmaker[AsyncSession]:
        return db_helper.session_factory

    @provide(scope=Scope.REQUEST)
    async def provide_session(
        self,
        session_maker: async_sessionmaker[AsyncSession],
    ) -> AsyncIterable[AsyncSession,]:
        async with session_maker() as session:
            yield session

    @provide(scope=Scope.REQUEST)
    async def provide_aiokafka_admin(
        self,
    ) -> AIOKafkaAdminClient:
        admin_client = AIOKafkaAdminClient(
            bootstrap_servers=settings.kafka.connections[0]
        )
        await admin_client.start()
        return admin_client

    application_gateway = provide(
        ApplicationGatewayImpl,
        scope=Scope.REQUEST,
        provides=ApplicationGateway,
    )
    application_reader = provide(
        ApplicationReaderImpl,
        scope=Scope.REQUEST,
        provides=ApplicationReader,
    )
    kafka_service = provide(
        KafkaServiceImpl,
        scope=Scope.REQUEST,
        provides=KafkaGateway,
    )
    get_applications_query = provide(
        GetApplications,
        scope=Scope.REQUEST,
    )
    get_applications_interactor = provide(
        GetApplication,
        scope=Scope.REQUEST,
    )
    create_topic_kafka_interactor = provide(
        CreateTopicKafkaInteractor,
        scope=Scope.REQUEST,
    )
    get_kafka_messages_interactor = provide(
        GetKafkaMessagesInteractor,
        scope=Scope.REQUEST,
    )
    create_application_interactor = provide(
        CreateApplicationInteractor,
        scope=Scope.REQUEST,
    )
    sa_commiter = provide(
        SACommiter,
        scope=Scope.REQUEST,
        provides=Commiter,
    )


def setup_fastapi_container():
    return make_async_container(
        AppProvider(),
        context={Settings: settings},
    )
