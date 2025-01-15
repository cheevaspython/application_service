from dishka import Provider, Scope, make_async_container, from_context

from source.config.settings import Settings, settings


class AppProvider(Provider):
    config = from_context(provides=Settings, scope=Scope.APP)

    # gateway = provide(
    #     Gateway,
    #     scope=Scope.REQUEST,
    #     provides=GatewayProtocol,
    # )


def setup_fastapi_container():
    return make_async_container(
        AppProvider(),
        context={Settings: settings},
    )
