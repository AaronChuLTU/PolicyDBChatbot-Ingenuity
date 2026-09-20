// Message.jsx — renders a single chat message (user or bot).
// Bot messages follow the team's mock schema (PCOIS2-31): they may carry
// citations, a low-confidence warning, and an escalation message. Display
// logic follows Alina's frontend display rules.

export default function Message({ role, text, citations, confidence, escalation }) {
  const isUser = role === "user";

  if (isUser) {
    return (
      <div className="msg msg--user">
        <div className="msg__bubble">{text}</div>
      </div>
    );
  }

  const showLowConfidence = confidence === "low";
  const hasCitations = citations && citations.length > 0;

  return (
    <div className="msg msg--bot">
      <div className="msg__avatar" aria-hidden="true">
        <svg viewBox="0 0 24 24" width="15" height="15" fill="none">
          <path
            d="M4 5.5C4 4.67 4.67 4 5.5 4h13c.83 0 1.5.67 1.5 1.5v9c0 .83-.67 1.5-1.5 1.5H9l-4 3.5V16H5.5C4.67 16 4 15.33 4 14.5v-9Z"
            fill="currentColor"
          />
        </svg>
      </div>
      <div className="msg__content">
        <div className="msg__bubble">{text}</div>

        {/* Low-confidence flag and citations share one compact tag row —
            matches the team's wireframe (Direction A) more closely than
            stacking each as its own full-width box. */}
        {(showLowConfidence || hasCitations) && (
          <div className="msg__tags">
            {showLowConfidence && (
              <span className="msg__tag msg__tag--warning">⚠ Low confidence</span>
            )}
            {hasCitations && (
              <>
                <span className="msg__tags-label">Sources</span>
                {citations.map((c, i) => (
                  <a
                    key={i}
                    className="msg__tag msg__tag--source"
                    href={c.source_url}
                    target="_blank"
                    rel="noreferrer"
                  >
                    {c.policy_title}{c.section ? ` — ${c.section}` : ""}
                  </a>
                ))}
              </>
            )}
          </div>
        )}

        {/* Escalation: shown beneath the answer when escalation is required.
            Kept as a full block, not a tag — it's a required instruction to
            act on, not a label, so it isn't safe to compact without hiding
            what it actually says. */}
        {escalation && (
          <div className="msg__escalation">
            {escalation}
          </div>
        )}
      </div>
    </div>
  );
}
