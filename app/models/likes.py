"""Describe Like model in database."""

from sqlalchemy import (
    Integer,
    ForeignKey,
    UniqueConstraint
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


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
