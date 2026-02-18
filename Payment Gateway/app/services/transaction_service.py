from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from models.transaction import Transaction
from fastapi import HTTPException
from schemas.transaction_schema import TransactionCreate, TransactionUpdate
from gateways.music_wevhook import add_music_webhook

class TransactionService:
    @staticmethod
    def purchase(db: Session, 
            transaction_in: TransactionCreate, 
            idempotency_key: str, 
            payment_type: str
        ) -> Transaction:
        try:
            existing_transaction = db.query(Transaction).filter(Transaction.idempotency_key == idempotency_key).first()

            if existing_transaction:
                return existing_transaction
            
            transaction_data = Transaction(**transaction_in.model_dump())

            transaction_data.payment_type = payment_type
            transaction_data.idempotency_key = idempotency_key

            db.add(transaction_data)
            db.commit()
            db.refresh(transaction_data)
            return transaction_data
        except SQLAlchemyError as e:
            db.rollback()
            raise e
    
    @staticmethod
    async def update_status(
        db: Session,
        transaction_in: TransactionUpdate,
        transaction_id: int
    ) -> Transaction:

        try:
            transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()

            if not transaction:
                raise HTTPException(status_code=404, detail="Transaction not found")

            update_data = transaction_in.model_dump(exclude_unset=True)

            for key, value in update_data.items():
                setattr(transaction, key, value)

            if update_data["status"] == "success":
                try:
                    await add_music_webhook({"transaction_id": int(transaction.id)})
                except Exception as e:
                    db.rollback()
                    raise HTTPException(status_code=502,detail=f"Webhook failed: {str(e)}")

            db.commit()
            db.refresh(transaction)

            return transaction

        except SQLAlchemyError:
            db.rollback()
            raise HTTPException(
                status_code=500,
                detail="Database error while updating transaction"
            )
