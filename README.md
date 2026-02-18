# 🎵 Music Service API

## 📌 Project Overview

Developed a music service backend with full CRUD functionalities for songs, playlists, transactions, and ownership tracking. Implemented transactional logic with idempotency keys to prevent duplicate API calls.

---

## ✨ Key Features

1. **Songs** — Create, read, update, delete songs. Endpoints return songs by ID or reference number.
2. **Playlists** — Manage user playlists linked to owned songs only; includes adding, removing, shuffling, and ordered retrieval.
3. **Transactions** — Handle song purchases with external gateways (`cheap` and `expensive`). Ensures idempotent transactions and proper status handling (`success`, `failed`, `processing`).
4. **Owned Songs** — Add purchased songs to the user's library; validated via transaction status.
5. **Webhook Integration** — Automatically sync purchased songs to the owned songs endpoint; includes rollback on failure.

---

## 🛠 Technical Highlights

- **FastAPI** for RESTful API endpoints.
- **SQLAlchemy ORM** with PostgreSQL/MySQL.
- **Idempotency key** mechanism to prevent duplicate transactions.
- **Async HTTP calls** using `httpx` for gateway and webhook integration.
- **Pydantic models** with `model_dump` for request/response validation.
- **Environment configuration** via `.env` for external services.

---

## ⚠️ Error Handling & Validation

- Proper HTTP status codes for `404`, `422`, `500`, and `502`.
- Validation for owned songs, missing references, and transaction processing states.
- Decimal handling and JSON serialization fixes.

---

## 🚀 Getting Started

### Prerequisites
- Python 3.10+
- MySQL

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/music-service.git
cd music-service

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Running the Services

**Music Service**
```bash
cd "Music Service"
uvicorn app.main:app --reload
```

**Payment Gateway** (runs on a different port)
```bash
cd "Payment Gateway"
uvicorn app.main:app --reload --port 9000
```

### Environment Variables

Both services require a `.env` file. An `example.env` template is provided in each service directory — copy and fill in the required values:

```bash
cp example.env .env
```

---

## 📡 API Documentation & Testing

A Postman documentation and test file is included in the repository. Import it into Postman to explore and test all available API endpoints.
