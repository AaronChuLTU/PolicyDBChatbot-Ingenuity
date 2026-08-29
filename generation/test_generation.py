"""
Tests for the generation layer (PCOIS2-48/49/50).

Runs without Ollama or Postgres by substituting a stub retriever and a
stub LLM client, so the routing logic can be checked on its own. That is
the point: these tests prove that a refusal or a low score produces the
right schema response, independent of what any particular model happens
to say on the day.

Test data is taken from the real PCOIS2-47 retrieval results, including
row 14 - the case where the wrong policy was retrieved at a confident
0.795 - so the wrong-policy path is exercised with the score that
actually occurred.

    python test_generation.py
"""
from prompts import REFUSAL_MARKER, SYSTEM_PROMPT, build_user_prompt, is_refusal
from respond import (
    RERANK_THRESHOLD, answer_question, build_citations, confidence_label,
)

PASS, FAIL = "PASS", "FAIL"
results = []


def check(name, condition, detail=""):
    results.append((PASS if condition else FAIL, name, detail))


# --- Fixtures from the real PCOIS2-47 results ---------------------------

def chunk(title, section, score, text="Policy text.", url="https://policies.latrobe.edu.au/x"):
    return {
        "chunk_id": f"{title[:3]}-{section[:3]}",
        "policy_title": title,
        "section": section,
        "source_url": url,
        "text": text,
        "rerank_score": score,
    }


# Row 1: clean high-confidence hit
GOOD_HITS = [
    chunk("Academic Dress Policy", "Part D - Graduands", 0.999,
          "Academic dress must be worn as prescribed for the relevant award."),
    chunk("Academic Dress Policy", "Section 5 - Policy Statement", 0.797),
]

# Row 14: the dangerous one - confident score, wrong policy
WRONG_POLICY_HITS = [
    chunk("Academic Promotions Policy", "Section 5 - Policy Statement", 0.795,
          "Applications for promotion are assessed by the committee."),
]

# Rows 15/16: out-of-scope controls
OUT_OF_SCOPE_HITS = [
    chunk("Admissions Policy", "Section 8 - Authority", 0.000),
]

# Mixed scores: only the first should be cited
MIXED_HITS = [
    chunk("Admissions Policy", "Section 4 - Entry Requirements", 0.910),
    chunk("Admissions Policy", "Section 7 - Definitions", 0.028),
]


class StubRetriever:
    def __init__(self, hits):
        self.hits = hits

    def search(self, query, *a, **kw):
        return self.hits


class StubClient:
    """Returns a scripted reply, and records what it was sent."""

    def __init__(self, reply):
        self.reply = reply
        self.last_system = None
        self.last_user = None

    def generate(self, system, user, **kw):
        self.last_system = system
        self.last_user = user
        return self.reply


class BrokenClient:
    def generate(self, system, user, **kw):
        raise ConnectionError("connection refused")


# --- 1. Prompt construction ---------------------------------------------

user_msg = build_user_prompt("What is the dress code?", GOOD_HITS)

check("Prompt includes the question", "What is the dress code?" in user_msg)
check("Prompt includes excerpt text", "prescribed for the relevant award" in user_msg)
check("Prompt hides policy titles from the model",
      "Academic Dress Policy" not in user_msg,
      "titles withheld so the model cannot invent citations")
check("Prompt hides section names from the model", "Part D - Graduands" not in user_msg)
check("Prompt hides source URLs from the model", "policies.latrobe.edu.au" not in user_msg)
check("System prompt forbids writing citations", "Do not name policies" in SYSTEM_PROMPT)
check("System prompt warns about similar-wording policies",
      "admission applications" in SYSTEM_PROMPT,
      "the row 14 failure mode is described explicitly")

# --- 2. Refusal detection ------------------------------------------------

check("Detects a bare refusal marker", is_refusal(REFUSAL_MARKER))
check("Detects a marker wrapped in prose",
      is_refusal(f"I'm sorry, {REFUSAL_MARKER}."))
check("Does not flag a normal answer",
      not is_refusal("Academic dress must be worn at graduation ceremonies."))

# --- 3. Citations --------------------------------------------------------

cites = build_citations(GOOD_HITS)
check("Citations use the schema field names",
      set(cites[0]) == {"policy_title", "section", "source_url"})
check("Citations come from chunk metadata",
      cites[0]["policy_title"] == "Academic Dress Policy")

check("Low-scoring chunks are not cited",
      len(build_citations(MIXED_HITS)) == 1,
      "0.028 chunk excluded")

dupes = [chunk("Admissions Policy", "Section 4", 0.9),
         chunk("Admissions Policy", "Section 4", 0.8)]
check("Duplicate policy+section collapses to one citation",
      len(build_citations(dupes)) == 1)

# --- 4. Confidence mapping ----------------------------------------------

check("0.999 -> high", confidence_label(0.999) == "high")
check("0.582 -> medium", confidence_label(0.582) == "medium",
      "lowest passing in-scope score from PCOIS2-47")
check("0.028 -> low", confidence_label(0.028) == "low")

# --- 5. End-to-end routing ----------------------------------------------

# Success
client = StubClient("Academic dress must be worn as prescribed for the award.")
r = answer_question("What is the dress code?", StubRetriever(GOOD_HITS), client)
check("Good hit -> status success", r["status"] == "success")
check("Good hit -> confidence high", r["confidence"] == "high")
check("Good hit -> no escalation", r["escalation_required"] is False)
check("Good hit -> citations attached", len(r["citations"]) > 0)
check("Answer text comes from the model",
      r["answer"] == "Academic dress must be worn as prescribed for the award.")

# Out of scope - below threshold, never reaches the model
client = StubClient("This should never be called.")
r = answer_question("Where can I park?", StubRetriever(OUT_OF_SCOPE_HITS), client)
check("Below threshold -> status out_of_scope", r["status"] == "out_of_scope")
check("Below threshold -> no citations", r["citations"] == [],
      "schema rule: out-of-scope shows no unrelated sources")
check("Below threshold -> escalates", r["escalation_required"] is True)
check("Below threshold -> model never called", client.last_user is None,
      "saves an inference call and removes any chance of a guess")

# Wrong policy retrieved confidently - the row 14 case.
# Score 0.795 clears the threshold, so the prompt is the only defence.
client = StubClient(REFUSAL_MARKER)
r = answer_question("How are admission applications assessed?",
                    StubRetriever(WRONG_POLICY_HITS), client)
check("Wrong policy + refusal -> status low_confidence",
      r["status"] == "low_confidence",
      "score 0.795 cleared the threshold; the prompt caught it")
check("Wrong policy + refusal -> escalates", r["escalation_required"] is True)
check("Wrong policy + refusal -> no invented answer",
      REFUSAL_MARKER not in r["answer"],
      "marker replaced with a readable message")
check("Wrong policy + refusal -> confidence low", r["confidence"] == "low")

# Empty reply treated as a refusal
r = answer_question("Anything?", StubRetriever(GOOD_HITS), StubClient("   "))
check("Empty model reply -> low_confidence", r["status"] == "low_confidence")

# LLM unreachable
r = answer_question("Anything?", StubRetriever(GOOD_HITS), BrokenClient())
check("LLM down -> status error", r["status"] == "error")
check("LLM down -> escalates", r["escalation_required"] is True)

# --- 6. Schema conformance ----------------------------------------------

EXPECTED_FIELDS = {
    "status", "question", "answer", "citations", "confidence",
    "escalation_required", "escalation_message",
}
VALID_STATUS = {"success", "out_of_scope", "low_confidence", "error"}
VALID_CONFIDENCE = {"high", "medium", "low"}

samples = [
    answer_question("q", StubRetriever(GOOD_HITS), StubClient("An answer.")),
    answer_question("q", StubRetriever(OUT_OF_SCOPE_HITS), StubClient("x")),
    answer_question("q", StubRetriever(GOOD_HITS), StubClient(REFUSAL_MARKER)),
    answer_question("q", StubRetriever(GOOD_HITS), BrokenClient()),
]

check("All responses have exactly the schema fields",
      all(set(s) == EXPECTED_FIELDS for s in samples))
check("All statuses are valid", all(s["status"] in VALID_STATUS for s in samples))
check("All confidence values are valid",
      all(s["confidence"] in VALID_CONFIDENCE for s in samples))
check("Question is echoed back", all(s["question"] == "q" for s in samples))
check("Escalation always carries a message",
      all(s["escalation_message"] for s in samples if s["escalation_required"]))


# --- Report --------------------------------------------------------------

if __name__ == "__main__":
    passed = sum(1 for r in results if r[0] == PASS)
    for status, name, detail in results:
        line = f"[{status}] {name}"
        if detail:
            line += f"\n         {detail}"
        print(line)
    print(f"\n{passed}/{len(results)} passed")
    if passed != len(results):
        raise SystemExit(1)
