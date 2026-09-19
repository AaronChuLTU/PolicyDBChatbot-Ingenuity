// App.jsx — the page shell for the Policy DB Chatbot.
//
// Sprint 4:
//   PCOIS2-64 — the conversation now runs against the real POST /ask
//               endpoint (PCOIS2-56) via src/api/policyApi.js.
//   PCOIS2-65 — a "Thinking…" indicator while the request is in flight,
//               and a recoverable error state with a Try again button.

import { useState, useEffect, useRef } from "react";
import Message from "./components/Message.jsx";
import { askPolicyQuestion } from "./api/policyApi.js";
import "./styles/theme.css";
import "./styles/app.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  // { message, question } — question is kept so Try again can resend it.
  const [error, setError] = useState(null);
  const [theme, setTheme] = useState(() => localStorage.getItem("theme") || "light");

  // The in-flight request, so it can be cancelled on unmount.
  const requestRef = useRef(null);

  // Apply the chosen theme to the <html> element so the CSS tokens switch,
  // and persist it so it survives a page refresh.
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
    localStorage.setItem("theme", theme);
  }, [theme]);

  // Don't leave a request running against an unmounted component.
  useEffect(() => () => requestRef.current?.abort(), []);

  function toggleTheme() {
    setTheme((t) => (t === "light" ? "dark" : "light"));
  }

  /**
   * Send a question and fold the result into the conversation.
   *
   * `isRetry` skips re-appending the user's bubble: on a retry the
   * question is already sitting in the transcript, and echoing it again
   * would make the history read as though they asked twice.
   */
  async function ask(question, { isRetry = false } = {}) {
    if (!question || loading) return;

    setError(null);
    if (!isRetry) {
      setMessages((m) => [...m, { role: "user", text: question }]);
      setInput("");
    }
    setLoading(true);

    const controller = new AbortController();
    requestRef.current = controller;

    try {
      const res = await askPolicyQuestion(question, { signal: controller.signal });

      // status "error" is the backend telling us the pipeline broke
      // partway (retrieval or Ollama unreachable) — see respond.py's
      // error_response(). It arrives as a normal 200, but it isn't an
      // answer, so it belongs in the error state where the user gets a
      // Try again rather than in the transcript as a bot reply.
      if (res.status === "error") {
        setError({ message: res.answer, question });
        return;
      }

      setMessages((m) => [
        ...m,
        {
          role: "bot",
          text: res.answer,
          citations: res.citations,
          confidence: res.confidence,
          escalation: res.escalation_required ? res.escalation_message : "",
        },
      ]);
    } catch (err) {
      // We cancelled this ourselves (unmount) — nothing to report.
      if (err?.name === "AbortError" && controller.signal.aborted) return;
      setError({
        message: err?.message || "Something went wrong. Please try again.",
        question,
      });
    } finally {
      // Only the newest request owns the loading flag.
      if (requestRef.current === controller) {
        requestRef.current = null;
        setLoading(false);
      }
    }
  }

  function handleSend() {
    ask(input.trim());
  }

  function handleRetry() {
    if (error) ask(error.question, { isRetry: true });
  }

  function handleKeyDown(e) {
    // isComposing guards against Enter committing an IME candidate
    // (Chinese, Japanese, Korean input) being read as "send".
    if (e.key === "Enter" && !e.nativeEvent.isComposing) handleSend();
  }

  return (
    <div className="app">
      <header className="app-header">
        <div className="app-header__inner">
          <div className="app-header__mark" aria-hidden="true">
            <svg viewBox="0 0 24 24" width="22" height="22" fill="none">
              <path
                d="M4 5.5C4 4.67 4.67 4 5.5 4h13c.83 0 1.5.67 1.5 1.5v9c0 .83-.67 1.5-1.5 1.5H9l-4 3.5V16H5.5C4.67 16 4 15.33 4 14.5v-9Z"
                fill="currentColor"
              />
              <circle cx="9" cy="10" r="1.15" fill="var(--mark-bg)" />
              <circle cx="12" cy="10" r="1.15" fill="var(--mark-bg)" />
              <circle cx="15" cy="10" r="1.15" fill="var(--mark-bg)" />
            </svg>
          </div>
          <div>
            <h1 className="app-header__title">Ingenuity</h1>
            <p className="app-header__sub">Answers grounded in official university policy</p>
          </div>
          <button
            className="app-header__toggle"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
          >
            {theme === "light" ? "🌙 Dark" : "☀ Light"}
          </button>
        </div>
      </header>

      <div className="disclaimer">
        Guidance based only on published policy. For binding decisions, confirm with the relevant university contact.
      </div>

      <main className="conversation">
        {messages.length === 0 && !loading && !error ? (
          <div className="empty-state">
            <h2>Ask about a university policy</h2>
            <p>Try “What are the rules on academic dress for graduation?”</p>
          </div>
        ) : (
          messages.map((m, i) => (
            <Message
              key={i}
              role={m.role}
              text={m.text}
              citations={m.citations}
              confidence={m.confidence}
              escalation={m.escalation}
            />
          ))
        )}

        {/* PCOIS2-65: in-flight indicator. role="status" so screen readers
            announce it without stealing focus. */}
        {loading && (
          <div className="thinking" role="status" aria-live="polite">
            <span className="thinking__dots" aria-hidden="true">
              <i />
              <i />
              <i />
            </span>
            <span className="thinking__label">Thinking…</span>
          </div>
        )}

        {/* PCOIS2-65: recoverable error. Sits below the question rather
            than replacing it, so the user can see what failed and resend
            it without retyping. */}
        {error && !loading && (
          <div className="error-note" role="alert">
            <p className="error-note__text">{error.message}</p>
            <button className="error-note__retry" onClick={handleRetry}>
              Try again
            </button>
          </div>
        )}
      </main>

      <div className="composer">
        <div className="composer__inner">
          <input
            className="composer__input"
            placeholder="Ask about a university policy"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyDown}
            disabled={loading}
            aria-label="Ask about a university policy"
          />
          <button className="composer__send" onClick={handleSend} disabled={loading}>
            {loading ? "Sending…" : "Send"}
          </button>
        </div>
      </div>
    </div>
  );
}
