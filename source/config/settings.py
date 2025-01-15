import os
import pytz
from typing import Tuple

from pydantic import BaseModel, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class RunConfig(BaseModel):
    host: str = "0.0.0.0"
    port: int = 8088


class DbSettings(BaseModel):
    url: PostgresDsn
    echo: bool = False
    echo_pool: bool = False
    max_overflow: int = 50
    pool_size: int = 10
    naming_convention: dict[str, str] = {
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_N_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }

    @classmethod
    def create_url(cls):
        POSTGRES_DB = os.getenv("POSTGRES_DB")
        POSTGRES_USER = os.getenv("POSTGRES_USER")
        POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
        POSTGRES_HOST = os.getenv("POSTGRES_HOST")
        POSTGRES_PORT = os.getenv("POSTGRES_PORT")

        return f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

    def __init__(self, **kwargs):
        kwargs["url"] = kwargs.get("url", self.create_url())
        super().__init__(**kwargs)


class ApiV1Prefix(BaseModel):
    prefix: str = "/v1"
    auth: str = "/auth"
    users: str = "/users"


class ApiPrefix(BaseModel):
    prefix: str = "/api"
    admin_prefix: str = "/admin"
    v1: ApiV1Prefix = ApiV1Prefix()

    @property
    def bearer_token_url(self) -> str:
        parts = (self.prefix, self.v1.prefix, self.v1.auth, "/login")
        path = "".join(parts)
        return path.removeprefix("/")


class KafkaSettings(BaseModel):
    port: str = "kafka-0:9092"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=(".env.template", ".env"),
        case_sensitive=False,
        env_nested_delimiter="__",
        env_prefix="FASTAPI_CFG__",
        extra="ignore",
    )
    db: DbSettings
    tz: pytz.tzinfo.BaseTzInfo = pytz.timezone("Europe/Moscow")
    run: RunConfig = RunConfig()
    api: ApiPrefix = ApiPrefix()
    kafka: KafkaSettings = KafkaSettings()


settings = Settings()
