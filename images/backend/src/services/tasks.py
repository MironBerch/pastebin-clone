from uuid import UUID
import asyncio

from sqlalchemy import delete

from db.minio import MinIOClient, get_minio_client
from models.pastes import Paste
from src.celery_app import celery_app
from db.postgres import get_async_session


async def delete_paste_from_db(paste_id: str | UUID) -> None:
    async for session in get_async_session():
        await session.execute(delete(Paste).where(Paste.id == paste_id))
        await session.commit()
        break


@celery_app.task
def burn_paste(paste_id: str | UUID) -> None:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    minio: MinIOClient = get_minio_client()
    minio.delete_file(f'{paste_id}.txt')

    loop.run_until_complete(delete_paste_from_db(paste_id))
    loop.close()
