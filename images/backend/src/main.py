from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from api.urls import api_router
from core.config import settings
from db.minio import get_minio_client


@asynccontextmanager
async def lifespan(app: FastAPI):
    s3_adapter = get_minio_client()
    s3_adapter.create_bucket()
    yield


app = FastAPI(
    title=settings.fastapi.title,
    description=settings.fastapi.description,
    version=settings.fastapi.version,
    docs_url=settings.fastapi.docs_url,
    openapi_url=settings.fastapi.openapi_url,
    lifespan=lifespan,
)

app.include_router(api_router)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True,
    )
