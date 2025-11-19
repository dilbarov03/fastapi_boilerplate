from datetime import datetime
from typing import Annotated
from sqlalchemy import DateTime
from sqlmodel import Field, SQLModel
from app.core.config import settings


class BaseSQLModel(SQLModel):
    created_at: Annotated[
        datetime,
        Field(
            sa_type=DateTime(timezone=False),
            default_factory=lambda: datetime.now(tz=settings.DEFAULT_TIMEZONE).replace(tzinfo=None),
            nullable=False,
        ),
    ]

    changed_at: Annotated[
        datetime | None,
        Field(
            sa_type=DateTime(timezone=False),
            default=None,
            sa_column_kwargs={
                "onupdate": lambda: datetime.now(tz=settings.DEFAULT_TIMEZONE).replace(tzinfo=None),
            },
        ),
    ]
