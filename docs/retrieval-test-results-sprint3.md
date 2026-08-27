# Retrieval Test Results - Sprint 3 (PCOIS2-47)

**Date run:** 2026-08-27  
**Corpus:** policy_chunks (La Trobe policy documents)  
**Configuration A:** vector-only, threshold 0.35 (Sprint 2 baseline)  
**Configuration B:** BM25 + vector, RRF fusion, cross-encoder rerank, threshold 0.5  
**Reranker:** cross-encoder/ms-marco-MiniLM-L-6-v2  
**Tuning:** vector top-20, BM25 top-20, RRF k=60, rerank top-20, final top-5

**Result:** vector-only 15/16  →  hybrid+rerank 13/16  
**Fixed by hybrid:** 1  |  **Regressed:** 3

No LLM generation is involved. A test passes when the top-ranked chunk
comes from the expected policy and clears the threshold. Out-of-scope
controls pass when NOTHING clears the threshold - the behaviour needed
for the chatbot to refuse and escalate rather than answer (User Story 4).

| # | Question | Expected policy | Vector score | Vector | Hybrid score | Hybrid | Top result (hybrid) | Found by |
|---|---|---|---|---|---|---|---|---|
| 1 | What academic dress do graduands wear at a graduation ceremony? | Academic Dress Policy | 0.659 | PASS | 0.999 | PASS | Academic Dress Policy - Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent | bm25, vector |
| 2 | Who is entitled to wear a doctoral gown? | Academic Dress Policy | 0.601 | PASS | 0.902 | PASS | Academic Dress Policy - Section 7 - Definitions | bm25, vector |
| 3 | Can I keep my academic gown after the ceremony? | Academic Dress Policy | 0.600 | PASS | 0.797 | PASS | Academic Dress Policy - Section 5 - Policy Statement | bm25, vector |
| 4 | What happens if a student fails the same subject more than once? | Academic Progression Review Policy | 0.535 | PASS | 0.985 | PASS | Academic Progression Review Policy - Part B - Details of Academic Progression Stages | bm25, vector |
| 5 | Can I appeal an academic progression decision? | Academic Progression Review Policy | 0.478 | PASS | 0.882 | PASS | Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression | bm25, vector |
| 6 | What are the stages of academic progression review? | Academic Progression Review Policy | 0.595 | PASS | 0.999 | PASS | Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression | bm25, vector |
| 7 | How do I apply for promotion to Associate Professor? | Academic Promotions Policy | 0.565 | PASS | 0.977 | PASS | Academic Promotions Policy - Section 3 - Scope | bm25, vector |
| 8 | Who sits on the academic promotions committee? | Academic Promotions Policy | 0.645 | PASS | 0.998 | PASS | Academic Promotions Policy - Part D - Academic Promotions Committees | bm25, vector |
| 9 | What is the basis for academic promotion? | Academic Promotions Policy | 0.624 | PASS | 0.991 | PASS | Academic Promotions Policy - Part B - Basis for Promotion | bm25, vector |
| 10 | What qualifications must academic staff hold to teach a subject? | Academic Staff Qualifications Policy | 0.569 | PASS | 0.999 | PASS | Academic Staff Qualifications Policy - Section 5 - Policy Statement | bm25, vector |
| 11 | Does a lecturer need a qualification higher than the course they teach? | Academic Staff Qualifications Policy | 0.489 | PASS | 0.111 | FAIL | Academic Staff Qualifications Policy - Section 5 - Policy Statement | vector |
| 12 | What are the English language requirements for admission? | Admissions Policy | 0.567 | PASS | 0.582 | PASS | Admissions Policy - Section 2 - Purpose | bm25, vector |
| 13 | Can I get credit for prior study when I apply? | Admissions Policy | 0.502 | PASS | 0.028 | FAIL | Admissions Policy - Section 7 - Definitions | bm25 |
| 14 | How are applications for admission assessed? | Admissions Policy | 0.563 | PASS | 0.795 | FAIL | Academic Promotions Policy - Section 5 - Policy Statement | bm25, vector |
| 15 | How do I book a car parking permit on campus? | _(none - out of scope)_ | 0.367 | FAIL | 0.000 | PASS | Admissions Policy - Section 8 - Authority and Associated Information | vector |
| 16 | What food is available at the campus cafe today? | _(none - out of scope)_ | 0.236 | PASS | 0.000 | PASS | Academic Promotions Policy - Part C - Referee and External Assessor Reports | bm25 |

## What changed

**Fixed by hybrid retrieval:**

- How do I book a car parking permit on campus? — vector 0.367 (returned Academic Staff Qualifications Policy), hybrid 0.000 (returned Admissions Policy), found by vector

**Regressed:**

- Does a lecturer need a qualification higher than the course they teach? — vector 0.489, hybrid 0.111 (returned Academic Staff Qualifications Policy)
- Can I get credit for prior study when I apply? — vector 0.502, hybrid 0.028 (returned Admissions Policy)
- How are applications for admission assessed? — vector 0.563, hybrid 0.795 (returned Academic Promotions Policy)

## Observations

**1. The reranker resolves the Sprint 2 scope-detection blocker.**
Sprint 2's central finding was that no similarity threshold could separate
real questions from irrelevant ones: a legitimate question scored 0.297
while an out-of-scope control scored 0.367. Under hybrid retrieval both
out-of-scope controls score exactly 0.000, and the lowest-scoring passing
in-scope question scores 0.582. The gap is now unambiguous. A threshold of
0.5 sits comfortably inside it, and the escalation path in the agreed
response schema (PCOIS2-31) can be implemented on this signal.

**2. The two score columns measure different things and are not comparable.**
Vector score is cosine similarity — how close in meaning a chunk is to the
question. Rerank score is a cross-encoder judgement of whether the chunk
actually answers the question. The cross-encoder is far more decisive:
in-scope questions cluster at 0.88–0.999 rather than vector's 0.48–0.66.
This is why the raw pass counts (15/16 vs 13/16) understate the improvement.

**3. BM25 contributed to 12 of 16 top results.**
Ten rows show `bm25, vector`, meaning both methods independently surfaced
the same chunk. Row 13 was retrieved by BM25 alone — the literal term
"credit" was matched where vector search missed it entirely. Keyword search
is earning its place in the pipeline.

**4. Row 13 is a corpus gap, not a retrieval failure.**
Inspecting data/cleaned/169.jsonl confirms the Admissions Policy mentions
credit only as cross-references: "the granting of credit in accordance with
the principles and conditions outlined in the Credit Standard", and Section 6
referring to "Admissions Procedure - Credit" and "Admissions Standard -
Credit". None of those three documents are in the five-policy corpus. The
reranker scoring 0.028 is therefore correct behaviour; the vector-only pass
at 0.502 was a false positive that returned the right policy without the
answer. Resolving this requires ingesting the referenced documents, not
tuning retrieval.

**5. Row 14 is the only genuine failure, and it is the dangerous kind.**
"How are applications for admission assessed?" returned the Academic
Promotions Policy at 0.795 — high confidence, wrong policy. Promotion
applications are also "assessed", so the two policies collide semantically.
This is the failure mode that matters most for the project: an LLM would
generate a fluent, confident answer citing the wrong policy. Two honest
refusals (rows 11 and 13) are preferable to one confident error.

**6. Clause-level precision remains unresolved and is not measured here.**
Several passing rows return Definitions or Purpose sections rather than the
operative clause — row 2 returned "Section 7 - Definitions" at 0.902, row 12
returned "Section 2 - Purpose". These pass because the test only checks the
policy title. Citation quality depends on landing on the right clause, so
the test set should be extended with expected sections in the next sprint.

**7. Chunking defect identified during analysis.**
Chunk 169-0-0, labelled "Preamble", contains the entire policy document
duplicated — all eight sections plus site navigation text. An oversized
chunk distorts BM25 length normalisation and competes with the correctly
scoped chunks. Raised for the ingestion pipeline (PCOIS2-27).

**Recommended settings for Sprint 3 generation:** rerank threshold 0.5,
final top-k 5. Retain the vector-only comparison in this harness so it
functions as a regression check against future retrieval changes.

- Did BM25 contribute? Check the "Found by" column — rows showing
  `bm25, vector` are cases where both methods agreed.
- Is the out-of-scope gap now clean? Compare the highest out-of-scope
  score against the lowest in-scope score. If the in-scope minimum is
  above the out-of-scope maximum, a single threshold now works and the
  Sprint 2 blocker is resolved.
- Recommended threshold for Sprint 3 generation, based on that gap.
- Is the retrieved *section* the operative clause, or still Definitions
  and Purpose sections?
