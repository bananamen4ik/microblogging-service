"""Describe Like model in database."""

from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


class Like(Base):
    """DB Like model."""

    __tablename__ = "likes"

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
    tweet_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("tweets.id"),
        nullable=False
    )
