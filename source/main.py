from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from source.config.settings import settings
from source.api import router as api_router
from source.db.db_helper import db_helper
from source.ioc import setup_fastapi_container

from dishka.integrations import fastapi as fastapi_integration

app = FastAPI()

container = setup_fastapi_container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Точка входа: выполняется перед запуском приложения
    try:
        yield  # Передаем управление FastAPI (логика старта приложения здесь)
    finally:
        # Завершение: выполняется после завершения работы приложения
        await db_helper.dispose()


app = FastAPI(
    title="Example",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:8000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
)
fastapi_integration.setup_dishka(container, app)

app.mount(
    "/media",
    StaticFiles(directory=settings.media_files_path.upload_image),
    name="media",
)
