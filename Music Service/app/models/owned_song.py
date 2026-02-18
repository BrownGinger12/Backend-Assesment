from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class OwnedSong(Base):
    __tablename__ = "owned_songs"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    ref_no: Mapped[str] = mapped_column(String(36), ForeignKey("songs.ref_no"), nullable=False)

    song: Mapped["Song"] = relationship("Song", back_populates="owned_songs")
    playlist: Mapped[list["Playlist"]] = relationship("Playlist", back_populates="owned_song")