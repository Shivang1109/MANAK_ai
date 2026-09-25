# ManakAI 🏛️
### AI-Powered Conversational Assistant for Indian Standards & BIS Services
**Smart India Hackathon 2026 | Problem Statement SIH26107 | Team BISync**

---

## What It Does

ManakAI helps industries, MSMEs, startups, and consumers navigate the Bureau of Indian Standards (BIS) ecosystem using natural language. Instead of searching through hundreds of PDFs, users ask questions and get **grounded, citation-backed answers** in seconds.

**Key capabilities:**
- 💬 Conversational Q&A on Indian Standards (IS numbers, clauses, requirements)
- 🔎 Find applicable standards by describing a product in plain language
- 📋 Step-by-step BIS certification guidance (Scheme I, II, III, CRS, FMCS)
- 🏅 Hallmarking guidance (gold/silver purity, HUID, process, fees)
- 🔬 NABL testing lab suggestions by product and region
- 📄 Clause/page-level source citations on every answer
- 👍 Answer feedback loop → Admin analytics dashboard

---

## Architecture

```
Browser (React)
    ↓ JWT
Spring Boot API (port 8080)
    ↓ Internal call
FastAPI RAG Service (port 8000)
    ↓                    ↓
ChromaDB             Google Gemini 2.0 Flash
(4000+ BIS chunks)   (free LLM — Ollama fallback)
    ↑
PostgreSQL (users, conversations, feedback)
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + TypeScript + Vite + TailwindCSS |
| Backend API | Spring Boot 3.2 (Java 17) + JWT Auth |
| RAG Engine | FastAPI (Python) + ChromaDB + SentenceTransformers |
| LLM | Google Gemini 2.0 Flash (free) — Ollama local fallback |
| Embeddings | sentence-transformers/all-MiniLM-L6-v2 |
| Database | PostgreSQL 16 |

---

## Prerequisites

- Java 17+ and Maven 3.9+
- Python 3.11–3.13
- Node.js 18+ and npm
- PostgreSQL 16 running locally
- Google Gemini API key (free at https://makersuite.google.com/app/apikey)

---

## First-Time Setup

### 1. Database
```bash
psql -U postgres -c "CREATE USER manakai_user WITH PASSWORD 'password';"
psql -U postgres -c "CREATE DATABASE manakai OWNER manakai_user;"
psql -h localhost -U manakai_user -d manakai -f backend-api/schema-fixed.sql
```

### 2. RAG Service
```bash
cd rag-service
pip install -r requirements.txt
# Set GOOGLE_API_KEY in rag-service/.env
python add_hallmarking_schemes_data.py
python add_nabl_labs_data.py
python add_expanded_demo_data.py
```

### 3. Frontend
```bash
cd frontend && npm install
```

---

## Running the App (3 terminals)

**Terminal 1 — RAG Service (start first)**
```bash
cd rag-service
export PYTHONPATH="$(pwd)/src:$PYTHONPATH"
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Backend API**
```bash
cd backend-api
export POSTGRES_DB=manakai POSTGRES_USER=manakai_user POSTGRES_PASSWORD=password
mvn spring-boot:run
```

**Terminal 3 — Frontend**
```bash
cd frontend && npm run dev
```

Open **http://localhost:3000**

---

## Demo Credentials

| Role | Email | Password |
|------|-------|----------|
| User | demo@manakai.in | demo123 |
| Admin | admin@manakai.in | admin123 |

---

## Try These Queries

- "What are the requirements for LED bulbs under BIS?"
- "How do I get BIS certification for my product as an MSME?"
- "What is hallmarking? How do I get a hallmarking licence?"
- "Which NABL lab can test my electrical products?"
- "Explain BIS Scheme I vs CRS registration"
- "What are the chemical requirements for cement under IS 269?"

---

## How the RAG Pipeline Works

```
User query
  → QueryProcessor (intent detection + IS number extraction)
  → EmbeddingService (MiniLM → 384-dim vector)
  → HybridRetriever (ChromaDB cosine similarity, top-10)
  → ReRanker (cross-encoder scoring, top-5)
  → LLMService (Gemini 2.0 Flash with grounded prompting)
  → Citation extraction ([Source N, Clause X.Y])
  → Answer with confidence score
```

If confidence < 0.5, system shows "Insufficient evidence" instead of hallucinating.

---

## Environment Variables

**rag-service/.env**
```
GOOGLE_API_KEY=your_gemini_api_key_here
OLLAMA_HOST=http://localhost:11434
```

**backend-api/.env**
```
POSTGRES_HOST=localhost
POSTGRES_DB=manakai
POSTGRES_USER=manakai_user
POSTGRES_PASSWORD=password
JWT_SECRET=your_jwt_secret
RAG_SERVICE_URL=http://localhost:8000
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```
