# Changelog

## 0.3.0 — 2026-09-21

- Add `manuscript-acceptance-cycle` (scope, frozen candidates, three independent
  reviewers with exact-ACCEPT counting, Foster editorial cycles, fresh re-review,
  delivery) and its review-and-deliver route. Catalog grows to 35 skills.
- Make companion-site Pages deployment a bootstrap standard: every scaffolded
  repository installs `pages.yml` pinned to the same released revision as the
  submodule; the owner still enables Pages with build type "GitHub Actions".
- Apply the standing licensing policy in the core: Apache-2.0 for code, CC BY 4.0
  for manuscripts, with `LICENSES.md` and `licenses/CC-BY-4.0.txt`.
- Container and local verification only: 24 tests pass, including routing, silent
  shadowing rejection, manuscript freeze and rename/case guards, site/link/source
  packaging, held-out prose, and session-ledger coverage. No manuscript build or
  scientific simulation is run by this release.
- Consumer adoption still requires a separate tested pin update in each paper.

## 0.2.0 — 2026-09-19

- Add 18 program, review, provenance, traceability and publication skills.
- Add a project manifest schema and standard-library conformance, read-only audit,
  manuscript-freeze, companion-site/link and immutable-source-package helpers.
- Add explicit-source session ledgers with deduplication and coverage limits,
  read-only editorial triage, and infrastructure-only paper scaffolding.
- Inherit shared routes when no local explicit route matches. Local overrides
  retain authority; consumer profiles do not need copied shared routes.
- Add immutable-action reusable workflows for conformance/process logs, sites,
  release packages and explicitly authorized manuscript builds. Frozen manifests
  prohibit manuscript builds; this release did not compile any paper.
- Test source protection, rename/case guards, schema/pin/path failures, source
  packages, held-out prose and synthetic session/commit windows.

Consumer adoption requires a separate tested pin update. Infrastructure evidence
is not scientific validation; hosted environment and licensing decisions remain
project-local and cannot be inferred from a core release.
