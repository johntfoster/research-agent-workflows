---
name: codespace-reproducer
description: "Pin and test clean-clone development containers and Codespaces, separating infrastructure startup from scientific reproduction."
---

# Codespace Reproducer

1. Read the existing devcontainer, toolchain lock and local reproduction instructions. Preserve paper-specific environment requirements and immutable source/framework pins.

2. Pin the base/prebuilt image by registry digest and record architecture. Confirm referenced source revisions and toolchain dependencies; a mutable latest tag is not a reproducible pin.

3. Build/start the container from a clean clone with submodules initialized. Run the smallest infrastructure smoke test, then separately authorized scientific tests; manuscript freeze forbids manuscript generation during this goal.

4. Test the hosted Codespace only within authorized service access. Record the created environment identity, image digest, command/results and cleanup; do not claim a local Docker test proves hosted Codespace startup.

5. Update reproduction evidence and authoritative launch links. Report unavailable architecture/service/scientific gates explicitly; distinguish configuration-valid, local-container-verified and hosted-verified.
