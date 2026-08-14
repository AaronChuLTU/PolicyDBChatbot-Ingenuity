// Message.jsx — renders a single chat message (user or bot).
// Bot messages follow the team's mock schema (PCOIS2-31): they may carry
// citations, a low-confidence warning, and an escalation message. Display
// logic follows Alina's frontend display rules.

export default function Message({ role, text, citations, confidence, escalation }) {
  const isUser = role === "user";

  if (isUser) {
    return (
      <div className="msg msg--user">
        <div>
          <div className="msg__bubble">{text}</div>
        </div>
      </div>
    );
  }

  const showLowConfidence = confidence === "low";
  const hasCitations = citations && citations.length > 0;

  return (
    <div className="msg msg--bot">
      <div>
        <div className="msg__bubble">{text}</div>

        {/* Low-confidence warning: tell the user to verify the answer */}
        {showLowConfidence && (
          <div className="msg__warning">
            ⚠ Low confidence — please verify this against the official policy.
          </div>
        )}

        {/* Citations: only shown when a policy source is present */}
        {hasCitations && (
          <div className="msg__sources">
            <p className="msg__sources-label">Sources</p>
            {citations.map((c, i) => (
              <div key={i}>
                <a className="msg__source-link" href={c.source_url} target="_blank" rel="noreferrer">
                  {c.policy_title}{c.section ? ` — ${c.section}` : ""}
                </a>
              </div>
            ))}
          </div>
        )}

        {/* Escalation: shown beneath the answer when escalation is required */}
        {escalation && (
          <div className="msg__escalation">
            {escalation}
          </div>
        )}
      </div>
    </div>
  );
}
