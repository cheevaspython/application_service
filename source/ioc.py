from collections.abc import AsyncIterable

from dishka import Provider, provide, Scope, make_async_container, from_context, AnyOf
from dishka.integrations.taskiq import TaskiqProvider

from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from source.config.settings import Settings, settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    # gateway = provide(
    #     Gateway,
    #     scope=Scope.REQUEST,
    #     provides=GatewayProtocol,
    # )


def setup_taskiq_container():
    return make_async_container(
        AppProvider(),
        TaskiqProvider(),
        context={Settings: settings},
    )


def setup_fastapi_container():
    return make_async_container(
        AppProvider(),
        context={Settings: settings},
    )
