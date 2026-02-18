from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from models.transaction_song import TransactionSong
from models.transaction import Transaction
from models.song import Song
from schemas.transaction_song_schema import TransactionSongCreate
from gateways.payment_gateways import expensive_gateway, cheap_gateway


class TransactionSongService:
    @staticmethod
    def get_by_transaction(db: Session, transaction_id: int) -> list[TransactionSong]:
        return db.query(TransactionSong).filter(
            TransactionSong.transaction_id == transaction_id
        ).all()

    @staticmethod
    async def create(db: Session, ts_in: TransactionSongCreate, idempotency_key: str) -> list[TransactionSong]:
        try:
            processing_transaction = db.query(Transaction).filter(Transaction.idempotency_key == idempotency_key).first()

            if processing_transaction and processing_transaction.status in ["success", "failed"]:
                raise HTTPException(status_code=200, detail="transaction already done")

            
            existing_transaction = db.query(TransactionSong).filter(TransactionSong.idempotency_key == idempotency_key).all()

            if existing_transaction:
                 return existing_transaction
            
            existing_songs = db.query(Song).filter(Song.ref_no.in_(ts_in.song_ref_nos)).all()
            
            if not existing_songs:
                raise HTTPException(status_code=404, detail="Songs do not exist")
            
            total_amount = sum(song.price for song in existing_songs)

            transaction_total = float(total_amount)

            transaction_id = None

            try:
                if transaction_total < 10:
                    resp = await cheap_gateway({"total_amount": transaction_total}, idempotency_key)
                else:
                    resp = await expensive_gateway({"total_amount": transaction_total}, idempotency_key)
                transaction_id = resp.get("id")
                if not transaction_id:
                    raise HTTPException(status_code=500, detail="Gateway did not return transaction_id")
            except Exception as e:
                raise HTTPException(status_code=502, detail=f"Gateway error: {str(e)}")

            found_ref_nos = {song.ref_no for song in existing_songs}
            missing = [ref_no for ref_no in ts_in.song_ref_nos if ref_no not in found_ref_nos]
            if missing:
                raise HTTPException(status_code=404, detail=f"Songs not found: {missing}")

            results = []
            for song in existing_songs:
                existing = db.query(TransactionSong).filter(
                    TransactionSong.transaction_id == transaction_id,
                    TransactionSong.song_ref_no == song.ref_no
                ).first()
                if existing:
                    results.append(existing)
                    continue

                ts = TransactionSong(
                    transaction_id=transaction_id,
                    song_ref_no=song.ref_no,
                    idempotency_key=idempotency_key
                )
                db.add(ts)
                results.append(ts)

            db.commit()
            for ts in results:
                db.refresh(ts)
            return results
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    @staticmethod
    def delete(db: Session, transaction_id: int) -> None:
        try:
            deleted_count = db.query(TransactionSong).filter(
                TransactionSong.transaction_id == transaction_id
            ).delete(synchronize_session=False)

            if deleted_count == 0:
                raise HTTPException(
                    status_code=404,
                    detail="Transaction song link not found"
                )

            db.commit()

            return {
                    "message": "Transaction songs deleted successfully",
                    "deleted_count": deleted_count
                }

        except SQLAlchemyError as e:
            db.rollback()
            raise e
