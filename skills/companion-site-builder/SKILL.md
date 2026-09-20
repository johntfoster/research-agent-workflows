---
name: companion-site-builder
description: "Build and verify a paper companion site from authoritative manifest links and recorded evidence, then deploy when authorized."
---

# Companion Site Builder

1. Read the project manifest and existing site/build workflow. Preserve established scientific content and assets; use existing builders when present.

2. For a metadata-driven site run `python3 .agent/shared/tools/research_project.py site --output .agent-runtime/site`. This writes generated infrastructure output only; it does not compile a manuscript or invent results.

3. Run `python3 .agent/shared/tools/research_project.py links .agent-runtime/site` and verify external source, citation, release and environment URLs. A launch link is not an embedded interaction or a tested Codespace.

4. Inspect the generated site for clear project authority, reproduction instructions and category-specific evidence. Label pending or unavailable checks; never add a reproducibility-success badge without its evidence.

5. Deploy through the authorized Pages workflow, inspect the workflow conclusion, fetch the deployed URL and verify representative links/assets. Record local build success separately if deployment is unavailable.
