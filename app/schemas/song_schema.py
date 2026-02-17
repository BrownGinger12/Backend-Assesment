from pydantic import BaseModel, Field
from datetime import datetime
from decimal import Decimal

class SongBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    length: int = Field(..., gt=0)
    date_released: datetime
    price: Decimal = Field(..., gt=0)


class SongCreate(SongBase):
    pass


class SongUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=255)
    length: int | None = Field(None, gt=0)
    date_released: datetime | None = None
    price: Decimal | None = Field(None, gt=0)


class SongResponse(SongBase):
    id: int
    ref_no: str
    
    class Config:
        from_attributes = True
