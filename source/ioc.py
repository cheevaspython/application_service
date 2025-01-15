from typing import AsyncIterable

from dishka import Provider, Scope, make_async_container, from_context, provide
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from source.api.dependency.aplication.gateway import ApplicationGateway
from source.api.dependency.aplication.gateway_impl import ApplicationGatewayImpl
from source.api.dependency.aplication.reader import ApplicationReader
from source.api.dependency.aplication.reader_impl import ApplicationReaderImpl
from source.api.interactors.aplication.create import CreateApplicationInteractor
from source.api.interactors.aplication.get import GetApplication
from source.api.queries.application.get_many import GetApplications
from source.db.db_helper import db_helper
from source.config.settings import Settings, settings


class AppProvider(Provider):
    config = from_context(
        provides=Settings,
        scope=Scope.APP,
    )

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
    get_applications_query = provide(
        GetApplications,
        scope=Scope.REQUEST,
    )
    get_applications_interactor = provide(
        GetApplication,
        scope=Scope.REQUEST,
    )
    create_application_interactor = provide(
        CreateApplicationInteractor,
        scope=Scope.REQUEST,
    )


def setup_fastapi_container():
    return make_async_container(
        AppProvider(),
        context={Settings: settings},
    )
