from os import environ

from pydantic_settings import BaseSettings
from pydantic import BaseModel, SecretStr, Field


class RedisConfig(BaseModel):
    host: str = 'redis'
    port: int = 6379
    db: int = 0


class PostgresConfig(BaseModel):
    host: str = 'db'
    port: int = 5432
    db: str = 'pastebin'
    user: str = environ.get('POSTGRES_USER', 'postgres')
    password: SecretStr = SecretStr(
        environ.get('POSTGRES_PASSWORD', 'postgres'),
    )


class FastAPIConfig(BaseModel):
    title: str = 'API v1'
    description: str = 'Read-only movies API'
    version: str = '1.0'
    docs_url: str = '/movies/api/docs'
    openapi_url: str = '/movies/api/openapi.json'
    host: str = '0.0.0.0'
    port: int = 8000


class Settings(BaseSettings):
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)


settings = Settings()
