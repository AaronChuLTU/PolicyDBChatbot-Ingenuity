import { useState, useEffect } from "react";
import "./InfoButton.css";

/**
 * InfoButton
 * -----------
 * Self-contained "home / info" button for the toolbar.
 * Place this file (and InfoButton.css) in: frontend/src/components/
 *
 * Usage in App.jsx:
 *   import InfoButton from "./components/InfoButton";
 *   ...
 *   <InfoButton />
 *
 * Edit ABOUT_CONTENT / FAQ_CONTENT below to change the copy.
 */

const ABOUT_CONTENT = [
  "Policy DB Chatbot helps La Trobe University students and staff find answers from the official Policy Database, without digging through PDFs.",
  "Ask a question in plain language and it searches the Policy Database directly, using retrieval-augmented generation (RAG) rather than guessing.",
  "Every answer links back to the specific policy it came from, so you can check the source yourself.",
  "Built as a capstone project by Team Ingenuity.",
];

const FAQ_CONTENT = [
  {
    q: "What can I ask?",
    a: "Anything covered by La Trobe's Policy Database — things like academic integrity, special consideration, grading, enrolment, and leave policies.",
  },
  {
    q: "How accurate are the answers?",
    a: "Answers are generated only from the Policy Database itself, and each one comes with a citation so you can verify it against the source policy.",
  },
  {
    q: "What happens if it can't find an answer?",
    a: "It will say so rather than guessing, and point you toward who to contact instead.",
  },
  {
    q: "Is my chat saved?",
    a: "No — there's no login or account system, so chats aren't saved to a profile. Once you refresh or start a new chat, that conversation is gone.",
  },
  {
    q: "How do I start a new conversation?",
    a: "Use the New Chat button in the toolbar — it clears the current conversation and starts fresh.",
  },
];

function CloseIcon(props) {
  return (
    <svg
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      {...props}
    >
      <path d="M6 6l12 12M18 6L6 18" />
    </svg>
  );
}

export default function InfoButton() {
  const [open, setOpen] = useState(false);
  const [tab, setTab] = useState("about"); // "about" | "faq"

  useEffect(() => {
    if (!open) return;
    const onKey = (e) => {
      if (e.key === "Escape") setOpen(false);
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [open]);

  return (
    <>
      {/* Reuses the site's own pill-button style so it matches
          "+ New chat" and "☀ Light" exactly, instead of a one-off look. */}
      <button
        type="button"
        onClick={() => setOpen(true)}
        aria-label="About and FAQ"
        title="About / FAQ"
        className="app-header__toggle"
      >
        ? About
      </button>

      {open && (
        <div
          className="info-modal-overlay"
          role="dialog"
          aria-modal="true"
          aria-labelledby="info-modal-title"
        >
          <div
            className="info-modal-overlay__backdrop"
            onClick={() => setOpen(false)}
          />

          <div className="info-modal">
            <div className="info-modal__header">
              <h2 id="info-modal-title" className="info-modal__title">
                Policy DB Chatbot
              </h2>
              <button
                type="button"
                onClick={() => setOpen(false)}
                aria-label="Close"
                className="info-modal__close"
              >
                <CloseIcon />
              </button>
            </div>

            <div className="info-modal__tabs">
              <button
                type="button"
                onClick={() => setTab("about")}
                className={
                  tab === "about"
                    ? "info-modal__tab info-modal__tab--active"
                    : "info-modal__tab"
                }
              >
                About
              </button>
              <button
                type="button"
                onClick={() => setTab("faq")}
                className={
                  tab === "faq"
                    ? "info-modal__tab info-modal__tab--active"
                    : "info-modal__tab"
                }
              >
                FAQ
              </button>
            </div>

            <div className="info-modal__content">
              {tab === "about" ? (
                <ul className="info-modal__about-list">
                  {ABOUT_CONTENT.map((line, i) => (
                    <li key={i} className="info-modal__about-item">
                      {line}
                    </li>
                  ))}
                </ul>
              ) : (
                <div className="info-modal__faq-list">
                  {FAQ_CONTENT.map((item, i) => (
                    <div key={i} className="info-modal__faq-item">
                      <p className="info-modal__faq-question">{item.q}</p>
                      <p className="info-modal__faq-answer">{item.a}</p>
                    </div>
                  ))}
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </>
  );
}
