// policyApi.js
// Single place for all calls to the RAG/chatbot backend.
// Response shape follows the team's agreed mock schema (PCOIS2-31, Alina):
//   { status, question, answer, citations[], confidence, escalation_required, escalation_message }
// where each citation = { policy_title, section, source_url }.

const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

// Sample responses matching the three documented cases, used while the
// backend is not yet connected. Cycles through them so the UI can be seen
// handling success, low-confidence and out-of-scope states.
const MOCKS = [
  {
    status: "success",
    question: "What are the rules for academic dress at La Trobe University?",
    answer:
      "Academic dress must be worn as prescribed for the relevant award and ceremony, according to the University's Academic Dress Policy.",
    citations: [
      {
        policy_title: "Academic Dress Policy",
        section: "Part E — Specific Academic Dress Requirements",
        source_url: "https://policies.latrobe.edu.au/document/view.php?id=208&version=4",
      },
    ],
    confidence: "high",
    escalation_required: false,
    escalation_message: "",
  },
  {
    status: "low_confidence",
    question: "Can I receive a special exemption from the academic dress requirements?",
    answer:
      "The available policy information does not provide enough detail to confirm whether you are eligible for an exemption.",
    citations: [
      {
        policy_title: "Academic Dress Policy",
        section: "Part E — Specific Academic Dress Requirements",
        source_url: "https://policies.latrobe.edu.au/document/view.php?id=208&version=4",
      },
    ],
    confidence: "low",
    escalation_required: true,
    escalation_message:
      "Please check the complete Academic Dress Policy or contact the appropriate University area for confirmation.",
  },
  {
    status: "out_of_scope",
    question: "What food is available at the campus café today?",
    answer:
      "I could not find relevant information in the available La Trobe University policy documents.",
    citations: [],
    confidence: "low",
    escalation_required: true,
    escalation_message:
      "Please rephrase your question or visit the official La Trobe University website for further assistance.",
  },
];

let mockIndex = 0;

/**
 * Send a user's question to the backend and get a schema-shaped response back.
 *
 * NOTE: Backend not built yet — this returns mocked responses matching the
 * agreed schema, cycling through success / low-confidence / out-of-scope so
 * the UI can be tested against all three. When the backend is ready, remove
 * the mock block and uncomment the real fetch.
 */
export async function askPolicyQuestion(question) {
  // --- MOCK (remove once backend is ready) ---
  await new Promise((r) => setTimeout(r, 600));
  const res = { ...MOCKS[mockIndex % MOCKS.length], question };
  mockIndex += 1;
  return res;
  // --- END MOCK ---

  /* Real version for when the backend is ready:
  const res = await fetch(`${API_BASE}/ask`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question }),
  });
  if (!res.ok) throw new Error("Failed to reach the policy service.");
  return res.json();
  */
}
