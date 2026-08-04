"""
PCOIS2-28: Set up vector database & generate embeddings.

Implements the vector store choice from PCOIS2-8 (Recommended RAG
Approach): pgvector on Postgres, chosen over Pinecone/Chroma for this
project because it lets vector search and the audit-log / relational
data (PCOIS2 later sprints) live in one database with no vendor lock-in.

Embedding model: sentence-transformers/all-MiniLM-L6-v2 (384-dim, free,
runs locally, no API key). This is a placeholder-free default so the
pipeline works before PCOIS2-32 (select LLM provider) is decided; if the
team picks a provider whose embeddings you'd rather standardise on
(e.g. OpenAI text-embedding-3-small), swap embed_texts() and the VECTOR
column width accordingly - everything else in this script stays the same.

Reads:  data/cleaned/all_chunks.jsonl   (from PCOIS2-27)
Writes: rows into the `policy_chunks` table (schema below)

Connection config via environment variables (with local defaults):
    PGHOST, PGPORT, PGDATABASE, PGUSER, PGPASSWORD
"""
import json
import os

import psycopg2
from psycopg2.extras import execute_values
from sentence_transformers import SentenceTransformer

EMBED_MODEL_NAME = "all-MiniLM-L6-v2"
EMBED_DIM = 384
CHUNKS_PATH = "data/cleaned/all_chunks.jsonl"

DB_CONFIG = dict(
    host=os.environ.get("PGHOST", "localhost"),
    port=os.environ.get("PGPORT", "5432"),
    dbname=os.environ.get("PGDATABASE", "policydb"),
    user=os.environ.get("PGUSER", "postgres"),
    password=os.environ.get("PGPASSWORD", "postgres"),
)

CREATE_TABLE_SQL = f"""
CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS policy_chunks (
    chunk_id      TEXT PRIMARY KEY,
    policy_id     INT NOT NULL,
    policy_title  TEXT NOT NULL,
    category      TEXT,
    section       TEXT,
    version       TEXT,
    status        TEXT,
    review_date   TEXT,
    source_url    TEXT NOT NULL,
    text          TEXT NOT NULL,
    embedding     VECTOR({EMBED_DIM})
);

-- ANN index for fast similarity search once the table has real volume.
CREATE INDEX IF NOT EXISTS policy_chunks_embedding_idx
    ON policy_chunks USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 100);
"""

UPSERT_SQL = """
INSERT INTO policy_chunks
    (chunk_id, policy_id, policy_title, category, section, version, status,
     review_date, source_url, text, embedding)
VALUES %s
ON CONFLICT (chunk_id) DO UPDATE SET
    text = EXCLUDED.text,
    embedding = EXCLUDED.embedding,
    version = EXCLUDED.version,
    status = EXCLUDED.status,
    review_date = EXCLUDED.review_date;
"""


def load_chunks(path=CHUNKS_PATH):
    chunks = []
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                chunks.append(json.loads(line))
    return chunks


def embed_texts(model: SentenceTransformer, texts: list[str]):
    return model.encode(texts, show_progress_bar=len(texts) > 20, normalize_embeddings=True)


def connect():
    return psycopg2.connect(**DB_CONFIG)


def setup_schema(conn):
    with conn.cursor() as cur:
        cur.execute(CREATE_TABLE_SQL)
    conn.commit()


def load_into_db(conn, chunks, embeddings):
    rows = [
        (
            c["chunk_id"], c["policy_id"], c["policy_title"], c.get("category"),
            c["section"], c.get("version"), c.get("status"), c.get("review_date"),
            c["source_url"], c["text"], emb.tolist(),
        )
        for c, emb in zip(chunks, embeddings)
    ]
    with conn.cursor() as cur:
        execute_values(cur, UPSERT_SQL, rows)
    conn.commit()


def search(conn, model: SentenceTransformer, query: str, k: int = 5):
    """Vector-similarity search (cosine distance via pgvector's <=> operator).
    Hybrid keyword+vector retrieval and reranking are PCOIS2-29's job -
    this is the vector half of that pipeline stage."""
    q_emb = model.encode([query], normalize_embeddings=True)[0].tolist()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT policy_title, section, source_url, text,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM policy_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (q_emb, q_emb, k),
        )
        return cur.fetchall()


def main():
    print(f"Loading embedding model ({EMBED_MODEL_NAME}) ...")
    model = SentenceTransformer(EMBED_MODEL_NAME)

    print(f"Loading cleaned chunks from {CHUNKS_PATH} ...")
    chunks = load_chunks()
    print(f"  {len(chunks)} chunks loaded")

    print("Connecting to Postgres and ensuring schema/pgvector extension ...")
    conn = connect()
    setup_schema(conn)

    print("Generating embeddings ...")
    texts = [c["text"] for c in chunks]
    embeddings = embed_texts(model, texts)

    print("Writing to policy_chunks ...")
    load_into_db(conn, chunks, embeddings)
    print(f"Done. {len(chunks)} chunks embedded and stored.")

    conn.close()


if __name__ == "__main__":
    main()
