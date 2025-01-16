import pytest
import asyncio
from typing import AsyncGenerator, Generator

from sqlalchemy.ext.asyncio import AsyncSession
from httpx import AsyncClient, ASGITransport
from fastapi import FastAPI

from source.db.db_helper import db_helper, test_db_helper
from source.db.models.base import Base
from source.main import app


@pytest.fixture(scope="function")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    """
    Fixture для получения и управления циклом событий asyncio.

    Если цикл событий уже запущен, возвращает его.
    Если нет, создаёт новый цикл событий.
    """

    try:
        loop = asyncio.get_running_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function", autouse=True)
async def setup_test_db(event_loop: asyncio.AbstractEventLoop) -> AsyncGenerator:
    """
    Fixture для настройки тестовой базы данных перед тестами и очистки после.

    Создает и удаляет все таблицы базы данных.
    """

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with test_db_helper.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="function")
async def async_client(app_with_test_db: FastAPI) -> AsyncGenerator[AsyncClient, None]:
    """
    Fixture для создания асинхронного клиента HTTP с подключением к FastAPI приложению.

    Использует ASGITransport для взаимодействия с приложением.
    """

    transport = ASGITransport(app=app_with_test_db)
    async with AsyncClient(transport=transport, base_url="http://test") as client:
        yield client


@pytest.fixture(scope="function")
async def test_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Fixture для создания тестовой сессии базы данных.

    Обеспечивает корректное закрытие сессии после использования.
    """

    async with test_db_helper.session_factory() as session:
        yield session

        await session.close()


@pytest.fixture(scope="function")
async def app_with_test_db(test_db_session: AsyncSession) -> AsyncGenerator:
    """
    Fixture для подмены зависимости базы данных в FastAPI приложении на тестовую сессию.
    """

    async def override_get_db() -> AsyncGenerator[AsyncSession, None]:
        yield test_db_session

    app.dependency_overrides[db_helper.session_getter] = override_get_db

    yield app

    app.dependency_overrides.clear()
