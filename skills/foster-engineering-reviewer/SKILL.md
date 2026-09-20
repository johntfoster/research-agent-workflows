---
name: foster-engineering-reviewer
description: "Review engineering exposition, derivations and narrative against the author profile; produce a memo or explicitly authorized bounded edits."
---

# Foster Engineering Reviewer

1. Read local AGENTS, the author style profile, manuscript root and macros for the requested passage. Inspect maintenance policy first; frozen manuscripts permit a review memo only.

2. Run `python3 .agent/shared/tools/review_scan.py SOURCE` for read-only triage. Treat flags as candidates, not editorial or mathematical verdicts. Use foster-technical-prose and manuscript-narrative-review for contextual assessment.

3. For each passage check physical issue and engineering consequence first; purpose → equation → definitions → implication → limiting case; just-in-time symbols; necessary notation; explicit non-obvious derivations; and logical support for every therefore.

4. Check positive contribution statements, evidence and scope, ordinary engineering language, and explanation of implementation-specific vocabulary. Distinguish assumptions, choices, derived results and validation. Use equation-integrity and citation skills for technical claims; do not equate fluent prose with correct theory.

5. Produce a memo with source locations, issue, rationale, priority and a proposed revision or missing evidence. Edit only separately authorized unfrozen spans; preserve equations, labels, citations and claims unless the task explicitly changes them.

6. Compare pre/post sources or hashes. In review-only mode require byte-identical sources. For authorized edits run the local manuscript validation/build and inspect affected output; record unperformed checks rather than declaring editorial completion.
