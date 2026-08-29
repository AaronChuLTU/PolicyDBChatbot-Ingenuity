"""
PCOIS2-50: Response formatting with policy citations.

Turns a user question into the agreed response object from PCOIS2-31
(Alina's mock response schema) - the exact shape the React frontend
already renders.

    {
      status:              success | low_confidence | out_of_scope | error,
      question:            str,
      answer:              str,
      citations:           [ {policy_title, section, source_url} ],
      confidence:          high | medium | low,
      escalation_required: bool,
      escalation_message:  str
    }

WHERE CITATIONS COME FROM
Citations are built from the metadata already stored on each row of
policy_chunks (policy_title, section, source_url) and carried through
retrieval by hybrid_search. They are never produced by the language
model, which does not even see them - build_user_prompt passes excerpt
text only. A citation is therefore a fact about which database record was
retrieved, not a claim the model has made, so it cannot be hallucinated.

THRESHOLDS
RERANK_THRESHOLD = 0.5, from the PCOIS2-47 test run: out-of-scope controls
scored 0.000 and the lowest passing in-scope question scored 0.582, so 0.5
sits inside a clean gap.

The same value filters the citation list. Retrieval passes the top 5
chunks to the model, but some score very low (0.028 in one test row);
citing those would attach an authoritative-looking source to text that had
little to do with the answer.
"""
import sys

from prompts import SYSTEM_PROMPT, build_user_prompt, is_refusal

RERANK_THRESHOLD = 0.50      # below this: nothing relevant was found
CITATION_THRESHOLD = 0.50    # below this: chunk is not cited
HIGH_CONFIDENCE = 0.85       # in-scope questions clustered at 0.88-0.999

ESCALATION_OUT_OF_SCOPE = (
    "Please rephrase your question or visit the official La Trobe University "
    "website for further assistance."
)
ESCALATION_LOW_CONFIDENCE = (
    "Please check the complete policy document or contact the appropriate "
    "University area for confirmation."
)
NO_ANSWER_TEXT = (
    "I could not find relevant information in the available La Trobe "
    "University policy documents."
)
PARTIAL_ANSWER_TEXT = (
    "The available policy information does not provide enough detail to "
    "answer this question confidently."
)


def top_score(chunks: list[dict]) -> float:
    """Rerank score of the best hit, or 0.0 if there is nothing."""
    if not chunks:
        return 0.0
    score = chunks[0].get("rerank_score")
    return 0.0 if score is None else float(score)


def confidence_label(score: float) -> str:
    """Map a rerank score onto the schema's high/medium/low field."""
    if score >= HIGH_CONFIDENCE:
        return "high"
    if score >= RERANK_THRESHOLD:
        return "medium"
    return "low"


def build_citations(chunks: list[dict], threshold: float = CITATION_THRESHOLD) -> list[dict]:
    """Citation list from chunk metadata, best first.

    Deduplicated on (policy_title, section) because a long section can be
    split across several chunks - the reader wants one reference to the
    section, not the same line three times.
    """
    citations = []
    seen = set()

    for chunk in chunks:
        score = chunk.get("rerank_score")
        if score is not None and float(score) < threshold:
            continue

        key = (chunk.get("policy_title"), chunk.get("section"))
        if key in seen:
            continue
        seen.add(key)

        citations.append({
            "policy_title": chunk.get("policy_title", ""),
            "section": chunk.get("section", ""),
            "source_url": chunk.get("source_url", ""),
        })

    return citations


def _response(status, question, answer, citations, confidence,
              escalation_required, escalation_message=""):
    return {
        "status": status,
        "question": question,
        "answer": answer,
        "citations": citations,
        "confidence": confidence,
        "escalation_required": escalation_required,
        "escalation_message": escalation_message,
    }


def out_of_scope_response(question: str) -> dict:
    """Nothing cleared the threshold - no citations, per the schema's
    display rule that out-of-scope answers show no unrelated sources."""
    return _response(
        "out_of_scope", question, NO_ANSWER_TEXT, [], "low",
        True, ESCALATION_OUT_OF_SCOPE,
    )


def low_confidence_response(question: str, chunks: list[dict]) -> dict:
    """Retrieval found plausible policy text but the model would not answer
    from it. Citations are kept so the user can check the source
    themselves - that is the schema's low-confidence example."""
    return _response(
        "low_confidence", question, PARTIAL_ANSWER_TEXT,
        build_citations(chunks), "low", True, ESCALATION_LOW_CONFIDENCE,
    )


def error_response(question: str, message: str) -> dict:
    return _response("error", question, message, [], "low", True,
                     "Please try again shortly or contact the relevant "
                     "University area directly.")


def answer_question(question: str, retriever, client) -> dict:
    """Full path: retrieve -> generate -> format.

    retriever: a hybrid_search.HybridRetriever
    client:    an ollama_client.OllamaClient
    """
    question = (question or "").strip()
    if not question:
        return error_response("", "No question was provided.")

    # 1. Retrieve (PCOIS2-46)
    try:
        chunks = retriever.search(question)
    except Exception as e:                                # noqa: BLE001
        return error_response(question, f"Policy search is unavailable: {e}")

    # 2. Guard: did anything relevant come back?
    score = top_score(chunks)
    if score < RERANK_THRESHOLD:
        return out_of_scope_response(question)

    # 3. Generate, grounded in the retrieved text only (PCOIS2-48/49)
    try:
        raw = client.generate(
            system=SYSTEM_PROMPT,
            user=build_user_prompt(question, chunks),
        )
    except Exception as e:                                # noqa: BLE001
        return error_response(question, f"The policy assistant is unavailable: {e}")

    # 4. The model refused - it judged the excerpts insufficient or
    #    off-topic. This is the guard against a confidently retrieved but
    #    wrong policy, which the score threshold alone cannot catch.
    if is_refusal(raw):
        return low_confidence_response(question, chunks)

    answer = raw.strip()
    if not answer:
        return low_confidence_response(question, chunks)

    # 5. Success: attach citations from chunk metadata (PCOIS2-50)
    confidence = confidence_label(score)
    return _response(
        "success", question, answer, build_citations(chunks), confidence,
        False, "",
    )


def main():
    """CLI: python respond.py "your question here" """
    if len(sys.argv) < 2:
        print('Usage: python respond.py "your question"', file=sys.stderr)
        sys.exit(1)

    import json

    from build_vector_db import connect
    from hybrid_search import HybridRetriever
    from ollama_client import OllamaClient

    client = OllamaClient()
    if not client.is_available():
        print("Ollama is not reachable. Start it with:  ollama serve", file=sys.stderr)
        sys.exit(1)

    conn = connect()
    retriever = HybridRetriever(conn)

    result = answer_question(" ".join(sys.argv[1:]), retriever, client)
    print(json.dumps(result, indent=2, ensure_ascii=False))

    conn.close()


if __name__ == "__main__":
    main()
