---
name: research-chief-of-staff
description: "Review portfolio priorities, blockers, stale evidence, deadlines and dependency drift across explicitly registered research projects."
---

# Research Chief Of Staff

1. Read the program registry, workstream acceptance gates, decisions, and selected project manifests. Limit inspection to the registered projects requested by the user; finish with an explicit scope list.

2. Run the program repository's `python3 tools/portfolio.py audit`, supplying `--root` only for an authorized local paper parent. Separate snapshot evidence from live observations and retain missing-checkout errors.

3. Rank next actions by an explicit deadline or dependency, then the user's priority. Report unknown deadlines as unknown. Identify workflow-pin drift without advancing any paper pin.

4. Write a concise coordination report with owner, evidence, blocker, next action, and acceptance gate for each workstream. Update only program-owned priorities when authorized; never change paper authority from a portfolio command.

5. Check that every status can be traced to a manifest, audit observation, or dated decision. Return the smallest executable next task without claiming unrun scientific checks.
