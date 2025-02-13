"""Describe Tweet model in database."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base

if TYPE_CHECKING:
    from app.models.users import User  # pragma: no cover


class Tweet(Base):
    """DB Tweet model."""

    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    tweet_data: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    medias: Mapped[list[int] | None] = mapped_column(
        ARRAY(Integer),
        nullable=True
    )

    user: Mapped["User"] = relationship(back_populates="tweets")
