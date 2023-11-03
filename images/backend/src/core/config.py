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


class MinioConfig(BaseModel):
    host: str = 'minio'
    port: int = 9000
    user: str = environ.get('MINIO_ROOT_USER', 'minioadmin')
    password: SecretStr = SecretStr(
        environ.get('MINIO_ROOT_PASSWORD', 'minioadmin'),
    )


class FastAPIConfig(BaseModel):
    title: str = 'Pastebin-clone API v1'
    description: str = 'Pastebin-clone API'
    version: str = '1.0'
    docs_url: str = '/api/docs'
    openapi_url: str = '/api/openapi.json'
    host: str = '0.0.0.0'
    port: int = 8000


class Settings(BaseSettings):
    minio: MinioConfig = Field(default_factory=MinioConfig)
    redis: RedisConfig = Field(default_factory=RedisConfig)
    postgres: PostgresConfig = Field(default_factory=PostgresConfig)
    fastapi: FastAPIConfig = Field(default_factory=FastAPIConfig)


settings = Settings()
