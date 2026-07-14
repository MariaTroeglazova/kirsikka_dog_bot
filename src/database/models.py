from datetime import datetime
from sqlalchemy import String, DateTime, Float, func
from sqlalchemy.orm import Mapped, mapped_column
from .connection import Base

class DogProfile(Base):
    __tablename__ = "dog_profile"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(30), default="Кирси")
    birth_date: Mapped[datetime | None] = mapped_column(DateTime, default=datetime(2024, 12, 7))
    weight: Mapped[float | None] = mapped_column(Float, default=9)
    breed: Mapped[str | None] = mapped_column(String(50), default="Американский голый терьер")
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
