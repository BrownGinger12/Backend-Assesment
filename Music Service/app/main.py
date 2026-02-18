# app/main.py
from fastapi import FastAPI
from database import Base, engine
from routes.song_routes import router as song_router
from routes.transaction_song_routes import router as transaction_song_router
from routes.owned_song_routes import router as owned_song_router
from routes.playlist_routes import router as playlist_router
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Music API",
    description="API for managing songs and playlists",
    version="1.0.0"
)

app.include_router(song_router)
app.include_router(transaction_song_router)
app.include_router(owned_song_router)
app.include_router(playlist_router)

@app.get("/")
def root():
    return {"message": "Welcome to the Music API"}