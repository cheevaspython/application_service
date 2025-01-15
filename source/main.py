from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from dishka.integrations import fastapi as fastapi_integration

from source.api import router as api_router
from source.db.db_helper import db_helper
from source.ioc import setup_fastapi_container

app = FastAPI()

container = setup_fastapi_container()


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        yield
    finally:
        await db_helper.dispose()


app = FastAPI(
    title="ApplicationService",
    default_response_class=ORJSONResponse,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    api_router,
)
fastapi_integration.setup_dishka(container, app)
