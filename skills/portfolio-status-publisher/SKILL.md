---
name: portfolio-status-publisher
description: "Generate a program dashboard from project manifests and observed CI/site/environment/release evidence without editing papers."
---

# Portfolio Status Publisher

1. Read the portfolio registry and archived-project inventory. Choose committed snapshots or explicitly authorized live checkouts and identify observation dates.

2. Run the program audit; retain missing/error states. Gather current remote checks only through read-only service calls and associate results with exact commits or deployment identities.

3. Build the dashboard through `python3 tools/portfolio.py build --output .agent-runtime/site` in the program repository. Show authority links, status, workflow pin, latest observed checks, blocker and next milestone.

4. Check internal and external links and ensure unknown/unrun scientific checks remain distinct from infrastructure passes. Do not expose local absolute paths, private transcripts or confidential submission data in public output.

5. Deploy only the authorized program site and verify its live content. Record observed timestamps and limitations; do not mutate paper manifests as a side effect of publishing a portfolio view.
