from fastapi import APIRouter

from source.config.settings import settings

router = APIRouter(
    prefix=settings.api.prefix,
)
