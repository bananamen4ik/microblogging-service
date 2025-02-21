"""Describe Media model in database."""

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

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.tweets import Tweet


class Media(Base):
    """DB Media model."""

    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    ext: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    tweet_id: Mapped[int | None] = mapped_column(
        Integer,
        ForeignKey("tweets.id", ondelete="CASCADE"),
        nullable=True
    )

    tweet: Mapped["Tweet"] = relationship(
        "Tweet",
        back_populates="medias_objs"
    )

    @property
    def filename(self):
        """Get media filename."""
        return f"{self.id}.{self.ext}"
