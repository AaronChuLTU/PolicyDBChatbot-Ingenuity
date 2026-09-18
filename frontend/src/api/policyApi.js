// policyApi.js
// Single place for all calls to the RAG/chatbot backend.
//
// PCOIS2-64: the mock is gone — this now calls the real service built in
// PCOIS2-56 (backend/main.py):
//
//   POST /ask  {"question": "..."}  ->  the PCOIS2-31 schema object
//   GET  /health                    ->  {status, database, ollama}
//
// Response shape (PCOIS2-31, Alina):
//   { status, question, answer, citations[], confidence,
//     escalation_required, escalation_message }
// where each citation = { policy_title, section, source_url }.

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// The backend's own Ollama timeout defaults to 120s (OLLAMA_TIMEOUT), so
// give it a little more than that before we give up from this side.
// Without a ceiling here, a hung backend leaves "Thinking…" on screen
// indefinitely with no way out — which is the failure PCOIS2-65 exists
// to prevent.
const REQUEST_TIMEOUT_MS = 130000;

/**
 * A failure reaching or parsing the policy service.
 *
 * `status` is the HTTP status when the request landed and came back bad,
 * or null when it never landed at all (server down, DNS, CORS, timeout).
 * The UI shows `message` directly, so every message thrown from here is
 * written to be read by a user.
 */
export class PolicyApiError extends Error {
  constructor(message, { status = null, cause = null } = {}) {
    super(message);
    this.name = "PolicyApiError";
    this.status = status;
    this.cause = cause;
  }
}

/** Pull FastAPI's `{detail: ...}` out of a failed response, if present. */
async function readDetail(res) {
  try {
    const body = await res.json();
    if (typeof body?.detail === "string") return body.detail;
    // 422 validation errors arrive as a list of {loc, msg, type}.
    if (Array.isArray(body?.detail)) {
      return body.detail.map((d) => d?.msg).filter(Boolean).join("; ");
    }
  } catch {
    // Not JSON — an HTML error page from a proxy, or an empty body.
  }
  return "";
}

function messageForStatus(status, detail) {
  // 503 is the one the backend raises deliberately: Postgres was
  // unreachable at startup, so get_retriever() refuses. Its detail text
  // is already written for a human, so pass it through.
  if (status === 503) {
    return detail || "Policy search is currently unavailable. Please try again shortly.";
  }
  if (status === 422) {
    return "That question couldn't be sent to the policy service. Try rewording it.";
  }
  if (status === 404) {
    return `No /ask endpoint found at ${API_BASE}. Check VITE_API_BASE_URL points at the backend.`;
  }
  if (status >= 500) {
    return "The policy service ran into a problem answering that. Please try again.";
  }
  return detail || `The policy service rejected the request (HTTP ${status}).`;
}

/** Minimal guard that what came back is actually our schema. */
function looksLikeSchema(body) {
  return (
    body &&
    typeof body === "object" &&
    typeof body.status === "string" &&
    typeof body.answer === "string" &&
    Array.isArray(body.citations)
  );
}

/**
 * Send a user's question to the backend and get a schema-shaped response.
 *
 * Resolves with the PCOIS2-31 object — including `status: "error"`, which
 * is a normal 200 the backend returns when retrieval or Ollama failed
 * mid-pipeline. That case is the caller's to handle, not an exception.
 *
 * Throws PolicyApiError when the request itself failed: service down,
 * timed out, bad status, or a body that isn't the agreed schema.
 *
 * @param {string} question
 * @param {{signal?: AbortSignal}} [options] caller's signal, for cancelling
 *   an in-flight request when the component unmounts or a newer question
 *   supersedes this one.
 */
export async function askPolicyQuestion(question, { signal } = {}) {
  const controller = new AbortController();
  const timer = setTimeout(() => controller.abort(), REQUEST_TIMEOUT_MS);

  // Forward the caller's cancellation onto our controller, so either can
  // abort the request. (AbortSignal.any() isn't widely enough supported.)
  const forwardAbort = () => controller.abort();
  if (signal) {
    if (signal.aborted) controller.abort();
    else signal.addEventListener("abort", forwardAbort, { once: true });
  }

  let res;
  try {
    res = await fetch(`${API_BASE}/ask`, {
     method: "POST",
     headers: {
       "Content-Type": "application/json",
       "X-API-Key": import.meta.env.VITE_API_KEY,
     },
     body: JSON.stringify({ question }),
     signal: controller.signal,
   });
  } catch (err) {
    // The caller cancelled deliberately — let that propagate untouched so
    // the UI can tell it apart from a real failure and stay quiet.
    if (signal?.aborted) throw err;

    if (err?.name === "AbortError") {
      throw new PolicyApiError(
        "The policy service took too long to respond. Please try again.",
        { cause: err },
      );
    }
    // fetch only rejects on network-level failure: server down, DNS,
    // CORS rejection. A 500 is a resolved promise, handled below.
    throw new PolicyApiError(
      `Couldn't reach the policy service at ${API_BASE}. Check it's running, then try again.`,
      { cause: err },
    );
  } finally {
    clearTimeout(timer);
    signal?.removeEventListener("abort", forwardAbort);
  }

  if (!res.ok) {
    throw new PolicyApiError(messageForStatus(res.status, await readDetail(res)), {
      status: res.status,
    });
  }

  let body;
  try {
    body = await res.json();
  } catch (err) {
    throw new PolicyApiError("The policy service returned a response we couldn't read.", {
      status: res.status,
      cause: err,
    });
  }

  if (!looksLikeSchema(body)) {
    throw new PolicyApiError(
      "The policy service returned an unexpected response. Check VITE_API_BASE_URL.",
      { status: res.status },
    );
  }

  return body;
}

/**
 * Liveness of the backend's two dependencies. Not used by the chat flow —
 * handy when debugging why /ask keeps erroring, since it separates
 * "Postgres is down" from "Ollama is down".
 */
export async function checkHealth({ signal } = {}) {
  const res = await fetch(`${API_BASE}/health`, { signal });
  if (!res.ok) {
    throw new PolicyApiError(`Health check failed (HTTP ${res.status}).`, {
      status: res.status,
    });
  }
  return res.json();
}
