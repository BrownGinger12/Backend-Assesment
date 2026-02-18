# app/services/song_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.song import Song
from schemas.song_schema import SongCreate, SongUpdate
from fastapi import HTTPException

class SongService:

    @staticmethod
    def create(db: Session, song_in: SongCreate) -> Song:
        try:
            song = Song(**song_in.model_dump())
            db.add(song)
            db.commit()
            db.refresh(song)
            return song
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def get(db: Session, song_id: int) -> Song | None:
        try:
            return db.query(Song).filter(Song.id == song_id).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def get_by_ref(db: Session, ref_no: str) -> Song | None:
        try:
            return db.query(Song).filter(Song.ref_no == ref_no).first()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def list(db: Session) -> list[Song]:
        try:
            return db.query(Song).all()
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def update(db: Session, song_id: int, song_in: SongUpdate) -> Song | None:
        try:
            song = db.query(Song).filter(Song.id == song_id).first()
            if not song:
                return None
            for field, value in song_in.model_dump(exclude_unset=True).items():
                setattr(song, field, value)
            db.commit()
            db.refresh(song)
            return song
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def delete(db: Session, song_id: int) -> bool:
        try:
            song = db.query(Song).filter(Song.id == song_id).first()
            if not song:
                return False
            db.delete(song)
            db.commit()
            return True
        except SQLAlchemyError as e:
            db.rollback()
            raise e
