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

Submodule updates are explicit paper commits. A core release never changes a
paper until that paper advances its pinned commit and passes its own checks.
