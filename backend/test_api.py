"""
Tests for PCOIS2-56's FastAPI wrapper.

Same approach as generation/test_generation.py: a stub retriever and stub
LLM client are swapped in via FastAPI's dependency-override mechanism, so
these checks run without a live Postgres or Ollama. What answer_question()
itself decides for a given score or refusal is already covered by
generation/test_generation.py - this file only checks the HTTP layer on
top of it: status codes, response-schema conformance, and error handling.

    pip install fastapi uvicorn httpx   (httpx: TestClient dependency only)
    python test_api.py
"""
import sys

from fastapi import HTTPException
from fastapi.testclient import TestClient

from main import app, get_client, get_retriever

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, condition, detail=""):
    results.append((PASS if condition else FAIL, name, detail))


class StubRetriever:
    def __init__(self, hits):
        self.hits = hits

    def search(self, query, *a, **kw):
        return self.hits


class StubClient:
    """Returns a scripted reply, mirroring generation/test_generation.py."""

    def __init__(self, reply):
        self.reply = reply

    def generate(self, system, user, **kw):
        return self.reply

    def is_available(self):
        return True


def chunk(title, section, score, text="Policy text.",
          url="https://policies.latrobe.edu.au/x"):
    return {
        "chunk_id": f"{title[:3]}-{section[:3]}", "policy_title": title,
        "section": section, "source_url": url, "text": text,
        "rerank_score": score,
    }


GOOD_HIT = [chunk("Academic Dress Policy", "Part D - Graduands", 0.95,
                   "Academic dress must be worn as prescribed for the award.")]
OUT_OF_SCOPE_HIT = [chunk("Admissions Policy", "Section 8 - Authority", 0.0)]


def use(retriever_hits, reply):
    app.dependency_overrides[get_retriever] = lambda: StubRetriever(retriever_hits)
    app.dependency_overrides[get_client] = lambda: StubClient(reply)


client = TestClient(app)

# 1. Success path: 200 + a schema-conformant, fully-populated body
use(GOOD_HIT, "Academic dress must be worn as prescribed for the award.")
resp = client.post("/ask", json={"question": "What academic dress do graduands wear?"})
check("success -> 200", resp.status_code == 200, resp.text)
body = resp.json()
check("success -> status=success", body.get("status") == "success", body)
check("success -> one citation", len(body.get("citations", [])) == 1, body)
check("success -> escalation_required False", body.get("escalation_required") is False, body)

# 2. Out-of-scope: nothing clears the relevance threshold
use(OUT_OF_SCOPE_HIT, "irrelevant - should never be sent to the model")
resp = client.post("/ask", json={"question": "What food is available at the campus cafe today?"})
body = resp.json()
check("out_of_scope -> 200", resp.status_code == 200, resp.text)
check("out_of_scope -> status", body.get("status") == "out_of_scope", body)
check("out_of_scope -> no citations", body.get("citations") == [], body)

# 3. Model refuses (wrong-policy guard) -> low_confidence, not a crash
use(GOOD_HIT, "NO_ANSWER_IN_POLICY")
resp = client.post("/ask", json={"question": "Who is entitled to wear a doctoral gown?"})
check("refusal -> low_confidence", resp.json().get("status") == "low_confidence", resp.json())

# 4. Malformed request -> 422, not a 500
resp = client.post("/ask", json={})
check("missing question -> 422", resp.status_code == 422, resp.text)

# 5. Retriever unavailable (startup failed / Postgres down) -> 503, not a crash
def broken_retriever():
    raise HTTPException(status_code=503, detail="Policy search is unavailable: db down")


app.dependency_overrides[get_retriever] = broken_retriever
resp = client.post("/ask", json={"question": "anything"})
check("retriever down -> 503", resp.status_code == 503, resp.text)

# 6. Health endpoint shape
use(GOOD_HIT, "n/a")
resp = client.get("/health")
check("health -> 200", resp.status_code == 200, resp.text)
check("health -> has status/database/ollama",
      {"status", "database", "ollama"} <= resp.json().keys(), resp.json())

app.dependency_overrides.clear()

# --- report ---
passed = sum(1 for r, _, _ in results if r == PASS)
for status, name, detail in results:
    line = f"[{status}] {name}"
    if status == FAIL:
        line += f"  -> {detail}"
    print(line)
print(f"\n{passed}/{len(results)} passed")

if passed != len(results):
    sys.exit(1)
