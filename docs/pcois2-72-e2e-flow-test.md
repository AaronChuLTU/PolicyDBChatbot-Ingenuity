# End-to-End User Flow Test (PCOIS2-72)

**Date:** 19 Sep 2026
**Environment:** Deployed demo (frontend + backend via Cloudflare Tunnel, see root README's "Demo Hosting" section)

## Scope

Tested the complete flow from entering a question in the chat interface through to receiving the backend answer/citations, covering three required scenarios plus a recovery check.

## Results

| # | Scenario | Question asked | Result | Status |
|---|----------|----------------|--------|--------|
| 1 | Relevant policy question | "What am I allowed to wear to University?" | Real grounded answer returned with 5 citations from Academic Dress Policy and related sections | ✅ Pass |
| 2 | Escalation question | "What's the weather today?" | Correctly returned low-confidence escalation message with ASK La Trobe / policy@latrobe.edu.au contact routing, rather than a fabricated answer | ✅ Pass |
| 3 | API failure | (backend process stopped) | Frontend displayed a clear error banner ("Couldn't reach the policy service...") with a "Try again" button — no crash, no blank screen | ✅ Pass |
| 4 | Recovery after failure | "What are the rules on source materials?" (backend restarted) | Real grounded answer returned, citing Research Clinical Trials Policy — Part C, confirming the app recovers cleanly without a full page reload | ✅ Pass |

## Integration problems found

None. All four scenarios behaved as expected — the frontend/backend integration correctly handles the happy path, the escalation path, and backend unavailability without any unhandled errors.

## Notes

- Test 4 also served as corpus-coverage confirmation: the answer came from a different policy area (research conduct) than Test 1 (academic dress), showing retrieval isn't just working for one narrowly-tested topic.
- This test run doubled as additional verification for PCOIS2-74, since it was run against the actual tunneled demo URL rather than localhost.