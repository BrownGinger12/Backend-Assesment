from fastapi import FastAPI
from database import Base, engine
from routes.transaction_route import router as transaction_route
from dotenv import load_dotenv

load_dotenv()

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Expensive Gateway",
    version="1.0.0"
)

app.include_router(transaction_route)

@app.get("/")
def root():
    return {"message": "This is the expensive gateway"}
