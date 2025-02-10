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

from ..database import Base


class Tweet(Base):
    __tablename__ = "tweets"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"), nullable=False)
    tweet_data: Mapped[str] = mapped_column(Text, nullable=False)
    medias: Mapped[list[int] | None] = mapped_column(ARRAY(Integer), nullable=True)

    user: Mapped["User"] = relationship(back_populates="tweets")
