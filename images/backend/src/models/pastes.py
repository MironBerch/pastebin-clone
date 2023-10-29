import uuid
from enum import Enum
from datetime import datetime

from sqlalchemy import Column, String, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from db.postgres import Base


class ExpirationOption(Enum):
    TEN_MINUTES = '10_minutes'
    ONE_HOUR = '1_hour'
    ONE_DAY = '1_day'
    ONE_WEEK = '1_week'
    ONE_MONTH = '1_month'
    ONE_YEAR = '1_year'
    NEVER = 'never'
    BURN_AFTER_READ = 'burn_after_read'


class ExposureOption(Enum):
    PUBLIC = 'public'
    UNLISTED = 'unlisted'


class Paste(Base):
    __tablename__ = 'pastes'

    id: Column = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    title: Column[str] = Column(String(length=255), nullable=False)

    expiration: Column[ExpirationOption] = Column(
        SQLAlchemyEnum(ExpirationOption),
        default=ExpirationOption.NEVER,
        nullable=False,
    )
    exposure: Column[ExposureOption] = Column(
        SQLAlchemyEnum(ExposureOption),
        default=ExposureOption.PUBLIC,
        nullable=False,
    )

    created_at: Column[datetime] = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
