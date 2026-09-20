---
name: session-ledger-builder
description: "Recover and deduplicate repository-linked session provenance across explicitly named accessible harness stores and machines."
---

# Session Ledger Builder

1. Read the previous commit timestamp, target repository/worktrees, and the requested time window. Inventory explicitly available harness stores and named machines; do not search credential stores or presume every machine is accessible.

2. For local JSON/JSONL stores run `python3 .agent/shared/tools/session_ledger.py --repo REPO --since ISO --until ISO --source HARNESS=PATH`, repeating source arguments. The adapter supports common role/content, message, session_meta/payload, cwd and timestamp fields; list unsupported formats as gaps.

3. Use provider session tools or authorized remote reads for stores outside the adapter. Convert only necessary visible messages to an ignored runtime transcript; exclude hidden reasoning and credentials. Match repository/worktree metadata and time overlap before using a session.

4. Deduplicate mirrored visible conversations using the ledger message digest, then inspect inherited transcripts for overlapping ranges. Preserve source checksums and original provenance references; do not merge unrelated sessions merely because they share a model.

5. Store the ledger under `.agent-runtime/commit/`. Report inaccessible stores, uncertain timestamps, unrecognized formats and coverage bounds. A zero-entry ledger is incomplete evidence, not proof that no agent work occurred.
