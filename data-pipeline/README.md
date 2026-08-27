# PolicyDB Chatbot — Data Pipeline (PCOIS2-26, 27, 28)

Three scripts that take the project from "we know the five policies" to
"they're cleaned, chunked, embedded, and searchable" — implementing the
Hybrid RAG + Guardrails architecture recommended in PCOIS2-8.

```
scrape_policies.py   -->  clean_and_chunk.py   -->   build_vector_db.py
(PCOIS2-26)                (PCOIS2-27)                 (PCOIS2-28)
raw HTML/PDF                cleaned, chunked            embedded chunks
+ manifest.json              JSONL                       in Postgres/pgvector
```

## 1. Setup

```bash
pip install -r requirements.txt
```

You'll also need a Postgres database with the `pgvector` extension available:

- **Local via Docker (fastest):**
  ```bash
  docker run --name policydb-pg -e POSTGRES_PASSWORD=postgres -p 5432:5432 -d ankane/pgvector
  ```
- **Supabase free tier** — pgvector is available out of the box; use the
  connection details from your project's Settings > Database.
- **Local apt install** (Ubuntu/Debian): `apt-get install postgresql postgresql-16-pgvector`,
  then `psql -c "CREATE EXTENSION vector;"` on your target database.

Set connection details via environment variables (defaults shown):
```bash
export PGHOST=localhost
export PGPORT=5432
export PGDATABASE=policydb
export PGUSER=postgres
export PGPASSWORD=postgres
```

## 2. Run the pipeline

```bash
python scrape_policies.py     # PCOIS2-26 -> data/raw/*.html, data/manifest.json
python clean_and_chunk.py     # PCOIS2-27 -> data/cleaned/*.jsonl
python build_vector_db.py     # PCOIS2-28 -> policy_chunks table, embedded
```

## 3. Quick test query

```python
from sentence_transformers import SentenceTransformer
from build_vector_db import connect, search

model = SentenceTransformer("all-MiniLM-L6-v2")
conn = connect()
for title, section, url, text, sim in search(conn, model, "What are the rules on academic dress for graduation?"):
    print(f"{sim:.3f}  {title} — {section}")
```

## What's been verified vs. what still needs a live run

I built and tested this without access to the real La Trobe site or the
internet-hosted embedding model (my sandbox's network is limited to
package registries), so here's exactly what's been proven and what
hasn't:

| Component | Status |
|---|---|
| `clean_and_chunk.py` cleaning + chunking logic | **Tested** — ran against a fixture matching the documented page structure; correctly fixed clause spacing, stripped nav/footer/"Top of Page", converted the table to decision→role text, and extracted version/status/review date exactly matching Alina's real values for policy 208 |
| `scrape_policies.py` parsing/metadata-extraction logic | **Tested** — same fixture, confirms the extraction functions work; the actual live HTTP fetch against `policies.latrobe.edu.au` has **not** been run — do that first and diff a saved page against the fixture's structure |
| `build_vector_db.py` schema, insert, similarity search | **Tested end-to-end** against a real local Postgres+pgvector instance, using placeholder random vectors (couldn't reach huggingface.co to download the real model in my sandbox) — the SQL and pipeline plumbing is confirmed correct; the actual embedding model has **not** been run |

**First things to do when you run this for real:**
1. Run `scrape_policies.py` and open `data/raw/208.html` — compare its actual
   structure (class names, whether "Top of Page" is a link or plain text,
   whether there's a PDF link and what it looks like) against
   `strip_boilerplate()` and `find_pdf_link()`. Adjust selectors if needed.
2. Run `clean_and_chunk.py` and spot-check a couple of `data/cleaned/*.jsonl`
   entries against the original pages.
3. Run `build_vector_db.py` — first run downloads the ~90MB embedding model,
   so make sure that machine has internet access.


## Hybrid retrieval (Sprint 3) - Aaron

`hybrid_search.py` — retrieval used by everything downstream. Three stages:

1. **BM25 keyword search** (`BM25Index`) — literal term matching, catches
   things like "section 4.2" or a policy name that vector search misses.
2. **Reciprocal Rank Fusion** (`reciprocal_rank_fusion`) — merges the BM25
   and vector rankings. Uses rank position only, never raw scores, because
   a BM25 score of 8.4 and a cosine similarity of 0.51 aren't comparable.
3. **Cross-encoder reranking** (`rerank`) — re-scores the merged candidates
   by reading question and chunk together. This is the score to threshold
   on for refusal/escalation, not cosine similarity.

Tuning constants are at the top of the file: `VECTOR_CANDIDATES`,
`BM25_CANDIDATES`, `RRF_K`, `RERANK_CANDIDATES`, `FINAL_TOP_K`.

### Using it from other code

```python
from build_vector_db import connect
from hybrid_search import HybridRetriever

conn = connect()
retriever = HybridRetriever(conn)          # loads models once, reuse it
hits = retriever.search("your question")   # -> list of dicts, best first
```

Each hit has: `chunk_id`, `policy_title`, `section`, `source_url`, `text`,
`rerank_score` (0–1), `found_by`.

**For generation (Sprint 3):** treat `rerank_score < 0.5` on the top hit as
"no relevant policy found" and return the escalation response from the
agreed schema rather than generating an answer.

### CLI

```bash
python hybrid_search.py "What are the rules on academic dress?"
python hybrid_search.py --vector-only "..."   # Sprint 2 behaviour, for comparison
python hybrid_search.py --no-rerank "..."     # fusion only
```

### Tests

```bash
python run_retrieval_tests.py
```

Runs 16 questions through both vector-only and hybrid, writes
`docs/retrieval-test-results-sprint3.md`. Run this after any retrieval
change — it doubles as a regression check.

### Vector index

Uses HNSW rather than ivfflat. ivfflat trains its clusters from existing
rows, but the schema is created before any data is loaded, which produced
an index that returned zero rows for some queries (found in PCOIS2-47).
HNSW has no training step and builds incrementally as rows are inserted.
