#!/bin/sh
# Run from the repository root with an already reviewed staged change.
set -eu

if [ "$#" -ne 1 ]; then
  echo "usage: $0 MESSAGE_FILE (from the repository root)" >&2
  exit 2
fi

repository_root=$(git rev-parse --show-toplevel)
if [ "$(pwd -P)" != "$(cd "$repository_root" && pwd -P)" ]; then
  echo "run this helper from the repository root" >&2
  exit 2
fi

# Compatibility entry points in paper repositories are symlinks. Resolve the
# helper itself before locating core-owned validators so invocation through an
# old path is identical to invocation inside .agent/shared.
script_path=$(python3 -c 'import os, sys; print(os.path.realpath(sys.argv[1]))' "$0")
shared_root=$(CDPATH= cd -- "$(dirname -- "$script_path")/../../.." && pwd -P)
python3 "$shared_root/tools/validate_process_log.py" "$1"
if git diff --cached --quiet; then
  echo "no staged changes; stage the intended change before committing" >&2
  exit 1
fi
git diff --cached --check
if [ -d .githooks ]; then
  tools/agentctl hooks install
  for hook in prepare-commit-msg commit-msg; do
    if [ ! -x ".githooks/$hook" ]; then
      echo "missing executable hook: .githooks/$hook" >&2
      exit 1
    fi
  done
fi

git commit --file "$1"
