# app/services/song_service.py
from sqlalchemy.orm import Session
from app.models.song import Song
from app.schemas.song_schema import SongCreate, SongUpdate

class SongService:
    @staticmethod
    def create(db: Session, song_in: SongCreate) -> Song:
        song = Song(**song_in.model_dump())
        db.add(song)
        db.commit()
        db.refresh(song)
        return song

    @staticmethod
    def get(db: Session, song_id: int) -> Song | None:
        return db.query(Song).filter(Song.id == song_id).first()
    
    @staticmethod
    def get_by_ref(db: Session, ref_no: str) -> Song | None:
        return db.query(Song).filter(Song.ref_no == ref_no).first()

    @staticmethod
    def list(db: Session) -> list[Song]:
        return db.query(Song).all()

    @staticmethod
    def update(db: Session, song_id: int, song_in: SongUpdate) -> Song | None:
        song = db.query(Song).filter(Song.id == song_id).first()
        if not song:
            return None
        for field, value in song_in.model_dump(exclude_unset=True).items():
            setattr(song, field, value)
        db.commit()
        db.refresh(song)
        return song

    @staticmethod
    def delete(db: Session, song_id: int) -> bool:
        song = db.query(Song).filter(Song.id == song_id).first()
        if not song:
            return False
        db.delete(song)
        db.commit()
        return True
