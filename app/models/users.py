"""Describe User model in database."""

from sqlalchemy import (
    Integer,
    Text
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database import Base


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
