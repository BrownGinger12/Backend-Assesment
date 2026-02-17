from sqlalchemy import String, Integer, DateTime, Numeric
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from decimal import Decimal
import uuid
from app.database import Base


class Song(Base):
    __tablename__ = "songs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    ref_no: Mapped[str] = mapped_column(
        String(36),
        unique=True,
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )

    title: Mapped[str] = mapped_column(String(255), nullable=False)

    length: Mapped[int] = mapped_column(Integer, nullable=False)

    date_released: Mapped[datetime] = mapped_column(DateTime, nullable=False)

    price: Mapped[Decimal] = mapped_column(
        Numeric(10, 2),
        nullable=False
    )
