from fastapi import APIRouter

from source.config.settings import settings
from source.api.api_v1.views.application import router as application_router
from source.api.api_v1.views.kafka import router as kafka_router


public_router = APIRouter(
    prefix=settings.api.v1.prefix,
)
public_router.include_router(router=application_router)
public_router.include_router(router=kafka_router)
