"""Describe Tweet model in database."""

from sqlalchemy import (
    Integer,
    Text,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)
from sqlalchemy.dialects.postgresql import ARRAY

from app.database import Base


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
    main_content: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    medias: Mapped[list[int] | None] = mapped_column(
        ARRAY(Integer),
        nullable=True
    )
