---
name: latex-equation-integrity-checker
description: Resolve and validate rendered LaTeX equation references before answering or editing. Use when the user cites equation numbers, bare numbers in manuscript context, labels, boxed displays, stale numbering, aux-file conflicts, overfull display fixes, or asks to inspect, explain, box, remove, or revise a numbered equation.
---

# LaTeX Equation Integrity Checker

Use this skill before relying on rendered equation numbers.

## Workflow

1. Read `AGENTS.md` and resolve the manuscript root, macro files, and build
   directory from local instructions or `agent-profile.json`.
2. Prefer the root manuscript's fresh `.aux` file over section-local artifacts.
3. Use the shared resolver when available:

```bash
python3 .agent/shared/skills/latex-equation-resolver/scripts/resolve_equation.py "<number>" .
```

4. Open the resolved source span and confirm:
   - label
   - rendered number
   - environment type
   - locked-region status
   - nearby references
   - display width or style risks
5. If aux files disagree, rebuild the declared root before selecting authority.
6. After label-sensitive or display-sensitive edits, compile the declared root
   as many times as the repository recipe requires.

## Report

Report the resolved label, source location, and any integrity risks. If editing,
make the narrowest source change and then re-check the affected label/display.
