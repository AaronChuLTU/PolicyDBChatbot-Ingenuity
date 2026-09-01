"""
PCOIS2-56: Wrap retrieval + generation into a callable API endpoint.

Turns generation/respond.py's answer_question() - already a complete
retrieve -> guard -> generate -> guard -> cite pipeline - into the HTTP
service Sprint 4's frontend calls instead of the policyApi.js mock
(PCOIS2-31).

    POST /ask   {"question": "..."}  ->  the PCOIS2-31 schema object
    GET  /health                     ->  liveness of Postgres + Ollama

This module deliberately contains no retrieval, generation or guardrail
logic of its own - that would duplicate PCOIS2-46/48/49/50/52, which
already live in data-pipeline/ and generation/. It only does what an API
layer should: load those pieces once at startup, expose them over HTTP,
validate the request/response shape, and fail predictably when a
dependency (Postgres, Ollama) isn't there.

Run:
    uvicorn main:app --reload --port 8000
    python main.py                       # same thing, no --reload

Config via environment variables (all optional; same names the rest of
the project already uses):
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD   - see data-pipeline
    OLLAMA_HOST, OLLAMA_MODEL, OLLAMA_TIMEOUT        - see generation
    FRONTEND_ORIGINS   comma-separated list of allowed CORS origins
                        (default: the Vite dev server,
                        http://localhost:5173,http://127.0.0.1:5173)
    PORT                default 8000 - matches policyApi.js's API_BASE default
"""
import logging
import os
import sys
import threading
import time
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# generation/ and data-pipeline/ are plain script folders, not an
# installed package, so put both on the path - same pattern
# generation/test_generation_live.py already uses to reach
# hybrid_search.py and build_vector_db.py.
_HERE = os.path.dirname(os.path.abspath(__file__))
_ROOT = os.path.dirname(_HERE)
for _dir in ("generation", "data-pipeline"):
    _path = os.path.join(_ROOT, _dir)
    if _path not in sys.path:
        sys.path.insert(0, _path)

# Only light imports (requests + stdlib) happen at module level.
# HybridRetriever pulls in sentence-transformers and psycopg2, so that
# import is deferred to app startup below. That keeps `import main`
# cheap enough for test_api.py to exercise routing and schema
# conformance with a stub retriever/client and no Postgres or Ollama
# running - the same thing generation/test_generation.py already does
# for respond.py directly.
from ollama_client import OllamaClient                      # noqa: E402
from respond import answer_question                         # noqa: E402

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
logger = logging.getLogger("policydb.api")

FRONTEND_ORIGINS = [
    o.strip() for o in os.environ.get(
        "FRONTEND_ORIGINS",
        "http://localhost:5173,http://127.0.0.1:5173",
    ).split(",") if o.strip()
]

# Guards access to the shared Postgres connection and models inside
# HybridRetriever. FastAPI runs sync path functions in a thread pool, so
# concurrent requests would otherwise share one psycopg2 connection
# across threads, which psycopg2 doesn't support. Serialising here is
# the right tradeoff for a small class-project API; a connection pool
# would be the next step if this ever needed real concurrency.
_lock = threading.Lock()

_state = {"retriever": None, "client": None, "startup_error": None}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Deferred import - see note above.
    from build_vector_db import connect
    from hybrid_search import HybridRetriever

    logger.info("Starting up: connecting to Postgres and loading retrieval models ...")
    try:
        conn = connect()
        _state["retriever"] = HybridRetriever(conn)
    except Exception as e:                                  # noqa: BLE001
        # Retrieval couldn't come up (e.g. Postgres isn't running, or
        # policy_chunks is empty). Don't crash the process for that -
        # start the server anyway so /health reports the problem clearly
        # instead of the frontend just getting connection-refused.
        logger.error("Retriever failed to initialise: %s", e)
        _state["startup_error"] = str(e)

    _state["client"] = OllamaClient()
    if not _state["client"].is_available():
        logger.warning(
            "Ollama not reachable at %s - /ask will return status=error for "
            "any question that clears the relevance threshold, until "
            "`ollama serve` is running.",
            _state["client"].host,
        )

    logger.info("Startup complete.")
    yield
    logger.info("Shutting down.")


app = FastAPI(
    title="PolicyDB Chatbot API",
    description="Retrieval + grounded generation + citations + guardrails, "
                 "wrapped behind one endpoint (PCOIS2-56).",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=FRONTEND_ORIGINS,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --- Schema ---------------------------------------------------------------
# Mirrors PCOIS2-31 / respond.py's response dict exactly, so FastAPI
# validates every outgoing response against the agreed contract - and the
# frontend team gets this documented for free at /docs.

class AskRequest(BaseModel):
    question: str


class Citation(BaseModel):
    policy_title: str
    section: str
    source_url: str


class AskResponse(BaseModel):
    status: str
    question: str
    answer: str
    citations: list[Citation]
    confidence: str
    escalation_required: bool
    escalation_message: str


class HealthResponse(BaseModel):
    status: str
    database: bool
    ollama: bool


# --- Dependencies -----------------------------------------------------
# Overridden in test_api.py with a stub retriever/client, so routing and
# schema conformance can be tested without a live Postgres or Ollama -
# the same approach generation/test_generation.py takes for respond.py.

def get_retriever():
    if _state["retriever"] is None:
        raise HTTPException(
            status_code=503,
            detail=f"Policy search is unavailable: {_state['startup_error'] or 'not initialised'}",
        )
    return _state["retriever"]


def get_client():
    return _state["client"]


# --- Routes ----------------------------------------------------------------

@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest, retriever=Depends(get_retriever), client=Depends(get_client)):
    start = time.monotonic()
    with _lock:
        result = answer_question(payload.question, retriever, client)
    elapsed_ms = (time.monotonic() - start) * 1000

    # Minimal per-request line so the endpoint isn't silent in dev - the
    # fuller structured query log is PCOIS2-57's ticket, not duplicated here.
    logger.info(
        "status=%s confidence=%s citations=%d elapsed_ms=%.0f",
        result["status"], result["confidence"], len(result["citations"]), elapsed_ms,
    )
    return result


@app.get("/health", response_model=HealthResponse)
def health(client=Depends(get_client)):
    db_ok = _state["retriever"] is not None
    ollama_ok = bool(client and client.is_available())
    return HealthResponse(
        status="ok" if (db_ok and ollama_ok) else "degraded",
        database=db_ok,
        ollama=ollama_ok,
    )


@app.get("/")
def root():
    return {
        "service": "PolicyDB Chatbot API",
        "ask": 'POST /ask {"question": "..."}',
        "health": "GET /health",
        "docs": "/docs",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
