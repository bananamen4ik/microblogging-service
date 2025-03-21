"""Describe Follow model in database."""

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
    from app.models.users import User


class Follow(Base):
    """DB Follow model."""

    __tablename__ = "follows"
    __table_args__ = (
        UniqueConstraint(
            "user_id_follower",
            "user_id_following",
            name="uq_follower_following"
        ),
    )

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    user_id_follower: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )
    user_id_following: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    following: Mapped["User"] = relationship(
        "User",
        back_populates="followers",
        foreign_keys=[user_id_following]
    )
    follower: Mapped["User"] = relationship(
        "User",
        back_populates="following",
        foreign_keys=[user_id_follower]
    )
