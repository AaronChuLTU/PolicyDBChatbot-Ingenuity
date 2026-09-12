# Retrieval Test Results - Sprint 3 (PCOIS2-47)

**Date run:** 2026-09-12  
**Corpus:** policy_chunks (La Trobe policy documents)  
**Configuration A:** vector-only, threshold 0.35 (Sprint 2 baseline)  
**Configuration B:** BM25 + vector, RRF fusion, cross-encoder rerank, threshold 0.5  
**Reranker:** cross-encoder/ms-marco-MiniLM-L-6-v2  
**Tuning:** vector top-20, BM25 top-20, RRF k=60, rerank top-20, final top-5

**Result:** vector-only 12/17  →  hybrid+rerank 15/17  
**Fixed by hybrid:** 3  |  **Regressed:** 0

No LLM generation is involved. A test passes when the top-ranked chunk
comes from the expected policy and clears the threshold. Out-of-scope
controls pass when NOTHING clears the threshold - the behaviour needed
for the chatbot to refuse and escalate rather than answer (User Story 4).

| # | Question | Expected policy | Vector score | Vector | Hybrid score | Hybrid | Top result (hybrid) | Found by |
|---|---|---|---|---|---|---|---|---|
| 1 | What academic dress do graduands wear at a graduation ceremony? | Academic Dress Policy | 0.659 | PASS | 0.999 | PASS | Academic Dress Policy - Part D - Graduands and Graduates of Aboriginal or Torres Strait Islander Descent | bm25, vector |
| 2 | Who is entitled to wear a doctoral gown? | Academic Dress Policy | 0.601 | PASS | 0.902 | PASS | Academic Dress Policy - Section 7 - Definitions | bm25, vector |
| 3 | Can I keep my academic gown after the ceremony? | Academic Dress Policy | 0.600 | PASS | 0.797 | PASS | Academic Dress Policy - Section 5 - Policy Statement | bm25, vector |
| 4 | What happens if a student fails the same subject more than once? | Academic Progression Review Policy | 0.598 | FAIL | 0.985 | PASS | Academic Progression Review Policy - Part B - Details of Academic Progression Stages | bm25, vector |
| 5 | Can I appeal an academic progression decision? | Academic Progression Review Policy | 0.615 | FAIL | 0.882 | PASS | Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression | bm25 |
| 6 | What are the stages of academic progression review? | Academic Progression Review Policy | 0.595 | PASS | 0.999 | PASS | Academic Progression Review Policy - Part A - Monitoring and Determining Academic Progression | bm25, vector |
| 7 | How do I apply for promotion to Associate Professor? | Academic Promotions Policy | 0.565 | PASS | 0.977 | PASS | Academic Promotions Policy - Section 3 - Scope | bm25, vector |
| 8 | Who sits on the academic promotions committee? | Academic Promotions Policy | 0.645 | PASS | 0.998 | PASS | Academic Promotions Policy - Part D - Academic Promotions Committees | bm25, vector |
| 9 | What is the basis for academic promotion? | Academic Promotions Policy | 0.624 | PASS | 0.991 | PASS | Academic Promotions Policy - Part B - Basis for Promotion | bm25, vector |
| 10 | What qualifications must academic staff hold to teach a subject? | Academic Staff Qualifications Policy | 0.579 | PASS | 0.999 | PASS | Academic Staff Qualifications Policy - Section 5 - Policy Statement | bm25, vector |
| 11 | Does a lecturer need a qualification higher than the course they teach? | Academic Staff Qualifications Policy | 0.497 | FAIL | 0.107 | FAIL | Academic Staff Qualifications Policy - Section 5 - Policy Statement | vector |
| 12 | What are the English language requirements for admission? | English Language Entry Requirements Policy | 0.661 | PASS | 0.995 | PASS | English Language Entry Requirements Policy - Section 5 - Policy Statement | bm25, vector |
| 13 | Can I get credit for prior study when I apply? | VET Students Policy | 0.525 | PASS | 0.834 | PASS | VET Students Policy - Part C - Credit and Recognition of Prior Learning | bm25, vector |
| 14 | How are applications for admission assessed? | Admissions Policy | 0.567 | FAIL | 0.971 | FAIL | Recruitment Policy - Part I - Screening and Shortlisting Applicants | bm25, vector |
| 15 | How do I book a car parking permit on campus? | Campus Access, Premises and Facilities Policy | 0.655 | PASS | 0.876 | PASS | Campus Access, Premises and Facilities Policy - Part B - Parking | bm25, vector |
| 16 | What food is available at the campus cafe today? | _(none - out of scope)_ | 0.347 | PASS | 0.001 | PASS | Breastfeeding / Chestfeeding Policy - Part C - Breastfeeding/Chestfeeding/Parenting/Carer Facilities | bm25, vector |
| 17 | What is the wifi password for the student network? | _(none - out of scope)_ | 0.520 | FAIL | 0.205 | PASS | Library and Digital Learning Resources Policy - Part B - Access to Library Resources | bm25, vector |

## What changed

**Fixed by hybrid retrieval:**

- What happens if a student fails the same subject more than once? — vector 0.598 (returned Student Support Policy), hybrid 0.985 (returned Academic Progression Review Policy), found by bm25, vector
- Can I appeal an academic progression decision? — vector 0.615 (returned Graduate Research and RTP Scholarships Policy), hybrid 0.882 (returned Academic Progression Review Policy), found by bm25
- What is the wifi password for the student network? — vector 0.520 (returned Mobile Communication Device Policy), hybrid 0.205 (returned Library and Digital Learning Resources Policy), found by bm25, vector

No questions regressed.

## Observations

**1. Hybrid retrieval holds up at scale; vector-only degrades.**
This run uses the full 140-policy corpus rather than the five-policy pilot.
Against the pilot, vector-only scored 15/16 and hybrid 13/16 - vector-only
looked better. With 28x more content competing for the top spot, that
reverses: vector-only 12/17, hybrid 15/17. The pilot corpus was too small to
distinguish the two approaches, and testing only at that size would have
produced the wrong conclusion about which to build on.

**2. BM25 is doing the work at scale.**
Question 4 is the clearest case: vector-only returned the Student Support
Policy at 0.598, while hybrid returned the correct Academic Progression
Review Policy at 0.985. Question 5 returned the Graduate Research and RTP
Scholarships Policy under vector-only and was recovered by BM25 alone. Both
are semantically plausible neighbours that only literal term matching could
separate. BM25 contributed to the top result in 16 of 17 questions.

**3. Corpus expansion closed two of the three content gaps from Sprint 2.**
Question 12 (English language requirements) now returns the English Language
Entry Requirements Policy at 0.995 - the dedicated policy the Admissions
Policy had only cross-referenced. Question 13 (credit for prior study) now
returns VET Students Policy - Part C - Credit and Recognition of Prior
Learning at 0.834. Both previously failed because the answering document was
not in the corpus. This also explains two unexplained refusals in the
PCOIS2-51 generation tests: the model was correct to decline, because the
answer genuinely was not in the excerpts it was given.

**4. The corpus still covers Policies only, not Procedures or Standards.**
Question 13's answer is VET-specific because the general credit rules live in
the "Credit Standard" and "Admissions Procedure - Credit", which are a
different document type in the Policy Library and were excluded by the
discovery filter. Several policies delegate their operative detail this way.
Widening ingestion to Procedures, Standards and Schedules is a data-scoping
decision for the team, not a retrieval problem.

**5. Two test questions were wrong, not the system.**
Questions 12 and 15 originally expected the Admissions Policy and "no
relevant policy" respectively. Both expectations were written against the
five-policy corpus and became incorrect once the real corpus was ingested -
there is a Campus Access, Premises and Facilities Policy with a Part B on
Parking, so a parking question is no longer out of scope. Expected values
were corrected and a genuinely out-of-scope control (wifi password) added in
its place. Test sets written against a sample corpus need revisiting when the
corpus changes.

**6. Question 14 is the one real retrieval failure, and it worsened.**
"How are applications for admission assessed?" now returns Recruitment Policy
- Part I - Screening and Shortlisting Applicants at 0.971, up from Academic
Promotions at 0.795. The phrase "applications assessed" is used by student
admission, staff promotion and staff recruitment, and corpus growth added a
third competitor at higher confidence. Neither BM25 nor the reranker can
separate them, because the distinguishing context (student versus staff) is
not in the chunk text itself. A candidate mitigation is to use the policy
category already stored on each chunk to bias retrieval toward Student
Administration for student-phrased questions.

**7. Out-of-scope detection survived corpus growth, and the reranker is
essential to it.**
The wifi control scored 0.520 under vector-only, above the 0.35 threshold and
returning the Mobile Communication Device Policy. Under hybrid it scores
0.205. The campus cafe control scores 0.001. In both cases the reranker
correctly judged that a topically adjacent chunk does not answer the
question, which raw cosine similarity could not. With a larger corpus there
is always something superficially related, so the reranker becomes more
important as the corpus grows, not less.

**8. Recommended threshold.**
The lowest passing in-scope score is 0.797 (question 3); the highest
out-of-scope score is 0.205. The gap is wide, and the current 0.50 threshold
sits comfortably inside it with room on both sides. No change recommended.
Question 11 scores 0.107 and is discussed below.

**9. Question 11 remains an open case.**
"Does a lecturer need a qualification higher than the course they teach?"
scores 0.107 and is filtered before generation. The Academic Staff
Qualifications Policy states the principle - staff must be appropriately
qualified for the level of their teaching - but delegates the specific
requirement to the Higher Education Standards Framework and an associated
Procedure, neither of which is ingested. The low score is arguably correct
behaviour rather than a retrieval failure, and supports the scoping point in
observation 4.

**10. Section-level precision is still not measured.**
Several passing rows return Definitions, Purpose or Scope sections rather
than the operative clause - question 2 returns "Section 7 - Definitions",
question 7 returns "Section 3 - Scope". These pass because the test compares
policy titles only. Citation quality depends on landing on the right clause,
so the test set should carry expected sections in the next iteration. The
harness already has a field for this that is currently unused.

**Overall.** Hybrid retrieval justified itself under conditions the pilot
corpus could not test: three questions recovered, none regressed, and
out-of-scope detection intact at 28x scale. The remaining failure (question
14) is a semantic collision between student and staff policies that
retrieval alone cannot resolve, and the remaining gaps are ingestion scope
rather than ranking quality.
