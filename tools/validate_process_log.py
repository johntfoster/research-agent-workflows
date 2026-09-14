#!/usr/bin/env python3
"""Validate the six-section process log and AI provenance in a commit message."""

from __future__ import annotations

import argparse
from pathlib import Path
import re


SECTIONS = (
    "Summary",
    "What changed & why",
    "Alternatives considered",
    "Dead ends & backtracks",
    "Open questions",
    "Next steps",
)
HEADING = re.compile(r"^(?:##\s+)?(" + "|".join(re.escape(item) for item in SECTIONS) + r")\s*$")
FIELDS = {
    field: re.compile(r"^" + re.escape(field) + r"\s*:\s*(.+?)\s*$", re.IGNORECASE)
    for field in ("AI model(s)", "AI session(s)")
}
UNRECORDED = {"unknown", "unavailable", "not recorded", "n/a", "none", "todo", "tbd"}


def validate(message: str) -> list[str]:
    lines = message.splitlines()
    if not lines or not lines[0].strip():
        return ["commit subject is empty"]
    found = []
    for index, line in enumerate(lines[1:], start=1):
        if match := HEADING.match(line.strip()):
            found.append((match.group(1), index))
    errors = []
    names = [name for name, _ in found]
    for section in SECTIONS:
        if names.count(section) != 1:
            errors.append(f"section must appear exactly once: {section}")
    if names != list(SECTIONS):
        errors.append("sections must appear in the required order")
        return errors
    for position, (name, start) in enumerate(found):
        end = found[position + 1][1] if position + 1 < len(found) else len(lines)
        content = [line.strip() for line in lines[start + 1 : end] if line.strip()]
        if not content:
            errors.append(f"empty section: {name}")
        if name == "Summary":
            for field, pattern in FIELDS.items():
                values = [match.group(1) for line in content if (match := pattern.match(line))]
                if len(values) != 1 or values[0].casefold() in UNRECORDED:
                    errors.append(f"Summary needs one recorded {field} field")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("message_file", type=Path)
    args = parser.parse_args()
    errors = validate(args.message_file.read_text(encoding="utf-8"))
    for error in errors:
        print(error)
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
