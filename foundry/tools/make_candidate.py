#!/usr/bin/env python3
"""Stage 5 - Scaffold a candidate bundle with full provenance.

Mirrors the v1 candidate layout (candidate.yaml / PROVENANCE.json / evidence /
proposed / RESULTS / REVIEW) so the two passes are directly comparable and a
reviewer can diff them. Provenance is not optional: every promoted claim must
name the students, episodes and verbatim quotes it came from, so a reviewer can
walk back from a shipped line of profile text to the conversation that produced it.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--id", required=True, help="e.g. HV2-0001")
    ap.add_argument("--root", required=True)
    ap.add_argument("--clusters", required=True, help="corroborated.json")
    ap.add_argument("--cluster-ids", required=True, help="comma-separated C001,C004")
    ap.add_argument("--title", required=True)
    ap.add_argument("--placement", required=True)
    ap.add_argument("--action", default="add", choices=["add", "modify", "hold", "reject"])
    args = ap.parse_args()

    data = json.loads(Path(args.clusters).read_text())
    wanted = set(args.cluster_ids.split(","))
    picked = [c for c in data["clusters"] if c["cluster_id"] in wanted]
    if not picked:
        raise SystemExit(f"no clusters matched {wanted}")

    root = Path(args.root) / args.id
    (root / "evidence").mkdir(parents=True, exist_ok=True)
    (root / "proposed").mkdir(exist_ok=True)

    students = sorted({s for c in picked for s in c["students"]})
    episodes = sorted({e for c in picked for e in c["episodes"]})

    (root / "candidate.yaml").write_text(
        f"""id: {args.id}
title: "{args.title}"
action: {args.action}
placement: "{args.placement}"
status: proposed
source_pass: foundry-v2
baseline: sage 1.2.0
clusters: [{', '.join(sorted(wanted))}]
independence: {len(students)}
students: [{', '.join(students)}]
episodes_n: {len(episodes)}
claims:
""" + "".join(f"  - {c['claim']}\n" for c in picked), encoding="utf-8")

    (root / "PROVENANCE.json").write_text(json.dumps({
        "id": args.id,
        "pass": "foundry-v2",
        "method": "transcript episode mining -> LLM triage vs baseline coverage map "
                  "-> cross-student corroboration -> retrieval A/B",
        "baseline": "summer-camp-2026 hermes-profile 1.2.0",
        "clusters": picked,
        "students": students,
        "episodes": episodes,
    }, indent=2), encoding="utf-8")

    lines = [f"# {args.id} — evidence", ""]
    for c in picked:
        lines += [f"## {c['cluster_id']} — {c['claim']}", "",
                  f"- kind: {c['kind']}  |  independence: {c['independence']}"
                  f"  |  confidence: {c['confidence']}",
                  f"- novelty: {c['why_novel']}",
                  f"- baseline files checked: {', '.join(c['baseline_files_checked']) or 'n/a'}",
                  ""]
        for ev in c["evidence"]:
            fr = ev["friction"]
            lines += [f"### {ev['student']} — `{ev['episode_id']}`",
                      f"friction: retry_depth={fr['retry_depth']} "
                      f"failures={fr['n_tool_failures']} "
                      f"wall={fr['wall_seconds']}s resolved={fr['resolved']}", "",
                      "> " + (ev["quote"] or "").replace("\n", "\n> "), ""]
    (root / "evidence" / "excerpts.md").write_text("\n".join(lines), encoding="utf-8")

    print(f"scaffolded {root} ({len(picked)} clusters, {len(students)} students)")


if __name__ == "__main__":
    main()
