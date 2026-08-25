"""
PCOIS2-47: Document retrieval test results against sample questions.

Runs a fixed question set through BOTH retrieval configurations and writes a
side-by-side comparison:

    A. vector-only    - Sprint 2 behaviour (build_vector_db.search)
    B. hybrid+rerank  - Sprint 3 behaviour (hybrid_search.HybridRetriever)

Running both matters more than running the new one. "Hybrid retrieval scores
0.8" means nothing on its own; "hybrid fixed four questions vector-only got
wrong, and regressed none" is evidence the Sprint 3 work was worth doing.

No LLM is involved. This measures whether the correct policy and section
reach the top of the results - the prerequisite for grounded generation.

Usage (from data-pipeline/, venv active, PG* env vars set):
    python run_retrieval_tests.py

Writes: ../docs/retrieval-test-results-sprint3.md
"""
import os
from datetime import date

from build_vector_db import connect
from hybrid_search import (
    HybridRetriever, FINAL_TOP_K, VECTOR_CANDIDATES, BM25_CANDIDATES,
    RRF_K, RERANK_CANDIDATES, RERANKER_MODEL,
)

OUTPUT_PATH = os.path.join("..", "docs", "retrieval-test-results-sprint3.md")

# Score below which a result is treated as "nothing relevant found" - the
# point where the chatbot should refuse and escalate (User Story 4).
# Vector and rerank scores are different scales, so they get separate values.
VECTOR_THRESHOLD = 0.35     # carried over from Sprint 2
RERANK_THRESHOLD = 0.50     # cross-encoder sigmoid output; tune from results

# (question, expected_policy, expected_section_hint)
# expected_policy of None marks a deliberately out-of-scope control: the
# correct behaviour is for NOTHING to clear the threshold.
TEST_QUESTIONS = [
    ("What academic dress do graduands wear at a graduation ceremony?",
     "Academic Dress Policy", None),
    ("Who is entitled to wear a doctoral gown?",
     "Academic Dress Policy", None),
    ("Can I keep my academic gown after the ceremony?",
     "Academic Dress Policy", None),
    ("What happens if a student fails the same subject more than once?",
     "Academic Progression Review Policy", None),
    ("Can I appeal an academic progression decision?",
     "Academic Progression Review Policy", None),
    ("What are the stages of academic progression review?",
     "Academic Progression Review Policy", None),
    ("How do I apply for promotion to Associate Professor?",
     "Academic Promotions Policy", None),
    ("Who sits on the academic promotions committee?",
     "Academic Promotions Policy", None),
    ("What is the basis for academic promotion?",
     "Academic Promotions Policy", None),
    ("What qualifications must academic staff hold to teach a subject?",
     "Academic Staff Qualifications Policy", None),
    ("Does a lecturer need a qualification higher than the course they teach?",
     "Academic Staff Qualifications Policy", None),
    ("What are the English language requirements for admission?",
     "Admissions Policy", None),
    ("Can I get credit for prior study when I apply?",
     "Admissions Policy", None),
    ("How are applications for admission assessed?",
     "Admissions Policy", None),
    # Out-of-scope controls
    ("How do I book a car parking permit on campus?", None, None),
    ("What food is available at the campus cafe today?", None, None),
]


def evaluate(hits, expected, score_key, threshold):
    """Return (passed, top_title, top_section, top_score)."""
    if not hits:
        return (expected is None, "NO RESULTS", "-", 0.0)

    top = hits[0]
    score = top.get(score_key)
    score = 0.0 if score is None else float(score)

    if expected is None:
        # Out-of-scope control: correct behaviour is nothing clearing the bar.
        passed = score < threshold
    else:
        passed = (top["policy_title"] == expected) and (score >= threshold)

    return (passed, top["policy_title"], top.get("section", "-"), score)


def run():
    conn = connect()
    retriever = HybridRetriever(conn, load_reranker=True)

    results = []
    for question, expected, _hint in TEST_QUESTIONS:
        vec_hits = retriever.vector_only(question, FINAL_TOP_K)
        hyb_hits = retriever.search(question, FINAL_TOP_K, use_reranker=True)

        vec = evaluate(vec_hits, expected, "similarity", VECTOR_THRESHOLD)
        hyb = evaluate(hyb_hits, expected, "rerank_score", RERANK_THRESHOLD)

        found_by = ""
        if hyb_hits:
            found_by = ", ".join(sorted({m for m, _, _ in hyb_hits[0].get("found_by", [])}))

        results.append({
            "question": question,
            "expected": expected,
            "vec": vec,
            "hyb": hyb,
            "found_by": found_by,
        })

        v_mark = "PASS" if vec[0] else "FAIL"
        h_mark = "PASS" if hyb[0] else "FAIL"
        print(f"[vec {v_mark} {vec[3]:.3f}] [hyb {h_mark} {hyb[3]:.3f}]  {question}")

    conn.close()
    return results


def write_report(results):
    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

    vec_passed = sum(1 for r in results if r["vec"][0])
    hyb_passed = sum(1 for r in results if r["hyb"][0])
    total = len(results)

    fixed = [r for r in results if r["hyb"][0] and not r["vec"][0]]
    regressed = [r for r in results if r["vec"][0] and not r["hyb"][0]]

    lines = [
        "# Retrieval Test Results - Sprint 3 (PCOIS2-47)",
        "",
        f"**Date run:** {date.today().isoformat()}  ",
        f"**Corpus:** policy_chunks (La Trobe policy documents)  ",
        f"**Configuration A:** vector-only, threshold {VECTOR_THRESHOLD} (Sprint 2 baseline)  ",
        f"**Configuration B:** BM25 + vector, RRF fusion, cross-encoder rerank, "
        f"threshold {RERANK_THRESHOLD}  ",
        f"**Reranker:** {RERANKER_MODEL}  ",
        f"**Tuning:** vector top-{VECTOR_CANDIDATES}, BM25 top-{BM25_CANDIDATES}, "
        f"RRF k={RRF_K}, rerank top-{RERANK_CANDIDATES}, final top-{FINAL_TOP_K}",
        "",
        f"**Result:** vector-only {vec_passed}/{total}  \u2192  hybrid+rerank {hyb_passed}/{total}  ",
        f"**Fixed by hybrid:** {len(fixed)}  |  **Regressed:** {len(regressed)}",
        "",
        "No LLM generation is involved. A test passes when the top-ranked chunk",
        "comes from the expected policy and clears the threshold. Out-of-scope",
        "controls pass when NOTHING clears the threshold - the behaviour needed",
        "for the chatbot to refuse and escalate rather than answer (User Story 4).",
        "",
        "| # | Question | Expected policy | Vector score | Vector | Hybrid score | Hybrid | Top result (hybrid) | Found by |",
        "|---|---|---|---|---|---|---|---|---|",
    ]

    for i, r in enumerate(results, 1):
        exp = r["expected"] or "_(none - out of scope)_"
        v_pass, _v_title, _v_sec, v_score = r["vec"]
        h_pass, h_title, h_sec, h_score = r["hyb"]
        lines.append(
            f"| {i} | {r['question']} | {exp} | {v_score:.3f} | "
            f"{'PASS' if v_pass else 'FAIL'} | {h_score:.3f} | "
            f"{'PASS' if h_pass else 'FAIL'} | {h_title} - {h_sec} | {r['found_by']} |"
        )

    lines += ["", "## What changed", ""]

    if fixed:
        lines.append("**Fixed by hybrid retrieval:**")
        lines.append("")
        for r in fixed:
            lines.append(
                f"- {r['question']} \u2014 vector {r['vec'][3]:.3f} (returned "
                f"{r['vec'][1]}), hybrid {r['hyb'][3]:.3f} (returned {r['hyb'][1]}), "
                f"found by {r['found_by']}"
            )
        lines.append("")
    else:
        lines += ["No questions were fixed by hybrid retrieval.", ""]

    if regressed:
        lines.append("**Regressed:**")
        lines.append("")
        for r in regressed:
            lines.append(
                f"- {r['question']} \u2014 vector {r['vec'][3]:.3f}, "
                f"hybrid {r['hyb'][3]:.3f} (returned {r['hyb'][1]})"
            )
        lines.append("")
    else:
        lines += ["No questions regressed.", ""]

    lines += [
        "## Observations",
        "",
        "_Fill in after reviewing the table._",
        "",
        "- Did BM25 contribute? Check the \"Found by\" column \u2014 rows showing",
        "  `bm25, vector` are cases where both methods agreed.",
        "- Is the out-of-scope gap now clean? Compare the highest out-of-scope",
        "  score against the lowest in-scope score. If the in-scope minimum is",
        "  above the out-of-scope maximum, a single threshold now works and the",
        "  Sprint 2 blocker is resolved.",
        "- Recommended threshold for Sprint 3 generation, based on that gap.",
        "- Is the retrieved *section* the operative clause, or still Definitions",
        "  and Purpose sections?",
        "",
    ]

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"\nWrote {OUTPUT_PATH}")
    print(f"  vector-only  {vec_passed}/{total}")
    print(f"  hybrid+rerank {hyb_passed}/{total}  (fixed {len(fixed)}, regressed {len(regressed)})")


if __name__ == "__main__":
    write_report(run())
