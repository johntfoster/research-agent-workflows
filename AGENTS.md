# AGENTS.md

## Repository scope

This repository is the canonical, project-neutral agent workflow consumed by
research-paper repositories. It owns reusable skills, routing, schemas, tests,
and templates. It does not own any paper's theory, notation, data, conclusions,
verification status, or source-of-truth declarations.

## Development rules

- Keep every operational path repository-relative.
- A shared skill must work in more than one paper repository and must not name a
  particular manuscript, sibling checkout, equation set, or machine path.
- Put conditional detail in skill references and load it only when relevant.
- Test routing, activation, and all changed scripts before release.
- Preserve paper-local authority: consumer `AGENTS.md` files override shared
  defaults, and the shared core must never silently inspect sibling papers.
- Use structured process-log commit messages for ordinary commits.

## Release rules

- Use semantic version tags.
- Paper repositories consume an exact Git submodule commit.
- Never advance consumer pins automatically. Validate each paper before
  committing its submodule update.
