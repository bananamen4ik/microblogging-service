from sqlalchemy import (
    Integer,
    ForeignKey
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from ..database import Base


class Follow(Base):
    __tablename__ = "follows"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id_follower: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    user_id_following: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
