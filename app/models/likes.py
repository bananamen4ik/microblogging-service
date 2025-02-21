"""Describe Like model in database."""

from typing import TYPE_CHECKING

from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.tweets import Tweet
    from app.models.users import User


class Like(Base):
    """DB Like model."""

    __tablename__ = "likes"
    __table_args__ = (
        UniqueConstraint(
            "user_id",
            "tweet_id",
            name="uq_user_tweet"
        ),
    )

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
        ForeignKey("tweets.id", ondelete="CASCADE"),
        nullable=False
    )

    tweet: Mapped["Tweet"] = relationship(
        "Tweet",
        back_populates="likes"
    )
    user: Mapped["User"] = relationship(
        "User",
        back_populates="likes"
    )
