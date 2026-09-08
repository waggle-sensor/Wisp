#!/usr/bin/env python3
"""Stage 2b - Summarise the shipped baseline profile so miners can judge novelty.

An episode is only worth mining if the baseline does *not* already answer it.
v1 checked this with bag-of-words overlap, which over-credited the control
whenever a keyword happened to appear anywhere in a 1.6MB skill tree (its own
stated limitation). Here we instead hand the miner a readable map of what the
baseline covers - every reference file with its title and lead paragraph - so
the novelty judgement is semantic and auditable.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def summarize(path: Path, lead_chars: int = 320) -> dict:
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = [l.rstrip() for l in text.splitlines()]
    title = next((l.lstrip("# ").strip() for l in lines if l.startswith("#")), path.stem)
    body = "\n".join(l for l in lines if l.strip() and not l.startswith("#"))
    # headings double as a topic list and are cheap to scan
    heads = [l.lstrip("# ").strip() for l in lines if re.match(r"^#{2,3} ", l)]
    return {
        "file": str(path.relative_to(path.parents[2])),
        "title": title,
        "lead": body[:lead_chars].replace("\n", " "),
        "headings": heads[:14],
        "chars": len(text),
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--profile", required=True, help="hermes-profile dir")
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    profile = Path(args.profile)
    entries = []
    for p in sorted((profile / "skills" / "sage-waggle").rglob("*.md")):
        entries.append(summarize(p))
    for name in ("SOUL.md", "AGENTS.md"):
        if (profile / name).exists():
            entries.append(summarize(profile / name))

    out = Path(args.out)
    out.write_text(json.dumps(entries, indent=2), encoding="utf-8")

    md = ["# Baseline coverage map (sage-waggle + SOUL/AGENTS)", ""]
    for e in entries:
        md.append(f"## {e['file']}\n**{e['title']}** — {e['lead']}")
        if e["headings"]:
            md.append(f"Sections: {'; '.join(e['headings'])}")
        md.append("")
    out.with_suffix(".md").write_text("\n".join(md), encoding="utf-8")
    print(f"files: {len(entries)}  map chars: {out.with_suffix('.md').stat().st_size}")


if __name__ == "__main__":
    main()
