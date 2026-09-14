# Shared research-agent policy

This directory is a version-pinned workflow dependency. The enclosing paper
repository is the primary context and owns all scientific authority.

1. Read the enclosing repository's root `AGENTS.md` first.
2. Treat local instructions, theory files, notation, validation records, and
   provenance as authoritative for that paper.
3. Use `tools/agentctl route "<task>"` to select the smallest relevant shared or
   paper-local skill. Read a skill only when its route applies.
4. Resolve manuscript roots, build recipes, and implementation paths from the
   paper's `agent-profile.json` and local instructions.
5. Do not inspect a sibling repository unless the user explicitly requests it
   or `research-dependencies.yml` declares an exact, commit-pinned dependency
   needed for the task.
6. A project-local instruction overrides a shared default. A local skill may
   extend the core but must use a distinct name; silent shadowing is rejected.
7. Generated environments, harness copies, caches, and run output belong under
   ignored runtime paths, normally `.agent-runtime/`.
