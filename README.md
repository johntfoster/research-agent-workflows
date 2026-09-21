# Research Agent Workflows

Versioned, project-neutral agent skills for John T. Foster's research-paper
repositories. Each paper remains an independent Git repository and consumes
this repository at `.agent/shared` as a pinned submodule.

## Consumer contract

- Open the paper repository—not a portfolio superproject—as the VS Code root.
- Keep paper-specific authority in the paper's root `AGENTS.md`.
- Configure routing and repository-specific checks in `agent-profile.json`.
- Keep incubating paper-specific skills in `agent_local/skills/`.
- Link `tools/agentctl` to `../.agent/shared/tools/agentctl`.

Initialize a fresh clone with:

```sh
git submodule update --init --recursive
tools/agentctl check
```

Activate only routed skills for a harness, for example:

```sh
tools/agentctl route "audit the derivation"
tools/agentctl activate codex "audit the derivation"
```

Install an exact working set instead of a task route by naming skills or
profiles directly. Repeat the flags to build a set:

```sh
tools/agentctl activate copilot --skill commit --profile manuscript --profile research
```

`--skill` installs one exact catalog name; `--profile` installs every skill
matching that profile's declared globs. Unknown names fail instead of
installing nothing, so a typo cannot silently produce an empty harness.

Submodule updates are explicit paper commits. A core release never changes a
paper until that paper advances its pinned commit and passes its own checks.

## Research infrastructure (v0.2)

`research-project.yml` uses the JSON subset of YAML and follows
`config/research-project.schema.json`. Runtime commands need only Python 3.10+:

```sh
python3 .agent/shared/tools/research_project.py check
python3 .agent/shared/tools/research_project.py site
python3 .agent/shared/tools/research_project.py links .agent-runtime/site
python3 .agent/shared/tools/research_project.py package
```

The core contains 18 additional coordination, review, traceability, verification,
publication and provenance skills. Read-only review and session-ledger helpers
provide triage and coverage evidence, not invented reasoning or scientific proof.
See `templates/README.md` for hooks and reusable workflows. Manuscript builds are
explicit, disabled by default, and rejected while a manifest is frozen.

Run `python3 -m pip install -r requirements-test.txt` then
`python3 -m unittest discover -s tests -v` before releasing a core revision.
Consumer repositories advance pins only through separate tested commits.
