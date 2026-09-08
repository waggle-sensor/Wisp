#!/usr/bin/env python3
"""Redact common secret patterns in text files under a directory. Prints count of files changed."""
from __future__ import annotations

import re
import sys
from pathlib import Path

PATTERNS = [
    (re.compile(r"(?i)\bsk-[A-Za-z0-9_-]{20,}"), "[REDACTED]"),
    (re.compile(r"(?i)\bhf_[A-Za-z0-9]{20,}"), "[REDACTED]"),
    (re.compile(r"(?i)\bghp_[A-Za-z0-9]{20,}"), "[REDACTED]"),
    (re.compile(r"(?i)\bgho_[A-Za-z0-9]{20,}"), "[REDACTED]"),
    (re.compile(r"(?i)\bxox[baprs]-[A-Za-z0-9-]{10,}"), "[REDACTED]"),
    (re.compile(r"(?i)(Bearer\s+)[A-Za-z0-9._\-+/=]{16,}"), r"\1[REDACTED]"),
    (
        re.compile(
            r"(?i)((?:api[_-]?key|token|password|secret|authorization)\s*[:=]\s*[\"']?)([^\s\"']{12,})"
        ),
        r"\1[REDACTED]",
    ),
]

EXTS = {".md", ".txt", ".yaml", ".yml", ".json", ".log", ".csv", ".tsv", ".html", ".EXAMPLE"}
NAMES = {".env.EXAMPLE", ".hermes_history", ".skills_prompt_snapshot.json", ".gitignore", ".graphifyignore"}


def should_scan(path: Path) -> bool:
    if path.name in NAMES:
        return True
    if path.suffix in EXTS:
        return True
    if path.name.endswith(".EXAMPLE"):
        return True
    return False


def main() -> None:
    root = Path(sys.argv[1])
    changed = 0
    for path in root.rglob("*"):
        if not path.is_file() or not should_scan(path):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        new = text
        for pat, repl in PATTERNS:
            new = pat.sub(repl, new)
        if new != text:
            path.write_text(new, encoding="utf-8")
            changed += 1
    print(changed)


if __name__ == "__main__":
    main()
