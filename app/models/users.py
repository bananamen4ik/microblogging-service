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

if TYPE_CHECKING:  # pragma: no cover
    from app.models.tweets import Tweet
    from app.models.likes import Like
    from app.models.follows import Follow


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

    tweets: Mapped[list["Tweet"]] = relationship(
        "Tweet",
        back_populates="user"
    )
    likes: Mapped[list["Like"]] = relationship(
        "Like",
        back_populates="user"
    )
    followers: Mapped[list["Follow"]] = relationship(
        "Follow",
        back_populates="following",
        foreign_keys="Follow.user_id_following"
    )
    following: Mapped[list["Follow"]] = relationship(
        "Follow",
        back_populates="follower",
        foreign_keys="Follow.user_id_follower"
    )

    @property
    def followers_users(self) -> list["User"]:
        """Instead of association_proxy return connection follows-user."""
        return [follow.follower for follow in self.followers]

    @property
    def following_users(self) -> list["User"]:
        """Instead of association_proxy return connection follows-user."""
        return [follow.following for follow in self.following]
