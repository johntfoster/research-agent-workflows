---
name: manuscript-acceptance-cycle
description: "Review-and-deliver a manuscript: three independent reviewers until two exact ACCEPTs, three Foster review/edit cycles, fresh re-review, then deliver the PDF."
---

# Manuscript acceptance cycle

1. Fix the scope before touching anything: manuscript root, authorized edit scope, author style profile, build command, verification commands, delivery target, and the completion criterion (at least two of three independent reviewers returning exactly ACCEPT on one immutable snapshot). Label the exercise simulated AI peer review, not journal acceptance. Preserve pre-existing changes as a baseline.

2. Prepare a reproducible candidate. Run the numerical checks (for convergence or evidence-category labels, follow `verification-evidence-integrity`), rebuild the PDF, inspect figures and equation layout, and record commands and outcomes. Ship a versioned self-contained supplement with sources, parameters, dependency requirements, reproduction order, data, licenses and a payload-hash manifest when code or data are not released. Freeze manuscript, bibliography, code, data, figures, supplement and PDF with a SHA-256 manifest and a snapshot identifier in a new review-round directory, and write it read-only. Reviewers read immutable copies, never the working tree.

3. Launch three fresh independent reviewers on that snapshot with complementary emphasis: derivation and correctness; numerical verification and source fidelity; exposition, notation and claims. Require each to confirm the manifest digest equals the declared snapshot identifier, re-hash every listed file, report mismatches or missing files, use stable comment IDs with source locations, separate required changes from optional notes, and end with exactly one verdict: ACCEPT, MINOR REVISION, MAJOR REVISION, or REJECT. Reviewers write only their own reports and never edit the paper. Do not share other reports or acceptance counts.

4. Wait for all three reports and match each to the checkpoint's round and snapshot. Failures, missing reports, hash mismatches, or ambiguous verdicts make the round incomplete; recover the missing review without counting it as acceptance. Count only exact ACCEPT. Preserve every report unchanged. Before respawning a child that merely looks stalled, check its output paths for deliverables it may already have written, then reconcile both runs and keep one writer.

5. Build a response matrix for every substantive comment: evidence, disposition, source change or reasoned rebuttal, and verification. Resolve demonstrated correctness and reproducibility defects even when two reviewers already accept. Reconcile contradictory suggestions against equations, data and author instructions rather than vote totals, and retain rejected suggestions with their reasons.

6. Revise within scope, rerun affected checks and the full build, then freeze a new snapshot and repeat steps 3-5. A read-only snapshot blocks replacement, so restore write permission recursively before removing the old directory. Never carry acceptance across changed scientific content or combine votes from different rounds.

7. After an accepted round, run three Foster engineering and prose review-edit cycles using `foster-engineering-reviewer`, `foster-technical-prose`, and the local narrative-review skill. Each cycle produces a memo, a disposition, edits, a rebuild, and page-image inspection. Keep edits prose-only: no equation, symbol, label, citation, number, or claim may change. Prove it by comparing structural token counts and the digit-literal multiset before and after, and by confirming scientific paths are untouched. If one cycle's writer is still active, do not start a second writer in the same directory.

8. Re-review the revised tree. Run a fresh independent round on a new snapshot of the post-Foster content, because acceptance does not carry across the editorial edits. When the editorial cycles changed no source file, verify that the current sources are byte-identical to the accepted snapshot and that the built artifact matches its manifest; then the acceptance still applies and no further round is required.

9. Finish and deliver. Confirm no writer is active and the build is current against the frozen sources, verify site and artifact links, then send the actual artifact to the requested target. After sending, re-check the delivered file's digest against the current build and resend if the tree moved. Record the delivery receipt, or report unconfirmed delivery explicitly.

10. For a durable goal or watchers, keep a checkpoint with goal ID, phase, snapshot, reviewer run IDs, report paths, pending actions and automation IDs, and resume from it without duplicate writers or duplicate rounds. A checkpoint is not proof of completion. Mark the goal complete and remove watchers only after the acceptance, Foster, re-review, build and delivery gates are satisfied.
