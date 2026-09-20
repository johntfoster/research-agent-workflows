---
name: equation-change-impact-planner
description: "Plan the propagation of a proposed equation, label or assumption change across a paper, implementation, tests and declared dependents."
---

# Equation Change Impact Planner

1. Read the canonical root/macros and exact target equation or assumption. Distinguish a proposed change from an already committed change; identify the user-authorized edit boundary.

2. Trace definitions, uses, cross-references, summary tables, constitutive derivatives, weak forms, code maps, test inputs, figures, website consumers and declared dependent papers. Record source locations and unresolved edges.

3. For each dependency state what must change, what must remain invariant, and which analytical or numerical check can discriminate the result. Preserve reference/current-volume and push-forward conventions.

4. Write a propagation checklist ordered by prerequisites with owner, acceptance evidence and manuscript-freeze constraints. A plan is not permission to apply all mapped changes.

5. Check that every known consumer has an explicit disposition and that proposed code changes map to source equations. Return untraced dependencies as open items, not silently omitted work.
