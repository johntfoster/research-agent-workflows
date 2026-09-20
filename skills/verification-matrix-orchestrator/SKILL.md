---
name: verification-matrix-orchestrator
description: "Maintain and execute distinct implementation, analytical, convergence, finite-deformation and physical-validation gates."
---

# Verification Matrix Orchestrator

1. Read local verification instructions and matrix. Check active run locks and immutable/protected decks before edits or runs; identify authorized test commands and required environment.

2. Classify every gate as infrastructure, implementation, analytical, convergence, finite-deformation discrimination, or physical validation. Record equation/reduction, input, reference, tolerance, cost and expected observables.

3. Run the smallest relevant authorized gate with source/toolchain/input revisions, command, exit code and outputs. Separate current evidence from historical records and preserve failed results.

4. Update status from actual results only. A skipped, prescribed-field, material-only or surrogate run cannot satisfy a coupled gate. Do not tune or weaken required tests to obtain a pass.

5. Report category-specific acceptance, failures, exclusions and the next discriminating check. A green tooling/site run does not change scientific verification status.
