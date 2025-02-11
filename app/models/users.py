"""Describe User model in database."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base

if TYPE_CHECKING:
    from app.models.tweets import Tweet


class User(Base):
    """DB User model."""

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    api_key: Mapped[str] = mapped_column(
        Text,
        unique=True,
        nullable=False
    )
    name: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    tweets: Mapped[list["Tweet"]] = relationship(back_populates="user")
