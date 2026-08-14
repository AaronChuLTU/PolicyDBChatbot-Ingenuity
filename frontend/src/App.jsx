// App.jsx — the page shell for the Policy DB Chatbot.
// Sprint 2 scope: framework chosen (React+Vite), repo structured, and this
// basic shell in place — header, disclaimer, conversation area, composer.
// The backend call is stubbed in src/api/policyApi.js until retrieval is ready.

import { useState, useEffect } from "react";
import Message from "./components/Message.jsx";
import { askPolicyQuestion } from "./api/policyApi.js";
import "./styles/theme.css";
import "./styles/app.css";

export default function App() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [theme, setTheme] = useState("light");

  // Apply the chosen theme to the <html> element so the CSS tokens switch.
  useEffect(() => {
    document.documentElement.setAttribute("data-theme", theme);
  }, [theme]);

  function toggleTheme() {
    setTheme((t) => (t === "light" ? "dark" : "light"));
  }

  async function handleSend() {
    const question = input.trim();
    if (!question || loading) return;

    setMessages((m) => [...m, { role: "user", text: question }]);
    setInput("");
    setLoading(true);

    try {
      const res = await askPolicyQuestion(question);
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
      setMessages((m) => [
        ...m,
        { role: "bot", text: "Sorry — I couldn't reach the policy service. Please try again." },
      ]);
    } finally {
      setLoading(false);
    }
  }

  function handleKeyDown(e) {
    if (e.key === "Enter") handleSend();
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
        {messages.length === 0 ? (
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
        {loading && (
          <Message role="bot" text="Searching the policy library…" />
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
            aria-label="Ask about a university policy"
          />
          <button className="composer__send" onClick={handleSend} disabled={loading}>
            Send
          </button>
        </div>
      </div>
    </div>
  );
}
