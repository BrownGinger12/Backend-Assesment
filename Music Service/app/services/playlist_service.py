# services/playlist_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from models.playlist import Playlist
from models.owned_song import OwnedSong
from schemas.playlist_schema import PlaylistAdd
import random


class PlaylistService:
    @staticmethod
    def get_all(db: Session) -> list[Playlist]:
        try:
            return db.query(Playlist).all()
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def shuffle(db: Session) -> list[Playlist]:
        try:
            playlist = db.query(Playlist).all()
            if not playlist:
                raise HTTPException(status_code=404, detail="Playlist is empty")
            random.shuffle(playlist)
            return playlist
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def add(db: Session, playlist_in: PlaylistAdd) -> Playlist:
        try:
            owned_song = db.query(OwnedSong).filter(
                OwnedSong.ref_no == playlist_in.song_ref_no
            ).first()
            if not owned_song:
                raise HTTPException(status_code=404, detail="Owned song not found")

            existing = db.query(Playlist).filter(
                Playlist.ref_no == playlist_in.song_ref_no
            ).first()
            if existing:
                raise HTTPException(status_code=409, detail="Song already in playlist")

            playlist = Playlist(ref_no=playlist_in.song_ref_no)
            db.add(playlist)
            db.commit()
            db.refresh(playlist)
            return playlist
        except SQLAlchemyError as e:
            db.rollback()
            raise e

    @staticmethod
    def remove(db: Session, song_ref_no: str) -> dict:
        try:
            playlist = db.query(Playlist).filter(Playlist.ref_no == song_ref_no).first()
            if not playlist:
                raise HTTPException(status_code=404, detail="Song not found in the playlist")
            db.delete(playlist)
            db.commit()
            return {"message": "Song removed to playlist"}
        
        except SQLAlchemyError as e:
            db.rollback()
            raise e