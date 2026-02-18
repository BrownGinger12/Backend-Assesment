from pydantic import BaseModel,Field

class TransactionSongBase(BaseModel):
    song_ref_nos: list[str] = Field(..., min_length=1, description="At least one song ref_no is required")

class TransactionSongCreate(TransactionSongBase):
    pass

class TransactionSongResponse(BaseModel):
    id: int
    transaction_id: int
    song_ref_no: str
    idempotency_key: str

    class Config:
        from_attributes = True
