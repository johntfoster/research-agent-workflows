---
name: research-dependency-manager
description: "Audit or explicitly advance immutable shared-workflow and scientific dependency pins with consumer-specific checks."
---

# Research Dependency Manager

1. Read local AGENTS, research-project.yml, research-dependencies.yml when present, .gitmodules and current status. Identify each dependency source and exact revision; preserve dirty submodule work.

2. Confirm remote reachability and intended release compatibility. Review the changed core/schema/hooks against consumer overrides before fetching or changing a pin.

3. Advance only explicitly requested consumer pins, one paper at a time. Update its manifest and Git gitlink together; never bulk-advance papers merely because a core release exists.

4. Run agentctl checks, manifest conformance, routing, hook and applicable consumer tests. Enforce manuscript freeze and verify user-owned source hashes; leave a failing consumer at its known-good pin or record a recoverable uncommitted candidate.

5. Commit the tested dependency advance separately with source/revision/evidence. Verify a clean clone can initialize the pin and report remote/source availability, not just a locally cached object.
