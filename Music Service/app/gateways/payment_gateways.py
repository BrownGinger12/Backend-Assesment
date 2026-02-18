import httpx
from dotenv import load_dotenv
import os

load_dotenv()

async def expensive_gateway(payload: dict, idempotency_key: str):
    base_url = os.getenv("EXTERNAL_API_URL")

    if not base_url:
        raise ValueError("EXTERNAL_API_URL is not set in .env")

    headers = {
        "Content-Type": "application/json",
        "x-idempotency-key": idempotency_key
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{base_url}/transactions/expensive",
            json=payload,
            headers=headers
        )

    response.raise_for_status()
    return response.json()

async def cheap_gateway(payload: dict, idempotency_key: str):
    base_url = os.getenv("EXTERNAL_API_URL")

    if not base_url:
        raise ValueError("EXTERNAL_API_URL is not set in .env")

    headers = {
        "Content-Type": "application/json",
        "x-idempotency-key": idempotency_key
    }

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.post(
            f"{base_url}/transactions/cheap",
            json=payload,
            headers=headers
        )

    response.raise_for_status()
    return response.json()

