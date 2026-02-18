from pydantic import BaseModel, Field, model_validator, ConfigDict
from decimal import Decimal
from enum import Enum
from typing import List
from datetime import datetime

class TransactionStatus(str, Enum):
    processing = "processing"
    success = "success"
    failed = "failed"


class TransactionBase(BaseModel):
    total_amount: Decimal   

class TransactionUpdate(BaseModel):
    status: TransactionStatus | None = Field(None, description="Only accepts processing, success, and failed")


class TransactionCreate(TransactionBase):
    pass


class TransactionResponse(TransactionBase):
    id: int
    created_at: datetime
    payment_type: str
    status: str

    class Config:
        from_attributes = True
    