from sqlalchemy import Integer
from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from ..database import Base


class Media(Base):
    __tablename__ = "medias"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False)
