# routes/transaction_song_route.py
from fastapi import APIRouter, Depends, Header, HTTPException
from sqlalchemy.orm import Session
from database import get_db
from services.transaction_song_service import TransactionSongService
from schemas.transaction_song_schema import TransactionSongCreate, TransactionSongResponse

router = APIRouter(prefix="/transaction-songs", tags=["Transaction Songs"])


@router.get("/transaction/{transaction_id}", response_model=list[TransactionSongResponse])
def get_by_transaction(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    return TransactionSongService.get_by_transaction(db, transaction_id)


@router.post("/", response_model=list[TransactionSongResponse])
async def create_transaction_song(
    ts_in: TransactionSongCreate,
    idempotency_key: str = Header(..., alias="x-idempotency-key"),
    db: Session = Depends(get_db)
):
    return await TransactionSongService.create(db, ts_in, idempotency_key)


@router.delete("/{transaction_id}", status_code=204)
def delete_transaction_song(
    transaction_id: int,
    db: Session = Depends(get_db)
):
    TransactionSongService.delete(db, transaction_id)