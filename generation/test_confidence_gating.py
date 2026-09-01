from respond import top_score, confidence_label, RERANK_THRESHOLD, HIGH_CONFIDENCE

# Unambiguous cases: the score-threshold prediction and PCOIS2-51's
# table AGREE on the outcome for these. Safe to assert.
UNAMBIGUOUS_CASES = [
    ("Academic dress at graduation", 0.999, True),
    ("Fails same subject twice", 0.985, True),
    ("Appeal academic progression decision", 0.882, True),
    ("Stages of academic progression review", 0.999, True),
    ("Promotions committee membership", 0.998, True),
    ("Staff qualifications to teach", 0.999, True),
    ("Applications for admission assessed (wrong-policy case)", 0.795, True),
    ("Lecturer qualification higher than course", 0.111, False),
    ("Credit for prior study (corpus gap)", 0.028, False),
    ("Car parking permit (out of scope)", 0.000, False),
    ("Campus cafe food (out of scope)", 0.000, False),
]

# Disputed cases: current code logic and PCOIS2-51's historical table
# disagree. NOT asserted as pass/fail - reported separately so the
# disagreement is visible, not hidden by the test suite.
DISPUTED_CASES = [
    ("Who is entitled to wear a doctoral gown?", 0.902, False),
    ("Can I keep my academic gown after the ceremony?", 0.797, False),
    ("How do I apply for promotion to Associate Professor?", 0.977, False),
    ("What is the basis for academic promotion?", 0.991, False),
    ("English language requirements for admission", 0.582, False),
]


def make_chunks(score):
    if score == 0.0:
        return []
    return [{"rerank_score": score, "policy_title": "Test Policy", "section": "Test Section"}]


def run_retrieval_gate_tests():
    print("=== Unambiguous cases (code and PCOIS2-51 table agree) ===")
    passed = 0
    for question, score, expected_reaches_generation in UNAMBIGUOUS_CASES:
        chunks = make_chunks(score)
        reaches_generation = top_score(chunks) >= RERANK_THRESHOLD
        ok = reaches_generation == expected_reaches_generation
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] score={score:<6} reaches_model={reaches_generation!s:5} {question}")
    print(f"\n{passed}/{len(UNAMBIGUOUS_CASES)} passed\n")

    print("=== DISPUTED cases (code says reach model, table says it didn't) ===")
    print("Not scored pass/fail - reported so the disagreement stays visible:\n")
    for question, score, table_says in DISPUTED_CASES:
        chunks = make_chunks(score)
        code_says = top_score(chunks) >= RERANK_THRESHOLD
        print(f"  score={score:<6} code says reach_model={code_says!s:5}  table says reach_model={table_says!s:5}  {question}")
    print()
    return passed, len(UNAMBIGUOUS_CASES)


def run_confidence_label_tests():
    # Source: PCOIS2-51's actual "Top rerank score" + "Confidence" columns
    # for the 7 questions that reached the model.
    cases = [
        (0.999, "high"),
        (0.985, "high"),
        (0.882, "high"),
        (0.998, "high"),
        (0.795, "medium"),  # PCOIS2-51 logged this as "medium" - matches confidence_label()
    ]
    print("=== confidence_label() vs real PCOIS2-51 confidence values ===")
    passed = 0
    for score, expected in cases:
        actual = confidence_label(score)
        ok = actual == expected
        passed += ok
        print(f"[{'PASS' if ok else 'FAIL'}] score={score} -> {actual} (expected {expected})")
    print(f"\n{passed}/{len(cases)} match real PCOIS2-51 confidence labels\n")
    return passed, len(cases)


if __name__ == "__main__":
    p1, t1 = run_retrieval_gate_tests()
    p2, t2 = run_confidence_label_tests()
    print(f"TOTAL: {p1 + p2}/{t1 + t2} passed")
    print(
        "\nNote on 'How are applications for admission assessed?' (0.795, reaches "
        "generation): this is PCOIS2-47's known wrong-policy-collision case. The "
        "score-based gate correctly lets it through to generation - it's SUPPOSED "
        "to. The real defence there is prompts.py Rule 1/2, which PCOIS2-51 "
        "confirmed worked (the model answered from the correct excerpt anyway). "
        "This test file deliberately does not try to make the score gate catch "
        "that case - see the deck's Bug & Issue slide for why that's the right call."
    )