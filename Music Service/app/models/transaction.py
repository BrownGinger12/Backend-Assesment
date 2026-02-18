from sqlalchemy import String, DateTime, Numeric, String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
from decimal import Decimal
from database import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    total_amount: Mapped[Decimal] = mapped_column(Numeric(10,2), nullable=False)
    payment_type: Mapped[str] = mapped_column(String(50), nullable=False, default="expensive")
    status: Mapped[str] = mapped_column(String(50), nullable=False, default="processing")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())