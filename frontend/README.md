# La Trobe Policy Assistant — Frontend

Sprint 2 deliverable: framework chosen, repo structured, and a basic page shell.

**Stack:** React + Vite (chat frontend that will call a separate RAG backend).

## Getting started

```bash
npm install
npm run dev
```

Then open the local URL Vite prints (usually http://localhost:5173).

## Project structure

```
src/
  api/         Backend calls live here (policyApi.js) — one place to change
  components/  Reusable UI pieces (Message.jsx)
  styles/      Design tokens (theme.css) + layout (app.css)
  App.jsx      The page shell: header, disclaimer, conversation, composer
  main.jsx     Entry point
```

## Backend connection

The backend isn't built yet, so `src/api/policyApi.js` returns **mock**
responses that follow the team's agreed schema (PCOIS2-31). It cycles through
success / low-confidence / out-of-scope so the UI can be tested against all
three. When the retrieval service is ready:
1. Set `VITE_API_BASE_URL` in a `.env` file (see `.env.example`).
2. In `policyApi.js`, remove the mock block and uncomment the real `fetch`.

### Response schema

The backend returns JSON of this shape:

```
{
  status: "success" | "out_of_scope" | "low_confidence" | "error",
  question: string,
  answer: string,
  citations: [ { policy_title, section, source_url } ],
  confidence: "high" | "medium" | "low",
  escalation_required: boolean,
  escalation_message: string
}
```

Display rules implemented in the UI:
- Always show the question and answer.
- Show citations only when the list is non-empty.
- Show a warning when confidence is "low".
- Show the escalation message when escalation_required is true.

## Notes for the team
- Keep all backend calls in `src/api/` — don't fetch directly from components.
- The disclaimer banner and source-citation UI reflect project must-haves
  (compliance notice + source citations) and should stay.
