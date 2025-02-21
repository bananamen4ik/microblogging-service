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
from sqlalchemy.ext.associationproxy import (
    association_proxy,
    AssociationProxy
)

from app.database import Base

if TYPE_CHECKING:  # pragma: no cover
    from app.models.users import User
    from app.models.medias import Media
    from app.models.likes import Like


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

    user: Mapped["User"] = relationship(
        "User",
        back_populates="tweets"
    )
    medias_objs: Mapped[list["Media"]] = relationship(
        "Media",
        back_populates="tweet"
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="tweet"
    )

    medias_filenames: AssociationProxy[list[str]] = association_proxy(
        "medias_objs",
        "filename"
    )

    @property
    def likes_users_data(self) -> list["User"]:
        """Instead of association_proxy return connection likes-user."""
        return [like.user for like in self.likes]
