
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.song_schema import SongCreate, SongUpdate, SongResponse
from app.services.song_service import SongService

router = APIRouter(prefix="/songs", tags=["Songs"])

@router.post("/", response_model=SongResponse)
def create_song(song_in: SongCreate, db: Session = Depends(get_db)):
    return SongService.create(db, song_in)

@router.get("/", response_model=List[SongResponse])
def list_songs(db: Session = Depends(get_db)):
    return SongService.list(db)

@router.get("/{song_id}", response_model=SongResponse)
def get_song(song_id: int, db: Session = Depends(get_db)):
    song = SongService.get(db, song_id)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


@router.get("/{refNo}", response_model=SongResponse)
def get_song_by_ref(refNo: str, db: Session = Depends(get_db)):
    song = SongService.get_by_ref(db, refNo)
    

@router.patch("/{song_id}", response_model=SongResponse)
def update_song(song_id: int, song_in: SongUpdate, db: Session = Depends(get_db)):
    song = SongService.update(db, song_id, song_in)
    if not song:
        raise HTTPException(status_code=404, detail="Song not found")
    return song


# DELETE
@router.delete("/{song_id}", status_code=204)
def delete_song(song_id: int, db: Session = Depends(get_db)):
    success = SongService.delete(db, song_id)
    if not success:
        raise HTTPException(status_code=404, detail="Song not found")
    return None
