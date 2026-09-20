---
name: submission-release-orchestrator
description: "Audit submission and reproducibility artifacts, package immutable source/checksums, and publish only the authorized release scope."
---

# Submission Release Orchestrator

1. Read local submission instructions, manifest, current release scope and manuscript freeze. Separate an infrastructure prerelease from a scientific/manuscript submission; do not fabricate authorship, declarations or journal state.

2. Inventory required journal artifacts, CRediT/authorship, declarations, AI-use statement, data/code availability, cover letter and highlights. Frozen or missing manuscript artifacts remain open audit items, never silently generated.

3. For an infrastructure source package run `python3 .agent/shared/tools/research_project.py package --output .agent-runtime/release`. It packages committed HEAD plus the pinned shared core, Git bundle, provenance and SHA256SUMS; uncommitted paper changes are excluded and recorded.

4. Verify archive contents, bundle integrity, checksums and clean-clone setup. Confirm licenses for each artifact class and exclude raw transcripts, credentials and runtime caches. Record image digest and site/environment verification separately.

5. Create the authorized tag/release and upload only reviewed assets. Fetch uploaded assets, verify checksums and authoritative links, then record release identifiers. Do not describe infrastructure-only packaging as a submitted or validated paper.
