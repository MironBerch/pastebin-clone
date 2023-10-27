from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete

from db.minio import MinIOClient, get_minio_client
from models.pastes import Paste
from core.celery import celery_app
from db.postgres import get_async_session


@celery_app.task
def burn_paste(paste_id: str | UUID) -> None:
    session: AsyncSession = get_async_session()
    minio: MinIOClient = get_minio_client()
    minio.delete_file(f'{paste_id}.txt')
    await session.execute(delete(Paste).where(Paste.id == paste_id))
    await session.commit()
