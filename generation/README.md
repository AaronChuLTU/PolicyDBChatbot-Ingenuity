# Generation layer (Sprint 3) — David

Turns a question into the response object the frontend renders. Sits
downstream of `hybrid_search.py` and upstream of `frontend/`.

```
question --> HybridRetriever --> [score >= 0.5?] --> Ollama/Qwen3 --> response JSON
             (PCOIS2-46)          respond.py         ollama_client     respond.py
                                                     + prompts.py      (PCOIS2-50)
```

| File | Ticket | What it does |
|---|---|---|
| `ollama_client.py` | PCOIS2-48 | Talks to Ollama's local API. Plumbing only — no policy logic |
| `prompts.py` | PCOIS2-49 | The instructions that force grounded answers and refusals |
| `respond.py` | PCOIS2-50 | Assembles the PCOIS2-31 schema response and attaches citations |
| `test_generation.py` | — | Logic tests; runs without Ollama or Postgres |

## Setup

```bash
pip install -r requirements.txt      # adds `requests` (already present)
ollama serve                         # in a separate terminal
ollama pull qwen3
```

Config (defaults suit a standard local install):

```bash
export OLLAMA_HOST=http://localhost:11434
export OLLAMA_MODEL=qwen3
export OLLAMA_TIMEOUT=120
```

## Run

```bash
python ollama_client.py                       # smoke test: is Ollama up?
python respond.py "What academic dress do graduands wear?"
python test_generation.py                     # 38 logic tests
```

`respond.py` prints the full schema object, so its output can be pasted
straight into the frontend's mock in `src/api/policyApi.js` to check the
UI renders it correctly.

## Two defences against hallucination

**1. The score threshold (`respond.py`).** Rerank score below 0.50 → the
model is never called at all; the response is `out_of_scope` with no
citations. The value comes from PCOIS2-47: out-of-scope controls scored
0.000, lowest passing in-scope question 0.582.

**2. The prompt (`prompts.py`).** The threshold cannot catch a *confidently
retrieved wrong policy* — PCOIS2-47 row 14 returned the Academic Promotions
Policy for an admissions question at 0.795, well clear of the threshold.
The system prompt therefore requires the model to check the excerpts
actually address the question before answering, and to emit
`NO_ANSWER_IN_POLICY` if they only cover a similar-sounding topic. That
routes to `low_confidence` + escalation instead of a fluent wrong answer.

## Citations cannot be hallucinated

`build_user_prompt` passes excerpt **text only** — no titles, sections or
URLs reach the model. Citations are read from the `policy_chunks` metadata
carried through retrieval, so a citation records which database row was
retrieved rather than what the model claims. A model that never sees a
policy name cannot invent one.

Chunks scoring below 0.50 are dropped from the citation list even when the
answer was generated, so a 0.028 chunk in the top-5 does not get an
authoritative-looking reference attached to it.

## What's tested vs. what needs a live run

Written without access to Ollama or a populated Postgres, so:

| Component | Status |
|---|---|
| Response routing, thresholds, citation building, schema conformance | **Tested** — 38 assertions in `test_generation.py`, using stub retriever/client and score fixtures taken from the real PCOIS2-47 results (including row 14 at 0.795) |
| `prompts.py` construction, refusal detection | **Tested** — asserts titles/sections/URLs never reach the model and that the marker is detected bare or wrapped in prose |
| `ollama_client.py` HTTP call | **Not run** — needs Ollama installed. The endpoint (`POST /api/chat`), payload and response shape follow Ollama's documented API, but nobody has executed it |
| Whether Qwen3 actually obeys the prompt | **Not tested** — this is the important one, see below |

**First things to do when you run this for real:**

1. `python ollama_client.py` — confirms Ollama is up and the model is pulled.
2. Run the PCOIS2-47 out-of-scope controls through `respond.py`
   ("How do I book a car parking permit on campus?", "What food is available
   at the campus cafe today?"). Both should come back `out_of_scope` without
   reaching the model.
3. **Run row 14 — `"How are applications for admission assessed?"`** This is
   the acceptance test for PCOIS2-49. Retrieval will hand it Academic
   Promotions text at ~0.795. A pass is `low_confidence` + escalation. A
   fluent answer about promotion committees is a fail, and means the prompt
   needs tightening.
4. Check Qwen3 isn't leaking `<think>` reasoning into answers. `think: false`
   plus `strip_reasoning()` should handle it; verify on the older Ollama
   builds that ignore the flag.
5. If the model over-refuses on valid questions, that is the safer direction
   to fail — loosen Rule 2 before touching the threshold.

## Overlap with other Sprint 3 tickets

`respond.py` necessarily touches ground owned by other tickets, because the
confidence gate and the escalation text sit on the same code path as the
response formatting. Flagging rather than duplicating:

- **PCOIS2-52 (confidence gating)** — `RERANK_THRESHOLD`, `top_score()` and
  `confidence_label()` are a working implementation. Build on these or
  replace them; they should not be written twice.
- **PCOIS2-53 (escalation message + contact routing)** — the
  `ESCALATION_*` constants currently hold the wording from Alina's PCOIS2-31
  examples. They are placeholders for whoever owns the real contact routing;
  swap the strings, no other change needed.
- **PCOIS2-51 (test generation, log hallucination cases)** — the live model
  testing this module could not do. Start with the row 14 acceptance test in
  step 3 above.
- **PCOIS2-56 (callable API endpoint)** — this module is deliberately not a
  web service. `answer_question(question, retriever, client)` returns the
  schema dict ready to serialise; the endpoint wraps it.

