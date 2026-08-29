"""
PCOIS2-49: Prompt engineering for grounded answers.

The instructions that force the model to answer only from retrieved policy
text and to refuse rather than guess. This is the main hallucination
control in the system, and it defends against two distinct failure modes.

FAILURE MODE 1 - nothing relevant retrieved.
Handled mostly upstream: PCOIS2-47 testing showed out-of-scope questions
score 0.000 against a lowest in-scope score of 0.582, so a rerank
threshold of 0.5 filters them before generation. The prompt is the second
line of defence for anything that slips through.

FAILURE MODE 2 - the WRONG policy retrieved confidently.
This is the one the threshold cannot catch, and PCOIS2-47 found a live
example: "How are applications for admission assessed?" returned the
Academic Promotions Policy at 0.795. Promotion applications are also
"assessed", so the policies collide semantically. A prompt that only says
"answer from the provided text" would produce a fluent, confidently cited,
completely wrong answer.

So the instructions below do not merely say "use the excerpts". They
require the model to first check that the excerpts actually address the
question that was asked, and to refuse if they only cover a superficially
similar topic. Aaron's note on that test row applies: two honest refusals
are preferable to one confident error.

REFUSAL_MARKER exists so refusal is detected by exact string match rather
than by trying to parse whether prose sounds like a refusal. respond.py
checks for it and switches the response to the escalation path.
"""

# Exact token the model must emit when it cannot answer. Detected by
# string match downstream - deliberately not a natural sentence, so it
# cannot appear by accident in a real policy answer.
REFUSAL_MARKER = "NO_ANSWER_IN_POLICY"

SYSTEM_PROMPT = f"""You are a policy assistant for La Trobe University. You answer \
questions using ONLY the policy excerpts supplied with each question.

You will be given a question and numbered excerpts from official La Trobe \
University policy documents. Follow these rules exactly.

RULE 1 - CHECK RELEVANCE FIRST
Before writing anything, decide whether the excerpts actually answer the \
question that was asked. The excerpts were selected by an automated search \
and are sometimes about a different policy that merely uses similar wording. \
An excerpt about assessing staff promotion applications does not answer a \
question about assessing student admission applications, even though both \
use the words "applications" and "assessed".

RULE 2 - REFUSE WHEN THE ANSWER IS NOT THERE
If the excerpts do not contain the information needed, reply with exactly \
this and nothing else:
{REFUSAL_MARKER}

Use it whenever any of these are true:
- The excerpts are about a different topic or a different policy.
- The excerpts mention the topic only in passing, or refer the reader to \
another document that is not included.
- The excerpts are definitions or scope statements that name the topic but \
do not state the actual rule.
- You would have to rely on your own knowledge, assumptions, or general \
knowledge of universities to answer.

Refusing is the correct, expected outcome in these cases. Do not stretch a \
partial match into an answer.

RULE 3 - ANSWER ONLY FROM THE EXCERPTS
When the excerpts do answer the question, state what they say. Every fact \
in your answer must come from the excerpts. Never add context, examples, \
caveats, or procedural advice from your own knowledge, even if it would be \
helpful and even if you are confident it is true.

RULE 4 - DO NOT WRITE CITATIONS
Do not name policies, quote section numbers, or add references. Citations \
are attached automatically from the source records. Write only the answer \
itself.

RULE 5 - STYLE
Be brief and factual: two to four sentences. Use plain English. Write in \
the third person about what the policy requires - not "you must" but "staff \
must" or "the policy requires". Do not open with a preamble such as \
"According to the excerpts"; just state the position. Use Australian \
spelling."""


def build_user_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble the question and the retrieved excerpts into one message.

    Only the chunk TEXT is passed to the model. Titles, sections and URLs
    are deliberately withheld: the model must not be able to reproduce
    citation details, because citations are attached from the database
    records instead (PCOIS2-50). A model that cannot see a policy name
    cannot invent one.
    """
    if not chunks:
        return (
            f"Question: {question}\n\n"
            "No policy excerpts were found for this question."
        )

    parts = [f"Question: {question}", "", "Policy excerpts:"]
    for i, chunk in enumerate(chunks, start=1):
        text = " ".join(chunk["text"].split())
        parts.append(f"\n[Excerpt {i}]\n{text}")

    parts += [
        "",
        "Answer the question using only the excerpts above. If they do not "
        f"contain the answer, reply with exactly {REFUSAL_MARKER}.",
    ]
    return "\n".join(parts)


def is_refusal(answer: str) -> bool:
    """True if the model declined to answer.

    Matches on the marker appearing anywhere rather than equalling the
    whole reply, because small models sometimes wrap it in a sentence
    despite being told not to.
    """
    return REFUSAL_MARKER in answer.upper()
