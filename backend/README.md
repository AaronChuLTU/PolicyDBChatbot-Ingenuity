# Backend API (Sprint 3) — Minh

**PCOIS2-56**: wraps the pipeline already built this sprint — `data-pipeline/hybrid_search.py`
(retrieval) and `generation/respond.py` (grounded generation, citations, guardrails) —
behind one HTTP endpoint, so Sprint 4's frontend can call a real service
instead of `frontend/src/api/policyApi.js`'s mock.

```
question --> HybridRetriever --> respond.answer_question() --> JSON
             (data-pipeline)      (generation)                 (this app)
```

No retrieval, generation or guardrail logic lives here — `main.py` only
loads those pieces once, exposes them over HTTP, validates the request
and response shape, and reports clearly when a dependency is down.

## Endpoints

| Method | Path      | Body                   | Returns |
|---|---|---|---|
| POST | `/ask`    | `{"question": "..."}`  | The PCOIS2-31 schema object (`status`, `question`, `answer`, `citations[]`, `confidence`, `escalation_required`, `escalation_message`) |
| GET  | `/health` | —                      | `{"status", "database", "ollama"}` |
| GET  | `/docs`   | —                      | Interactive Swagger UI, auto-generated from the schema (useful for PCOIS2-58) |

This is exactly the shape `policyApi.js` already expects — `API_BASE`
defaults to `http://localhost:8000`, and it already calls `POST /ask`
with `{question}`. Sprint 4 just needs to delete the `MOCK` block in
`askPolicyQuestion` and uncomment the real `fetch` underneath it.

## Setup

Same environment as `data-pipeline/` and `generation/`, plus this
folder's two extra packages:

```bash
pip install -r ../data-pipeline/requirements.txt
pip install -r requirements.txt
ollama serve                 # separate terminal
ollama pull qwen3
```

Postgres needs `policy_chunks` populated — see `data-pipeline/README.md`.

Config (all optional — same variable names the rest of the project
already uses):

```bash
export PGHOST=localhost PGPORT=5432 PGDATABASE=policydb PGUSER=postgres PGPASSWORD=postgres
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=qwen3
export FRONTEND_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
export PORT=8000
```

## Run

```bash
python main.py
# or: uvicorn main:app --reload --port 8000
```

Startup loads the embedding model, BM25 index and cross-encoder
reranker once (a few seconds — the same load `hybrid_search.py`'s CLI
does per run), then the server is ready.

Try it:

```bash
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What academic dress do graduands wear at a graduation ceremony?"}'

curl http://localhost:8000/health
```

## Tests

```bash
pip install fastapi uvicorn httpx     # httpx only needed for TestClient
python test_api.py
```

Runs without Postgres or Ollama — a stub retriever and stub LLM client
are swapped in via FastAPI's dependency overrides, the same idea
`generation/test_generation.py` uses for `respond.py` directly. These
tests check the HTTP layer only (status codes, schema conformance,
error handling); what `answer_question()` decides for a given score is
already covered by `test_generation.py`. Confirmed this runs clean with
neither `psycopg2` nor `sentence-transformers` installed — 12/12 pass.

## Design notes

- **Retrieval and generation models load once, at startup**, not per
  request — `HybridRetriever.__init__` loading the embedding model,
  BM25 index and reranker is the expensive part, and doing that per
  request would make every question slow.
- **`/ask` is serialised behind a lock.** FastAPI runs sync endpoints
  in a thread pool, and `HybridRetriever` holds a single psycopg2
  connection that shouldn't be queried from two threads at once. For a
  small class-project API this trade-off is fine; a connection pool
  would be the next step if this ever needed real concurrency.
- **If Postgres is unreachable at startup**, the server still starts
  (so `/health` can report the problem) and `/ask` returns `503` with
  the reason, rather than the process refusing to boot or the frontend
  seeing an opaque connection-refused error.
- **If Ollama isn't running yet**, startup only logs a warning —
  retrieval still works, and `answer_question()` already turns a
  failed `generate()` call into a graceful `status: "error"` response
  rather than a stack trace.
- **Response shape is enforced with a Pydantic `response_model`**, so
  if `respond.py` ever drifted from the agreed PCOIS2-31 schema, this
  layer would catch it rather than silently sending the frontend
  something it doesn't expect.

## Known gap carried over from Sprint 3

`respond.py`'s `ESCALATION_OUT_OF_SCOPE` / `ESCALATION_LOW_CONFIDENCE`
text is still the PCOIS2-31 placeholder wording, not Alina's finalised
PCOIS2-53 messages (the ones with the `policy@latrobe.edu.au` / ASK La
Trobe contact routing). `generation/README.md` already flags this as a
drop-in swap for whoever picks it up — this ticket doesn't touch it,
since the endpoint just returns whatever `answer_question()` gives it.
