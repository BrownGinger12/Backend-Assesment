from fastapi import APIRouter, Depends, HTTPException, Header
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.transaction_service import TransactionService
from schemas.transaction_schema import TransactionCreate, TransactionResponse, TransactionUpdate

router = APIRouter(prefix="/transactions", tags=["Transactions"])

@router.post("/expensive", response_model=TransactionResponse)
def purchase_songs(
    transaction_in: TransactionCreate,
    x_idempotency_key: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        transaction = TransactionService.purchase(db=db, transaction_in=transaction_in, idempotency_key=x_idempotency_key, payment_type="expensive")

        return transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/cheap", response_model=TransactionResponse)
def purchase_songs(
    transaction_in: TransactionCreate,
    x_idempotency_key: str = Header(...),
    db: Session = Depends(get_db)
):
    try:
        transaction = TransactionService.purchase(db=db, transaction_in=transaction_in, idempotency_key=x_idempotency_key, payment_type="cheap")

        return transaction
    except HTTPException as e:
        raise e
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=str(e)
        )

@router.patch(
    "/{transaction_id}",
    response_model=TransactionResponse,
    status_code=200
)
async def update_transaction(
    transaction_id: int,
    transaction_in: TransactionUpdate,
    db: Session = Depends(get_db)
):
    try:
        transaction = await TransactionService.update_status(db=db, transaction_id=transaction_id, transaction_in=transaction_in)
        return transaction

    except HTTPException as e:
        raise e

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
