"""Describe Media model in database."""

from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Media(Base):
    """DB Media model."""

    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
