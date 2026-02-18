# routes/playlist_routes.py
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from services.playlist_service import PlaylistService
from schemas.playlist_schema import PlaylistAdd, PlaylistResponse

router = APIRouter(prefix="/playlist", tags=["Playlist"])


@router.get("/", response_model=list[PlaylistResponse])
def get_all(db: Session = Depends(get_db)):
    return PlaylistService.get_all(db)


@router.get("/shuffle", response_model=list[PlaylistResponse])  # ✅ Before /{id}
def shuffle(db: Session = Depends(get_db)):
    return PlaylistService.shuffle(db)


@router.post("/", response_model=PlaylistResponse)
def add(playlist_in: PlaylistAdd, db: Session = Depends(get_db)):
    return PlaylistService.add(db, playlist_in)


@router.delete("/{song_ref_no}", status_code=204)
def remove(song_ref_no: str, db: Session = Depends(get_db)):
    PlaylistService.remove(db, song_ref_no)