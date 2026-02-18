from pydantic import BaseModel, ConfigDict
from schemas.owned_song_schema import OwnedSongResponse


class PlaylistAdd(BaseModel):
    song_ref_no: str

class PlaylistResponse(BaseModel):
    id: int
    owned_song: OwnedSongResponse

    model_config = ConfigDict(from_attributes=True)

class MessageResponse(BaseModel):
    message: str