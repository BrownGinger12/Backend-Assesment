from pydantic import BaseModel, ConfigDict
from schemas.song_schema import SongResponse


class OwnedSongCreate(BaseModel):
    transaction_id: int


class OwnedSongResponse(BaseModel):
    id: int
    ref_no: str
    song: SongResponse

    model_config = ConfigDict(from_attributes=True)