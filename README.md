# PolicyDB Chatbot — Ingenuity

An AI-powered chatbot that answers natural-language questions about La Trobe University policy using Retrieval-Augmented Generation (RAG), grounding every answer in official Policy Database text and citing its sources. Built as a capstone project for handover to La Trobe as the project owner.

## What it does

Staff, students, and administrators can ask plain-English questions about university policy and get:
- An answer generated strictly from official policy excerpts — never the model's own general knowledge
- Citations linking back to the specific policy section and source URL
- A clear escalation message (with contact routing) when the question falls outside what's covered, rather than a guessed answer
- A compliance disclaimer on every response

## Architecture

- **data-pipeline/** — Scrapes, cleans, chunks, and embeds La Trobe policy pages into Postgres (pgvector). Also runs hybrid (vector + BM25) retrieval and reranking.
- **generation/** — Wraps retrieval in grounded LLM generation via Ollama: relevance thresholding, refusal detection, prompt-injection filtering, and citation building.
- **backend/** — FastAPI layer exposing `/ask` and `/health`, with API key auth, rate limiting, audit logging, and a scheduled job that refreshes policy content periodically.
- **frontend/** — React + Vite chat interface.
- **docs/** — Retrieval/generation test results and corpus notes.

Each folder has its own README with setup specifics; this file covers the project as a whole.

## Tech stack

- **Frontend:** React, Vite
- **Backend:** FastAPI, Uvicorn
- **Retrieval:** PostgreSQL + pgvector, sentence-transformers embeddings, BM25 hybrid search, cross-encoder reranking
- **Generation:** Ollama (qwen3), running locally
- **Ops:** APScheduler (scheduled content refresh), slowapi (rate limiting), SQLite (query audit log)

## Local development setup

1. **Postgres + pgvector:** `docker run --name policydb-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d ankane/pgvector`
2. **Populate the database** — in `data-pipeline/`: `pip install -r requirements.txt`, then run `scrape_policies.py`, `clean_and_chunk.py`, `build_vector_db.py` in order (see `data-pipeline/README.md` for the full policy discovery process)
3. **Ollama:** install from ollama.com, then `ollama pull qwen3`
4. **Backend:** in `backend/`, `pip install -r requirements.txt`, copy `.env.example` to `.env` and set `API_KEY`, then `python main.py`
5. **Frontend:** in `frontend/`, `npm install`, copy `.env.example` to `.env` (set `VITE_API_KEY` to match the backend), then `npm run dev`
6. Open the printed local URL (usually `http://localhost:5173`) and ask a question

## Demo Hosting (PCOIS2-74)

The chatbot is demonstrated via a public URL without requiring anyone else to run code, using Cloudflare Tunnel to expose a locally-running stack.

### Why not fully cloud-hosted
Postgres and the frontend/backend could be hosted for free, but Ollama (the local LLM server) needs more RAM/CPU than free hosting tiers provide. With no project budget, the backend and Ollama run on a team member's machine, tunneled to a public URL for the duration of the demo. This is an accepted scope decision, not an oversight.

### Required setup
**Quickest option:** if Docker, Python, Node, `cloudflared`, and Ollama are already installed, double-click `start-demo.bat` in the repo root — it automates every step below, checks the database has data (offering to populate it if not), and opens the working demo link automatically. The manual steps are documented below for first-time setup, troubleshooting, or if the script isn't available.

1. Start Docker Postgres: `docker start policydb-pg`
2. Confirm Ollama is running: `ollama list` should show `qwen3` (Windows runs it as a background service automatically)
3. Backend: `cd backend && python main.py`
4. Frontend: `cd frontend && npm run dev`
5. Install cloudflared if needed: `winget install --id Cloudflare.cloudflared`
6. New terminal: `cloudflared tunnel --url http://localhost:8000` — copy the printed URL (backend)
7. Another new terminal: `cloudflared tunnel --url http://localhost:5173` — copy the printed URL (frontend)
8. In `backend/.env`, set `FRONTEND_ORIGINS` to include the frontend tunnel URL
9. In `frontend/.env`, set `VITE_API_BASE_URL` to the backend tunnel URL
10. Restart backend and frontend to pick up the new `.env` values
11. Open the frontend tunnel URL — that's the demo link

### Known limitations
- Tunnel URLs are ephemeral — they only change if the `cloudflared` commands themselves are restarted, not when the backend/frontend restart. Both tunnel terminals must stay open, and the host machine must stay awake, for the link to keep working.
- Since everything runs on one machine, that machine must remain on and connected for the full demo window.
- No custom/branded domain — `trycloudflare.com` URLs are randomly generated and can't be customized without purchasing a domain.

## Known limitations / future work

- **Policy roster is a manual snapshot.** Content of known policies refreshes automatically (see the backend's scheduled job), but the *list* of which policies currently exist is only updated by manually re-running `discover_policies.py` against a fresh copy of the Policy Library search results — new or expired policies aren't detected automatically.
- **Input validation is pattern-based**, not exhaustive against adversarial prompt injection.
- **No per-user authentication or role-based access** — the brief lists these as nice-to-have/optional, not implemented in this version.

## Viewing Audit Logs

Every `/ask` call is logged to `backend/policy_query_logs.db` (SQLite) — timestamp, question, retrieved chunks/citations, final answer, and metadata (confidence, status, response time). To inspect it, run from `backend/`:

- `python view_logs.py` — last 20 entries
- `python view_logs.py --limit 5` — last 5 entries

This file is gitignored and never committed — it contains real user question text.

## Project documentation

See `docs/` for retrieval and generation test results, and each subfolder's own README for module-specific detail.
