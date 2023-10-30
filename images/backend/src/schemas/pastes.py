from uuid import UUID
from datetime import datetime

from pydantic import Field

from models.pastes import ExpirationOption, ExposureOption
from schemas.base import CustomBaseSchema


class BasePasteSchema(CustomBaseSchema):
    id: UUID = Field(alias='uuid')
    title: str
    created_at: datetime


class PasteSchema(BasePasteSchema):
    text: str | None = None
    expiration: ExpirationOption
    exposure: ExposureOption


class CreatePasteSchema(CustomBaseSchema):
    title: str
    text: str | None = None
    expiration: ExpirationOption
    exposure: ExposureOption
