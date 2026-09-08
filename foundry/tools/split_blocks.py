"""Stage 6a - Parse `## Pitfalls` out of sage-waggle/SKILL.md into atomic blocks.

Input for split_pitfalls.py (Stage 6b). Each top-level `- **Label**: ...` bullet
plus its continuation lines becomes one record, in document order; the index of a
record here is the index split_groups.py assigns to a group.

Deterministic and offline. Reproduces the 85 blocks of the 1.3.0 release
byte-for-byte:

    git -C . show \
        hermes-profile-1.3.0-release:skills/sage-waggle/SKILL.md \
        > /tmp/skill_130.md
    python3 foundry/tools/split_blocks.py \
        --skill /tmp/skill_130.md --out foundry/.work/split/blocks.json
"""

import argparse
import json
import re
from pathlib import Path

START = "## Pitfalls"
END_PREFIX = "## ECR Readiness"


def parse_blocks(text):
    lines = text.split("\n")
    try:
        a = lines.index(START)
    except ValueError:
        raise SystemExit(f"no {START!r} section in the given SKILL.md")
    b = next(
        (i for i, l in enumerate(lines) if i > a and l.startswith(END_PREFIX)),
        len(lines),
    )

    blocks, cur = [], None
    for line in lines[a + 1 : b]:
        if line.startswith("- "):
            if cur is not None:
                blocks.append(cur)
            cur = [line]
        elif cur is not None:
            cur.append(line)
    if cur is not None:
        blocks.append(cur)

    recs = []
    for bl in blocks:
        while bl and not bl[-1].strip():
            bl.pop()
        body = "\n".join(bl)
        m = re.match(r"- \*\*(.+?)\*\*", bl[0])
        recs.append(
            {
                "first": bl[0],
                "label": m.group(1) if m else None,
                "len": len(body),
                "nlines": len(bl),
                "text": body,
            }
        )
    return recs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skill", required=True, help="path to sage-waggle/SKILL.md")
    ap.add_argument("--out", required=True, help="where to write blocks.json")
    args = ap.parse_args()

    recs = parse_blocks(Path(args.skill).read_text(encoding="utf-8"))
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(recs, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{len(recs)} blocks -> {out}")


if __name__ == "__main__":
    main()
