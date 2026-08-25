"""
PCOIS2-40 / PCOIS2-46: Hybrid retrieval - BM25 keyword search alongside
vector search, fused into one ranked list and re-scored by a reranker.

Why this exists
---------------
build_vector_db.py's search() does vector similarity only. It finds chunks
with similar *meaning*, but misses exact matches - someone typing "section
4.2", a specific policy name, or a term like "credit transfer" that appears
verbatim in the text. Sprint 2 retrieval testing (PCOIS2-29) showed this
directly: a legitimate question about credit for prior study scored 0.297,
lower than a deliberately out-of-scope question at 0.367.

This module adds three stages on top of vector search:

  1. BM25 keyword search      - catches literal term matches
  2. Reciprocal Rank Fusion   - merges both ranked lists into one
  3. Cross-encoder reranking  - re-scores the merged candidates for
                                actual question-answer relevance

Stage 3 matters most for the Sprint 2 findings. Cosine similarity between a
question and a chunk is a weak relevance signal - it is why "Definitions"
sections kept winning. A cross-encoder reads the question and the chunk
together and scores whether the chunk actually answers it, which is far more
discriminative and gives a usable basis for the refusal behaviour required
by User Story 4.

Usage:
    python hybrid_search.py "What are the rules on academic dress?"
    python hybrid_search.py --vector-only "..."     # for comparison

Requires the same PG* environment variables as build_vector_db.py.
"""
import argparse
import math
import os
import re
import sys

from sentence_transformers import CrossEncoder, SentenceTransformer

from build_vector_db import connect, EMBED_MODEL_NAME

# --- Tuning knobs (PCOIS2-46) -------------------------------------------
# Retrieve generously from each method, then let fusion and reranking cut it
# down. Too few candidates and the right chunk never reaches the reranker;
# too many and reranking gets slow and noisy.
VECTOR_CANDIDATES = 20      # top-k pulled from vector search
BM25_CANDIDATES = 20        # top-k pulled from BM25
RRF_K = 60                  # RRF damping constant; 60 is the standard default
RERANK_CANDIDATES = 20      # how many fused hits get re-scored
FINAL_TOP_K = 5             # how many chunks are passed downstream to the LLM

RERANKER_MODEL = "cross-encoder/ms-marco-MiniLM-L-6-v2"

# Minimal stopword list - just enough to stop BM25 matching on filler.
STOPWORDS = {
    "a", "an", "and", "are", "as", "at", "be", "by", "can", "do", "does",
    "for", "from", "how", "i", "if", "in", "is", "it", "me", "my", "of",
    "on", "or", "that", "the", "there", "this", "to", "was", "what", "when",
    "where", "which", "who", "why", "will", "with", "you", "your",
}


def tokenize(text: str) -> list[str]:
    """Lowercase word tokens, stopwords removed.

    Deliberately keeps digits and dotted references intact so queries like
    "section 4.2" still match - that is one of the cases vector search misses.
    """
    tokens = re.findall(r"[a-z0-9]+(?:\.[a-z0-9]+)*", text.lower())
    return [t for t in tokens if t not in STOPWORDS]


# --- Corpus loading ------------------------------------------------------

def load_corpus(conn) -> list[dict]:
    """Pull every chunk out of policy_chunks.

    BM25 needs the whole corpus in memory to compute term statistics. At the
    current size (under 100 chunks) that is trivial. If the corpus grows past
    a few thousand chunks, replace this with Postgres full-text search
    (ts_rank_cd over a tsvector column) so ranking happens in the database.
    """
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT chunk_id, policy_title, section, source_url, text
            FROM policy_chunks
            ORDER BY chunk_id;
            """
        )
        rows = cur.fetchall()

    return [
        {
            "chunk_id": r[0],
            "policy_title": r[1],
            "section": r[2],
            "source_url": r[3],
            "text": r[4],
        }
        for r in rows
    ]


# --- Stage 1a: BM25 keyword search (PCOIS2-40) ---------------------------

class BM25Index:
    """Okapi BM25 over the chunk texts.

    Implemented directly rather than pulling in rank_bm25 - it is about
    thirty lines, avoids another dependency, and makes the scoring visible
    for the report.

    k1 controls term-frequency saturation (how much repeated terms help);
    b controls length normalisation (how much long chunks are penalised).
    1.5 / 0.75 are the standard defaults and were not tuned further - the
    reranker does the fine-grained relevance work.
    """

    def __init__(self, corpus: list[dict], k1: float = 1.5, b: float = 0.75):
        self.corpus = corpus
        self.k1 = k1
        self.b = b

        self.docs = [tokenize(c["text"]) for c in corpus]
        self.doc_lens = [len(d) for d in self.docs]
        self.avg_len = sum(self.doc_lens) / len(self.docs) if self.docs else 0.0
        self.n_docs = len(self.docs)

        # document frequency per term
        df: dict[str, int] = {}
        for doc in self.docs:
            for term in set(doc):
                df[term] = df.get(term, 0) + 1

        # smoothed IDF (the +1 keeps common terms from going negative)
        self.idf = {
            term: math.log(1 + (self.n_docs - freq + 0.5) / (freq + 0.5))
            for term, freq in df.items()
        }

        # per-document term frequencies, precomputed
        self.term_freqs = []
        for doc in self.docs:
            tf: dict[str, int] = {}
            for term in doc:
                tf[term] = tf.get(term, 0) + 1
            self.term_freqs.append(tf)

    def score(self, query_tokens: list[str], doc_idx: int) -> float:
        tf = self.term_freqs[doc_idx]
        doc_len = self.doc_lens[doc_idx]
        score = 0.0
        for term in query_tokens:
            if term not in tf:
                continue
            freq = tf[term]
            numerator = freq * (self.k1 + 1)
            denominator = freq + self.k1 * (
                1 - self.b + self.b * doc_len / self.avg_len
            )
            score += self.idf.get(term, 0.0) * numerator / denominator
        return score

    def search(self, query: str, k: int = BM25_CANDIDATES) -> list[tuple[dict, float]]:
        query_tokens = tokenize(query)
        scored = [
            (self.corpus[i], self.score(query_tokens, i))
            for i in range(self.n_docs)
        ]
        scored = [(c, s) for c, s in scored if s > 0]
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored[:k]


# --- Stage 1b: vector search --------------------------------------------

def vector_search(conn, model, query: str, k: int = VECTOR_CANDIDATES):
    """Cosine-similarity search, same as build_vector_db.search() but
    returning dicts so both retrieval methods share one shape."""
    q_emb = model.encode([query], normalize_embeddings=True)[0].tolist()
    with conn.cursor() as cur:
        cur.execute(
            """
            SELECT chunk_id, policy_title, section, source_url, text,
                   1 - (embedding <=> %s::vector) AS similarity
            FROM policy_chunks
            ORDER BY embedding <=> %s::vector
            LIMIT %s;
            """,
            (q_emb, q_emb, k),
        )
        rows = cur.fetchall()

    return [
        (
            {
                "chunk_id": r[0],
                "policy_title": r[1],
                "section": r[2],
                "source_url": r[3],
                "text": r[4],
            },
            float(r[5]),
        )
        for r in rows
    ]


# --- Stage 2: Reciprocal Rank Fusion (PCOIS2-46) -------------------------

def reciprocal_rank_fusion(ranked_lists, rrf_k: int = RRF_K) -> list[dict]:
    """Merge several ranked lists into one.

    RRF scores each result by 1/(rrf_k + rank) and sums across lists. The
    key property: it uses *rank position only*, never the raw scores. That
    matters here because a BM25 score of 8.4 and a cosine similarity of
    0.51 are not comparable quantities - trying to normalise and weight them
    means inventing a conversion factor with nothing to justify it.

    A chunk found by both methods accumulates score from both, so agreement
    between keyword and semantic search naturally floats to the top.
    """
    fused: dict[str, dict] = {}

    for ranked in ranked_lists:
        for rank, (chunk, raw_score) in enumerate(ranked, start=1):
            cid = chunk["chunk_id"]
            if cid not in fused:
                fused[cid] = {**chunk, "rrf_score": 0.0, "found_by": []}
            fused[cid]["rrf_score"] += 1.0 / (rrf_k + rank)
            fused[cid]["found_by"].append((ranked.method, rank, raw_score))

    results = list(fused.values())
    results.sort(key=lambda c: c["rrf_score"], reverse=True)
    return results


class RankedList(list):
    """A ranked result list tagged with which method produced it."""

    def __init__(self, items, method: str):
        super().__init__(items)
        self.method = method


# --- Stage 3: cross-encoder reranking (PCOIS2-46) ------------------------

def rerank(reranker: CrossEncoder, query: str, candidates: list[dict],
           top_k: int = FINAL_TOP_K) -> list[dict]:
    """Re-score candidates by reading question and chunk together.

    The bi-encoder used for the vector index embeds the question and the
    chunk separately, so it can only measure whether they occupy similar
    regions of meaning-space. A cross-encoder runs both through the model
    at once and scores whether this chunk answers this question - a much
    stronger signal, and the one worth thresholding on for refusal.

    Output is a raw logit, so it is squashed to 0-1 with a sigmoid to make
    the numbers readable in the test report.
    """
    if not candidates:
        return []

    pairs = [(query, c["text"]) for c in candidates]
    scores = reranker.predict(pairs)

    for c, s in zip(candidates, scores):
        c["rerank_score"] = 1 / (1 + math.exp(-float(s)))

    ranked = sorted(candidates, key=lambda c: c["rerank_score"], reverse=True)
    return ranked[:top_k]


# --- Orchestration -------------------------------------------------------

class HybridRetriever:
    """Holds the models and the BM25 index so they load once, not per query."""

    def __init__(self, conn, load_reranker: bool = True):
        self.conn = conn
        print(f"Loading embedding model ({EMBED_MODEL_NAME}) ...", file=sys.stderr)
        self.embedder = SentenceTransformer(EMBED_MODEL_NAME)

        print("Building BM25 index from policy_chunks ...", file=sys.stderr)
        self.corpus = load_corpus(conn)
        self.bm25 = BM25Index(self.corpus)
        print(f"  {len(self.corpus)} chunks indexed", file=sys.stderr)

        self.reranker = None
        if load_reranker:
            print(f"Loading reranker ({RERANKER_MODEL}) ...", file=sys.stderr)
            self.reranker = CrossEncoder(RERANKER_MODEL)

    def search(self, query: str, top_k: int = FINAL_TOP_K,
               use_reranker: bool = True) -> list[dict]:
        vec_hits = RankedList(
            vector_search(self.conn, self.embedder, query, VECTOR_CANDIDATES),
            method="vector",
        )
        kw_hits = RankedList(
            self.bm25.search(query, BM25_CANDIDATES),
            method="bm25",
        )

        fused = reciprocal_rank_fusion([vec_hits, kw_hits])

        if use_reranker and self.reranker is not None:
            return rerank(self.reranker, query, fused[:RERANK_CANDIDATES], top_k)

        for c in fused:
            c["rerank_score"] = None
        return fused[:top_k]

    def vector_only(self, query: str, top_k: int = FINAL_TOP_K) -> list[dict]:
        """Sprint 2 behaviour, kept for the before/after comparison."""
        hits = vector_search(self.conn, self.embedder, query, top_k)
        return [{**chunk, "similarity": score} for chunk, score in hits]


def _format_hit(i: int, hit: dict) -> str:
    score = hit.get("rerank_score")
    score_str = f"{score:.3f}" if score is not None else f"rrf={hit['rrf_score']:.4f}"
    found = ", ".join(m for m, _, _ in hit.get("found_by", [])) or "-"
    snippet = " ".join(hit["text"].split())[:160]
    return (
        f"{i}. [{score_str}] {hit['policy_title']} - {hit['section']}\n"
        f"     found by: {found}\n"
        f"     {snippet}..."
    )


def main():
    parser = argparse.ArgumentParser(description="Hybrid policy retrieval")
    parser.add_argument("query", help="the question to search for")
    parser.add_argument("--vector-only", action="store_true",
                        help="skip BM25 and reranking (Sprint 2 behaviour)")
    parser.add_argument("--no-rerank", action="store_true",
                        help="hybrid retrieval + fusion, but no reranking")
    parser.add_argument("-k", type=int, default=FINAL_TOP_K,
                        help=f"how many results to show (default {FINAL_TOP_K})")
    args = parser.parse_args()

    conn = connect()
    retriever = HybridRetriever(conn, load_reranker=not (args.vector_only or args.no_rerank))

    if args.vector_only:
        hits = retriever.vector_only(args.query, args.k)
        print(f"\nVECTOR ONLY - {args.query}\n")
        for i, h in enumerate(hits, 1):
            snippet = " ".join(h["text"].split())[:160]
            print(f"{i}. [{h['similarity']:.3f}] {h['policy_title']} - {h['section']}")
            print(f"     {snippet}...")
    else:
        hits = retriever.search(args.query, args.k, use_reranker=not args.no_rerank)
        label = "HYBRID + RERANK" if not args.no_rerank else "HYBRID (no rerank)"
        print(f"\n{label} - {args.query}\n")
        for i, h in enumerate(hits, 1):
            print(_format_hit(i, h))

    conn.close()


if __name__ == "__main__":
    main()
