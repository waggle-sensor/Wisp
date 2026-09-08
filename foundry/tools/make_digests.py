#!/usr/bin/env python3
"""Stage 2a - Build compact per-episode digests for LLM triage.

Full episodes total ~6.6M chars, too much to read deeply everywhere. But the
v1 pass failed precisely because it narrowed with a *keyword* list, which can
only find gaps someone already thought of. So we narrow semantically instead:
a cheap LLM reads a digest of every episode and decides whether it is worth a
deep read. Nothing is excluded by topic in advance.

A digest keeps the parts that reveal what an episode is about and how hard it
was, at ~1-2k chars: the opening ask, the user's later turns (where course
corrections live), the tools used, and the head of each failing tool result.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

USER = re.compile(r"^### USER\n", re.MULTILINE)


def digest(body: str, meta: dict, max_chars: int = 2200) -> str:
    blocks = re.split(r"^(?=### (?:USER|ASSISTANT|TOOL))", body, flags=re.MULTILINE)
    users, failing = [], []
    for b in blocks:
        if b.startswith("### USER"):
            users.append(b[len("### USER\n"):].strip())
        elif b.startswith("### TOOL") and "[FAILED]" in b.split("\n", 1)[0]:
            head, _, rest = b.partition("\n")
            tool = head.replace("### TOOL ", "").replace(" [FAILED]", "")
            failing.append(f"[{tool}] {rest.strip()[:300]}")

    parts = [
        f"EPISODE {meta['episode_id']}",
        f"student={meta['student']} turns={meta['n_turns']} tools={meta['n_tool_calls']} "
        f"failures={meta['n_tool_failures']} retry_depth={meta['retry_depth']} "
        f"resolved={meta['resolved']} wall_s={meta['wall_seconds']}",
        "USER TURNS:",
    ]
    budget = max_chars - sum(len(p) for p in parts)
    per_user = max(200, budget // 2 // max(len(users), 1))
    for u in users[:8]:
        parts.append(f"- {u[:per_user]}")
    if failing:
        parts.append("FAILING TOOL RESULTS (head):")
        per_fail = max(150, budget // 2 // len(failing[:6]))
        for f in failing[:6]:
            parts.append(f"- {f[:per_fail]}")
    return "\n".join(parts)[:max_chars]


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--corpus", required=True)
    ap.add_argument("--batch-size", type=int, default=28)
    args = ap.parse_args()

    corpus = Path(args.corpus)
    index = json.loads((corpus / "episode_index.json").read_text())
    outdir = corpus / "digests"
    outdir.mkdir(exist_ok=True)

    # Hard episodes first so an interrupted run still covers the richest ones,
    # but every episode gets into some batch: no topic gate at this stage.
    index.sort(key=lambda e: (-e["retry_depth"], -e["n_tool_failures"], -e["n_tool_calls"]))

    batches = [index[i:i + args.batch_size] for i in range(0, len(index), args.batch_size)]
    for i, batch in enumerate(batches):
        text = "\n\n---\n\n".join(
            digest((corpus / "episodes" / f"{e['episode_id']}.md").read_text(errors="replace"), e)
            for e in batch
        )
        (outdir / f"batch_{i:02d}.txt").write_text(text, encoding="utf-8")
    print(f"batches: {len(batches)}  episodes: {len(index)}")
    print(f"avg batch chars: {sum((outdir / p.name).stat().st_size for p in outdir.iterdir()) // len(batches)}")


if __name__ == "__main__":
    main()
