# Consumer infrastructure

Use templates/hooks with a pinned shared submodule. The pre-commit entry point
enforces manuscript protection without generating disclosures; local hooks may
retain their legacy behavior outside explicitly frozen maintenance.

Reusable workflows under .github/workflows cover conformance and commit logs,
site build/link/deploy, immutable source packaging, and an explicit manuscript
build. Pin workflow references to the same released commit as the submodule.
The manuscript workflow is disabled by default and also rejects frozen manifests.
It is provided for future authorized work, not executed by this migration.
