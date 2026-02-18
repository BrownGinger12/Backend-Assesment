from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.owned_song_service import OwnedSongService
from schemas.owned_song_schema import OwnedSongCreate, OwnedSongResponse

router = APIRouter(prefix="/owned-songs", tags=["Owned Songs"])


@router.get("/", response_model=list[OwnedSongResponse])
def get_all(db: Session = Depends(get_db)):
    return OwnedSongService.get_all(db)

@router.get("/ref/{song_ref_no}", response_model=OwnedSongResponse)
def get_all(song_ref_no: str, db: Session = Depends(get_db)):
    return OwnedSongService.get_by_ref(db, song_ref_no)


@router.post("/", response_model=list[OwnedSongResponse])
def add_songs(
    owned_song_in: OwnedSongCreate,
    db: Session = Depends(get_db)
):
    return OwnedSongService.add(db, owned_song_in)