from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title=settings.fastapi.title,
    description=settings.fastapi.description,
    version=settings.fastapi.version,
    docs_url=settings.fastapi.docs_url,
    openapi_url=settings.fastapi.openapi_url,
    lifespan=lifespan,
)


if __name__ == '__main__':
    uvicorn.run(
        app='main:app',
        host=settings.fastapi.host,
        port=settings.fastapi.port,
        reload=True,
    )
