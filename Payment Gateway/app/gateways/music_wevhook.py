import httpx
from dotenv import load_dotenv
import os

load_dotenv()

async def add_music_webhook(payload: dict):
    base_url = os.getenv("EXTERNAL_API_URL")

    if not base_url:
        raise ValueError("EXTERNAL_API_URL is not set in .env")

    url = f"{base_url}/owned-songs/"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

    response.raise_for_status()
    return response.json()
