from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class TransactionSong(Base):
    __tablename__ = "transaction_songs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    idempotency_key: Mapped[str] = mapped_column(String(255), nullable=False)
    transaction_id: Mapped[int] = mapped_column(Integer, ForeignKey("transactions.id"), nullable=False)
    song_ref_no: Mapped[str] = mapped_column(String(36), ForeignKey("songs.ref_no"), nullable=False)
    song: Mapped["Song"] = relationship("Song", back_populates="transaction_songs")