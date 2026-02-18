from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Playlist(Base):
    __tablename__ = "playlist"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ref_no: Mapped[str] = mapped_column(String(36), ForeignKey("owned_songs.ref_no"), nullable=False)

    owned_song: Mapped["OwnedSong"] = relationship("OwnedSong", back_populates="playlist")