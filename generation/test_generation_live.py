"""
PCOIS2-51: Test generation against sample questions, log hallucination cases.

The same question set as PCOIS2-47, but checking the ANSWER the model
produces rather than just what retrieval returned. Runs the full live path -
real Postgres, real hybrid retrieval, real Ollama - because
test_generation.py covers the routing logic with stubs and deliberately
never calls the model. Whether Qwen3 actually obeys prompts.py is the
open question this file exists to answer.

WHAT COUNTS AS A HALLUCINATION HERE
A claim in the answer that is not supported by the excerpts the model was
given. Three automated signals, cheapest and most reliable first:

  1. Unsupported numbers  - a figure in the answer that appears in no
                            excerpt. Highest-value signal by far: policy
                            answers turn on day counts, percentages and
                            dates, and an invented number is both the most
                            damaging error and the easiest to detect.
  2. Unsupported terms    - content words absent from every excerpt.
                            Noisier (the model legitimately paraphrases),
                            so treated as review candidates, not verdicts.
  3. Rule violations      - citations written into the answer text
                            (prompts.py Rule 4), leaked <think> reasoning,
                            malformed schema, over-long answers.

None of these prove hallucination on their own, which is why the report
puts the answer and its excerpts side by side with a blank verdict column.
The automation narrows where a human needs to look; it does not replace
the human.

Usage (from generation/, venv active, PG env vars set, Ollama running):
    python test_generation_live.py
    python test_generation_live.py --limit 3      # quick smoke run

Writes: ../docs/generation-test-results-sprint3.md
"""
import argparse
import json
import os
import re
import sys
import time
from datetime import date

# data-pipeline holds build_vector_db and hybrid_search; generation imports
# them as top-level modules, so put that directory on the path.
_HERE = os.path.dirname(os.path.abspath(__file__))
_PIPELINE = os.path.join(os.path.dirname(_HERE), "data-pipeline")
if _PIPELINE not in sys.path:
    sys.path.insert(0, _PIPELINE)

from build_vector_db import connect                      # noqa: E402
from hybrid_search import HybridRetriever                # noqa: E402
from ollama_client import OllamaClient                   # noqa: E402
from respond import answer_question, RERANK_THRESHOLD    # noqa: E402

OUTPUT_PATH = os.path.join("..", "docs", "generation-test-results-sprint3.md")

SCHEMA_KEYS = {
    "status", "question", "answer", "citations", "confidence",
    "escalation_required", "escalation_message",
}

# (question, expected_status, why)
# expected_status None means any answering status is acceptable - the answer
# still gets reviewed, but there is no automated pass/fail on routing.
TEST_QUESTIONS = [
    ("What academic dress do graduands wear at a graduation ceremony?", None, ""),
    ("Who is entitled to wear a doctoral gown?", None, ""),
    ("Can I keep my academic gown after the ceremony?", None, ""),
    ("What happens if a student fails the same subject more than once?", None, ""),
    ("Can I appeal an academic progression decision?", None, ""),
    ("What are the stages of academic progression review?", None, ""),
    ("How do I apply for promotion to Associate Professor?", None, ""),
    ("Who sits on the academic promotions committee?", None, ""),
    ("What is the basis for academic promotion?", None, ""),
    ("What qualifications must academic staff hold to teach a subject?", None, ""),
    (
        "Does a lecturer need a qualification higher than the course they teach?",
        None,
        "Scored 0.111 in PCOIS2-47 - expected to be filtered before generation",
    ),
    ("What are the English language requirements for admission?", None, ""),
    (
        "Can I get credit for prior study when I apply?",
        None,
        "Corpus gap: credit rules live in the Credit Standard, not ingested. "
        "Scored 0.028, so should not reach the model",
    ),
    (
        "How are applications for admission assessed?",
        "low_confidence",
        "ACCEPTANCE TEST for PCOIS2-49. Retrieval hands this Academic "
        "Promotions text at 0.795, well above threshold. A fluent answer "
        "about promotion committees is a hallucination and a fail",
    ),
    (
        "How do I book a car parking permit on campus?",
        "out_of_scope",
        "Out-of-scope control - scored 0.000, must not reach the model",
    ),
    (
        "What food is available at the campus cafe today?",
        "out_of_scope",
        "Out-of-scope control - scored 0.000, must not reach the model",
    ),
]

STOPWORDS = {
    "a", "about", "after", "all", "also", "an", "and", "any", "applies",
    "apply", "are", "as", "at", "be", "been", "before", "being", "both",
    "but", "by", "can", "cannot", "check", "confirm", "do", "does", "each",
    "for", "from", "further", "given", "has", "have", "how", "however", "if",
    "in", "including", "into", "is", "it", "its", "may", "more", "most",
    "must", "no", "not", "of", "on", "one", "only", "or", "other", "out",
    "provide", "provided", "relevant", "required", "requires", "same",
    "shall", "should", "so", "some", "such", "than", "that", "the", "their",
    "then", "there", "these", "this", "those", "through", "to", "under",
    "up", "use", "used", "was", "were", "what", "when", "where", "which",
    "who", "will", "with", "within", "would", "you", "your",
    # Domain words that appear constantly and carry no hallucination signal
    "policy", "policies", "university", "student", "students", "staff",
    "course", "courses", "subject", "subjects",
}

WORD_RE = re.compile(r"[a-z]+")
NUMBER_RE = re.compile(r"\b\d+(?:\.\d+)?\b")

# Rule 4 says the model must not write citations. These patterns catch it.
CITATION_LEAK_RE = re.compile(
    r"\b(?:Section|Part|Clause|Schedule)\s+[\dA-Z]\b|"
    r"\b[A-Z][A-Za-z ]{3,40}\s+Policy\b|"
    r"\baccording to the (?:excerpt|policy|document)",
)
THINK_LEAK_RE = re.compile(r"</?think>", re.I)


def normalise(text: str) -> str:
    return " ".join(text.lower().split())


def content_words(text: str) -> set[str]:
    return {
        w for w in WORD_RE.findall(text.lower())
        if len(w) > 3 and w not in STOPWORDS
    }


def unsupported_numbers(answer: str, excerpts: str) -> list[str]:
    """Figures in the answer that appear nowhere in the excerpts."""
    return sorted({
        n for n in NUMBER_RE.findall(answer)
        if n not in NUMBER_RE.findall(excerpts)
    })


def unsupported_terms(answer: str, excerpts: str, limit: int = 8) -> list[str]:
    """Content words in the answer absent from the excerpts.

    Paraphrasing produces false positives here by design - a model saying
    "wear" where the policy says "worn" is not hallucinating. Crude stemming
    (comparing the first five characters) removes the most common of these
    without pretending to do real morphology.
    """
    excerpt_words = content_words(excerpts)
    excerpt_stems = {w[:5] for w in excerpt_words}

    missing = [
        w for w in sorted(content_words(answer))
        if w not in excerpt_words and w[:5] not in excerpt_stems
    ]
    return missing[:limit]


def check_response(result: dict, expected_status, chunks_text: str) -> dict:
    """Run every automated check over one response."""
    issues = []
    answer = result.get("answer", "") or ""

    # Schema conformance - the frontend renders this shape directly
    missing_keys = SCHEMA_KEYS - set(result)
    if missing_keys:
        issues.append(f"SCHEMA: missing keys {sorted(missing_keys)}")

    # Routing
    status = result.get("status")
    routing_ok = expected_status is None or status == expected_status
    if not routing_ok:
        issues.append(f"ROUTING: expected {expected_status}, got {status}")

    # Only inspect answer text when the model actually generated one
    generated = status == "success"

    nums, terms = [], []
    if generated:
        nums = unsupported_numbers(answer, chunks_text)
        if nums:
            issues.append(f"UNSUPPORTED NUMBERS: {', '.join(nums)}")

        terms = unsupported_terms(answer, chunks_text)
        if terms:
            issues.append(f"UNSUPPORTED TERMS: {', '.join(terms)}")

        leak = CITATION_LEAK_RE.search(answer)
        if leak:
            issues.append(f"RULE 4 (no citations in answer): \"{leak.group(0)}\"")

        if THINK_LEAK_RE.search(answer):
            issues.append("REASONING LEAK: <think> tags in answer")

        sentences = [s for s in re.split(r"[.!?]+", answer) if s.strip()]
        if len(sentences) > 5:
            issues.append(f"RULE 5 (2-4 sentences): {len(sentences)} sentences")

        if not result.get("citations"):
            issues.append("CITATIONS: success response has none")

    # An out_of_scope response must carry no citations
    if status == "out_of_scope" and result.get("citations"):
        issues.append("CITATIONS: out_of_scope response should have none")

    return {
        "routing_ok": routing_ok,
        "generated": generated,
        "issues": issues,
        "unsupported_numbers": nums,
        "unsupported_terms": terms,
    }


def run(limit=None):
    client = OllamaClient()
    if not client.is_available():
        sys.exit(
            "Ollama is not reachable. Start it in another terminal:\n"
            "    ollama serve\n"
            "then confirm the model is pulled:\n"
            "    ollama pull qwen3"
        )

    conn = connect()
    retriever = HybridRetriever(conn)

    questions = TEST_QUESTIONS[:limit] if limit else TEST_QUESTIONS
    results = []

    for i, (question, expected, note) in enumerate(questions, 1):
        print(f"\n[{i}/{len(questions)}] {question}")

        # Retrieve separately so the excerpts the model saw can be recorded.
        # answer_question retrieves again internally; the duplicate call is
        # cheap and keeps this harness from reaching into its internals.
        try:
            chunks = retriever.search(question)
        except Exception as e:                              # noqa: BLE001
            print(f"    retrieval failed: {e}")
            chunks = []

        chunks_text = " ".join(c.get("text", "") for c in chunks)
        top = float(chunks[0].get("rerank_score") or 0.0) if chunks else 0.0

        started = time.time()
        result = answer_question(question, retriever, client)
        elapsed = time.time() - started

        check = check_response(result, expected, chunks_text)

        results.append({
            "question": question,
            "expected": expected,
            "note": note,
            "result": result,
            "check": check,
            "top_score": top,
            "elapsed": elapsed,
            "chunks": [
                {
                    "policy_title": c.get("policy_title"),
                    "section": c.get("section"),
                    "score": float(c.get("rerank_score") or 0.0),
                    "text": " ".join((c.get("text") or "").split()),
                }
                for c in chunks
            ],
        })

        status = result.get("status")
        mark = "ok " if not check["issues"] else "FLAG"
        print(f"    [{mark}] status={status} score={top:.3f} {elapsed:.1f}s")
        for issue in check["issues"]:
            print(f"           - {issue}")

    conn.close()
    return results


def write_report(results):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    total = len(results)
    generated = sum(1 for r in results if r["check"]["generated"])
    flagged = [r for r in results if r["check"]["issues"]]
    routing_fails = [r for r in results if not r["check"]["routing_ok"]]
    hallucination_candidates = [
        r for r in results
        if r["check"]["unsupported_numbers"] or r["check"]["unsupported_terms"]
    ]

    lines = [
        "# Generation Test Results - Sprint 3 (PCOIS2-51)",
        "",
        f"**Date run:** {date.today().isoformat()}  ",
        f"**Model:** Ollama / {os.environ.get('OLLAMA_MODEL', 'qwen3')}  ",
        f"**Retrieval:** hybrid (BM25 + vector + cross-encoder rerank), "
        f"threshold {RERANK_THRESHOLD}  ",
        f"**Questions:** {total}  |  **Reached the model:** {generated}  |  "
        f"**Flagged for review:** {len(flagged)}",
        "",
        "Live end-to-end run: real Postgres, real retrieval, real model.",
        "`test_generation.py` covers routing logic with stubs and never calls",
        "the model, so this is the first check of whether the model actually",
        "obeys the prompt rules.",
        "",
        "A flag is a place to look, not a verdict. Automation narrows the",
        "search; the Verdict column below is filled in by a human comparing",
        "each answer against the excerpts it was given.",
        "",
        "## Summary",
        "",
        f"- Routing failures: **{len(routing_fails)}**",
        f"- Responses with unsupported numbers or terms: "
        f"**{len(hallucination_candidates)}**",
        f"- Clean: **{total - len(flagged)}/{total}**",
        "",
        "## Results",
        "",
        "| # | Question | Score | Status | Reached model | Flags | Verdict |",
        "|---|---|---|---|---|---|---|",
    ]

    for i, r in enumerate(results, 1):
        flags = "; ".join(r["check"]["issues"]) if r["check"]["issues"] else "-"
        lines.append(
            f"| {i} | {r['question']} | {r['top_score']:.3f} | "
            f"{r['result'].get('status')} | "
            f"{'yes' if r['check']['generated'] else 'no'} | {flags} |  |"
        )

    lines += [
        "",
        "## Answers and their excerpts",
        "",
        "Each answer below is followed by the excerpts the model was given.",
        "Read one against the other and record a verdict in the table above:",
        "**grounded** (every claim traceable to an excerpt), **hallucinated**",
        "(a claim that is not), or **wrong refusal** (the excerpts did answer",
        "the question but the model declined).",
        "",
    ]

    for i, r in enumerate(results, 1):
        res = r["result"]
        lines += [
            f"### {i}. {r['question']}",
            "",
            f"- **Status:** {res.get('status')}  ",
            f"- **Confidence:** {res.get('confidence')}  ",
            f"- **Top rerank score:** {r['top_score']:.3f}  ",
            f"- **Response time:** {r['elapsed']:.1f}s",
        ]
        if r["note"]:
            lines.append(f"- **Note:** {r['note']}")
        lines.append("")

        lines += ["**Answer:**", "", f"> {res.get('answer', '')}", ""]

        if res.get("citations"):
            lines.append("**Citations:**")
            lines.append("")
            for c in res["citations"]:
                lines.append(
                    f"- {c.get('policy_title')} - {c.get('section')} "
                    f"({c.get('source_url')})"
                )
            lines.append("")

        if r["check"]["issues"]:
            lines.append("**Flags:**")
            lines.append("")
            for issue in r["check"]["issues"]:
                lines.append(f"- {issue}")
            lines.append("")

        if r["check"]["generated"] and r["chunks"]:
            lines.append("<details><summary>Excerpts the model was given</summary>")
            lines.append("")
            for j, c in enumerate(r["chunks"], 1):
                text = c["text"]
                if len(text) > 900:
                    text = text[:900] + " ..."
                lines += [
                    f"**Excerpt {j}** - {c['policy_title']} / {c['section']} "
                    f"(score {c['score']:.3f})",
                    "",
                    f"> {text}",
                    "",
                ]
            lines += ["</details>", ""]

        lines.append("---")
        lines.append("")

    lines += [
        "## Observations",
        "",
        "_Fill in after reviewing the answers above._",
        "",
        "- Did the acceptance test (question 14, admissions vs promotions) pass?",
        "  A fluent answer about promotion committees is a prompt failure.",
        "- Did the out-of-scope controls stop before reaching the model?",
        "- Any confirmed hallucinations, and what kind - invented figures,",
        "  added procedural advice, or general knowledge not in the excerpts?",
        "- Did the model over-refuse on questions the excerpts did answer?",
        "  Over-refusal is the safer failure, but it still costs usefulness.",
        "- Response times: acceptable for an interactive chatbot?",
        "",
    ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nWrote {OUTPUT_PATH}")
    print(f"  {total} questions, {generated} reached the model, "
          f"{len(flagged)} flagged")


def main():
    parser = argparse.ArgumentParser(
        description="Live generation tests with hallucination logging"
    )
    parser.add_argument("--limit", type=int,
                        help="only run the first N questions (quick smoke run)")
    args = parser.parse_args()

    write_report(run(args.limit))


if __name__ == "__main__":
    main()