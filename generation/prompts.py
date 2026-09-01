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

FAILURE MODE 3 - over-refusal (added after PCOIS2-51 live testing).
The first live run refused 5 of 12 in-scope questions, several with rerank
scores above 0.97. Refusing is the safe direction to fail, but at that rate
the assistant declines a large share of legitimate questions. Three changes
below target it:

  1. RULE ORDER. Answering now comes before refusing. The original listed
     the refusal rule second and the answering rule third, and gave a
     detailed worked example of when to refuse with no matching example of
     when to answer. The instructions taught refusal by example and
     answering by assertion.

  2. USER PROMPT ENDING. build_user_prompt used to close with "If they do
     not contain the answer, reply with exactly NO_ANSWER_IN_POLICY" - the
     last thing the model read before generating. It now closes on the
     answering instruction, with refusal as the subordinate clause.

  3. SECTION TITLES. Excerpts now carry their section heading. A chunk
     headed "Part B - Basis for Promotion" is strong evidence that it
     answers "what is the basis for promotion", and withholding it threw
     that signal away. Policy names are still withheld, so the model cannot
     reproduce a citation even if it ignores Rule 5. Set
     INCLUDE_SECTION_TITLES = False to restore the original behaviour.

An honest caveat for whoever reads this next: these are hypotheses, tested
by re-running test_generation_live.py and comparing against the committed
baseline. An earlier attempt to fix over-refusal by loosening one Rule 3
bullet produced no improvement and one regression, and was reverted. The
citation lists on refused questions in that run also show TOC and Preamble
chunks reaching the model, so some of the over-refusal is likely caused by
the clean_and_chunk.py duplication defect rather than by this file.

REFUSAL_MARKER exists so refusal is detected by exact string match rather
than by trying to parse whether prose sounds like a refusal. respond.py
checks for it and switches the response to the escalation path.
"""

# Exact token the model must emit when it cannot answer. Detected by
# string match downstream - deliberately not a natural sentence, so it
# cannot appear by accident in a real policy answer.
REFUSAL_MARKER = "NO_ANSWER_IN_POLICY"

# Whether to show each excerpt's section heading to the model. Policy
# titles and URLs are never shown either way.
INCLUDE_SECTION_TITLES = True

SYSTEM_PROMPT = f"""You are a policy assistant for La Trobe University. You answer \
questions using ONLY the policy excerpts supplied with each question.

You will be given a question and numbered excerpts from official La Trobe \
University policy documents. Follow these rules exactly.

RULE 1 - CHECK RELEVANCE FIRST
Before writing anything, decide whether the excerpts address the question \
that was asked. The excerpts were selected by an automated search and are \
sometimes about a different policy that merely uses similar wording. An \
excerpt about assessing staff promotion applications does not answer a \
question about assessing student admission applications, even though both \
use the words "applications" and "assessed".

RULE 2 - ANSWER WHEN THE EXCERPTS ADDRESS THE QUESTION
If they do, state what they say. Every fact in your answer must come from \
the excerpts.

Policy documents often answer a question by stating a principle or a \
requirement rather than a step-by-step procedure. A principle is an answer. \
Answer, rather than refusing, when:
- the excerpt states what the University requires, ensures or approves, \
even if it does not list steps;
- the excerpt answers part of the question - answer that part and say \
nothing about the rest;
- the answer is shorter or more general than you expected.

Worked example. Asked "What is the basis for academic promotion?" and given \
an excerpt stating that applications are judged on their merit and assessed \
on evidence of quality, outcomes and impact across domains, the correct \
response states exactly that. It is an answer, not a scope statement.

RULE 3 - REFUSE WHEN THE ANSWER IS NOT THERE
If the excerpts do not contain the information needed, reply with exactly \
this and nothing else:
{REFUSAL_MARKER}

Use it when any of these are true:
- The excerpts are about a different topic or a different policy.
- The excerpts name the topic only in passing, or refer the reader to \
another document that is not included.
- The excerpts only define terms, or state which people or courses the \
policy applies to, without addressing what was asked.
- The excerpts are a table of contents, a list of section headings, or \
document administration details rather than policy content.
- You would have to rely on your own knowledge, assumptions, or general \
knowledge of universities to answer.

Refusing is correct in these cases. Do not stretch a genuinely unrelated \
excerpt into an answer. But do not refuse simply because the excerpts are \
briefer or more general than you would like - see Rule 2.

RULE 4 - NEVER ADD ANYTHING OF YOUR OWN
Never add context, examples, caveats, or procedural advice from your own \
knowledge, even if it would be helpful and even if you are confident it is \
true. If the excerpts do not say it, it does not appear in your answer.

RULE 5 - DO NOT WRITE CITATIONS
Do not name policies, quote section or part numbers, or add references. \
Citations are attached automatically from the source records. Write only \
the answer itself.

RULE 6 - STYLE
Be brief and factual: two to four sentences. Use plain English. Write in \
the third person about what the policy requires - not "you must" but "staff \
must" or "the policy requires". Do not open with a preamble such as \
"According to the excerpts"; just state the position. Use Australian \
spelling."""


def build_user_prompt(question: str, chunks: list[dict]) -> str:
    """Assemble the question and the retrieved excerpts into one message.

    Policy titles and URLs are never passed to the model: citations are
    attached from the database records instead (PCOIS2-50), and a model
    that cannot see a policy name cannot invent one. Section headings ARE
    passed when INCLUDE_SECTION_TITLES is set, because the heading is often
    the clearest signal that a chunk answers the question - "Part B - Basis
    for Promotion" against "what is the basis for promotion". Rule 5 still
    forbids writing them into the answer, and test_generation_live.py
    detects violations.

    The closing instruction leads with answering rather than refusing. The
    last line before generation primes the response, and the original
    ended on the refusal marker.
    """
    if not chunks:
        return (
            f"Question: {question}\n\n"
            "No policy excerpts were found for this question."
        )

    parts = [f"Question: {question}", "", "Policy excerpts:"]
    for i, chunk in enumerate(chunks, start=1):
        text = " ".join(chunk["text"].split())
        section = (chunk.get("section") or "").strip()
        if INCLUDE_SECTION_TITLES and section:
            parts.append(f"\n[Excerpt {i} - {section}]\n{text}")
        else:
            parts.append(f"\n[Excerpt {i}]\n{text}")

    parts += [
        "",
        "Answer the question using only the excerpts above, stating what "
        "they say even if they state a principle rather than a procedure. "
        "Only if they genuinely do not address the question, reply with "
        f"exactly {REFUSAL_MARKER}.",
    ]
    return "\n".join(parts)


def is_refusal(answer: str) -> bool:
    """True if the model declined to answer.

    Matches on the marker appearing anywhere rather than equalling the
    whole reply, because small models sometimes wrap it in a sentence
    despite being told not to.
    """
    return REFUSAL_MARKER in answer.upper()
