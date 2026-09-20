---
name: commit-process-synthesizer
description: "Synthesize a six-section sanitized development narrative from repository changes, session provenance and actual verification."
---

# Commit Process Synthesizer

1. Read local commit rules and the commit skill. Resolve the previous commit window, scoped diff, current tests, and session ledger before drafting; preserve unrelated dirty work.

2. Build a decision/evidence outline from recoverable visible sessions. Distinguish checks run now from historical reports. Identify unavailable reasoning explicitly; neither a diff nor a ledger hash supplies missing rationale.

3. Write Summary, What changed & why, Alternatives considered, Dead ends & backtracks, Open questions, and Next steps. Include actual AI model(s) and sanitized AI session(s) fields in Summary. Draft the header last.

4. Run `python3 .agent/shared/tools/validate_process_log.py MESSAGE_FILE`. This checks structure and provenance fields, not whether the narrative is true. Compare each factual claim to the diff or evidence and redact secrets and private transcript content.

5. If commit creation is authorized, use the commit skill with explicit path-scoped staging and manuscript-freeze enforcement. Inspect the resulting commit and remaining dirty state. A request for a narrative alone does not authorize a commit or push.
