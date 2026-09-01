import re

MIN_QUERY_LEN = 3
MAX_QUERY_LEN = 500

INJECTION_PATTERNS = [
    r"ignore (all|any|the)?\s*(previous|prior|above)\s*instructions",
    r"disregard (all|any|the)?\s*(previous|prior|above)\s*instructions",
    r"you are now",
    r"act as (if you are|a)",
    r"^\s*system\s*:",
    r"reveal (your|the) (system )?prompt",
    r"print (your|the) (system )?prompt",
    r"</?(script|iframe)",
]
_INJECTION_RE = re.compile("|".join(INJECTION_PATTERNS), re.IGNORECASE)


def check_input_safety(query: str):
    """Returns (is_safe: bool, reason: str | None).

    reason is None when is_safe is True; otherwise a short machine-readable
    tag the caller can log or map to a user-facing message.
    """
    if query is None:
        return False, "empty_input"

    stripped = query.strip()

    if len(stripped) < MIN_QUERY_LEN:
        return False, "too_short"

    if len(stripped) > MAX_QUERY_LEN:
        return False, "too_long"

    if _INJECTION_RE.search(stripped):
        return False, "possible_prompt_injection"

    return True, None