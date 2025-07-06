from http import HTTPStatus
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc
from fastapi import Depends, HTTPException

from models.pastes import Paste
from schemas.pastes import PasteSchema, BasePasteSchema
from models.pastes import ExpirationOption, ExposureOption
from db.postgres import get_async_session
from db.minio import MinIOClient, get_minio_client
from services.tasks import burn_paste


class PastesService:
    def __init__(self, db_adapter: AsyncSession, s3_adapter: MinIOClient):
        self.db_adapter = db_adapter
        self.s3_adapter = s3_adapter

    def __get_expiration_time(self, expiration: ExpirationOption) -> int | None:
        return {
            '10_minutes': 10 * 60,
            '1_hour': 60 * 60,
            '1_day': 24 * 60 * 60,
            '1_week': 7 * 24 * 60 * 60,
            '1_month': 30 * 24 * 60 * 60,
            '1_year': 365 * 24 * 60 * 60,
            'never': None,
            'burn_after_read': None,
        }[expiration]

    async def get_paste_by_pk(self, pk: str | UUID) -> PasteSchema:
        result = await self.db_adapter.execute(select(Paste).where(Paste.id == pk))
        paste = result.scalar_one_or_none()
        if not paste:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        paste_obj = PasteSchema(
            id=paste.id,
            title=paste.title,
            text=self.s3_adapter.get_text_file(f'{paste.id}.txt'),
            expiration=paste.expiration,
            exposure=paste.exposure,
            created_at=paste.created_at,
        )
        if paste.expiration == ExpirationOption.BURN_AFTER_READ:
            burn_paste(paste_obj.id)
        return paste_obj

    async def get_pastes(
        self, page_size: int, page_number: int
    ) -> list[BasePasteSchema]:
        stmt = (
            select(Paste)
            .where(Paste.exposure == ExposureOption.PUBLIC)
            .order_by(desc(Paste.created_at))
            .offset((page_number - 1) * page_size)
            .limit(page_size)
        )
        result = await self.db_adapter.execute(stmt)
        pastes = result.scalars().all()
        return [BasePasteSchema.model_validate(paste) for paste in pastes]

    async def create_paste(
        self,
        title: str,
        text: str,
        expiration: ExpirationOption,
        exposure: ExposureOption,
    ) -> PasteSchema:
        new_paste = Paste(
            title=title,
            expiration=expiration,
            exposure=exposure,
        )        
        self.db_adapter.add(new_paste)
        await self.db_adapter.commit()
        await self.db_adapter.refresh(new_paste)
        self.s3_adapter.upload_text_file(text, f'{new_paste.id}.txt')
        paste_schema = PasteSchema.model_validate(new_paste)
        paste_schema.text = text
        countdown = self.__get_expiration_time(paste_schema.expiration.value)
        if countdown:
            burn_paste.apply_async(args=[paste_schema.id], countdown=countdown)
        return paste_schema


def get_pastes_service(
    minio: MinIOClient = Depends(get_minio_client),
    postgres: AsyncSession = Depends(get_async_session),
) -> PastesService:
    return PastesService(db_adapter=postgres, s3_adapter=minio)
