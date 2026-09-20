---
name: theory-code-traceability-auditor
description: "Audit residuals and material laws against exact paper equations and connect publication claims to implemented verification."
---

# Theory Code Traceability Auditor

1. Read local implementation authority, canonical theory roots and traceability maps. Limit source inspection to the authorized implementation and its declared dependencies.

2. For each kernel/material identify the exact equation label, reference configuration, measures, variables, assumptions and units. Derive the implemented weak form, including factors of J and boundary terms.

3. Check constitutive derivatives, nested/outer AD dependencies and density distinctions independently of residual assembly. Record orphan code, orphan equations and undocumented reductions.

4. For each publication claim name the implementation path and an actual test, including run provenance and acceptance criterion. Distinguish material-only checks from coupled solves and analytical comparison from physical validation.

5. Produce a read-only audit matrix and prioritized corrections. Run only explicitly in-scope smallest checks; never weaken tolerances or edit the theory to fit an implementation convenience.
