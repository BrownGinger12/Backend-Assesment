# services/owned_song_service.py
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from models.owned_song import OwnedSong
from schemas.owned_song_schema import OwnedSongCreate, OwnedSongResponse
from models.transaction import Transaction
from models.transaction_song import TransactionSong

    
class OwnedSongService:
    @staticmethod
    def get_all(db: Session) -> list[OwnedSong]:
        try:
            return db.query(OwnedSong).all()
        except SQLAlchemyError as e:
            raise e
    
    @staticmethod
    def get_by_ref(db: Session, song_ref_no: str) -> OwnedSong:
        try:
            owned_song = db.query(OwnedSong).filter(OwnedSong.ref_no == song_ref_no).first() 
            if not owned_song:
                raise HTTPException(status_code=404, detail=f"Owned song {song_ref_no} not found")
            return owned_song
        except SQLAlchemyError as e:
            raise e

    @staticmethod
    def add(db: Session, owned_music_in: OwnedSongCreate) -> list[OwnedSong]:
        try:
            existing_transaction = db.query(Transaction).filter(
                Transaction.id == owned_music_in.transaction_id
            ).first()

            if not existing_transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            if existing_transaction and existing_transaction.status in ["success", "failed"]:
                raise HTTPException(status_code=200, detail="transaction already done")

            
            existing_songs = db.query(TransactionSong).filter(
                TransactionSong.transaction_id == owned_music_in.transaction_id
            ).all()

            if not existing_songs:
                raise HTTPException(status_code=404, detail="No songs found for transaction")

            results = []

            for song in existing_songs:
                already_owned = db.query(OwnedSong).filter(
                    OwnedSong.ref_no == song.song_ref_no
                ).first()

                if already_owned:
                    results.append(already_owned)
                    continue

                owned_song = OwnedSong(
                    ref_no=song.song_ref_no
                )

                db.add(owned_song)
                results.append(owned_song)

            db.commit()

            for owned_song in results:
                db.refresh(owned_song)

            return results

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(status_code=500, detail="Database error")
