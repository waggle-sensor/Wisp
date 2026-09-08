#!/usr/bin/env python3
"""Stage 0/6 - Cohort and corpus statistics for the write-up.

Emits the descriptive numbers a paper/poster needs (and that v1 reported only
partially, because it never opened the transcripts): how much the cohort
actually talked to the agent, how much friction they hit, and how the mining
funnel narrowed. Pure counting - no judgement, no LLM.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sqlite3
from collections import Counter
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--brains", required=True)
    ap.add_argument("--archives", required=True)
    ap.add_argument("--episode-index", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    brains = Path(args.brains)
    episodes = json.loads(Path(args.episode_index).read_text())

    per_student = {}
    for d in sorted(brains.iterdir()):
        if not d.is_dir():
            continue
        name = d.name
        sage = d / "sage"
        row = {
            "student": name,
            "has_state_db": (sage / "state.db").exists(),
            "sessions": 0, "messages": 0, "user_messages": 0,
            "tool_calls": 0, "chars": 0, "models": [],
            "memory_bytes": 0, "agent_created_skills": [],
            "episodes": 0, "episodes_with_failures": 0, "resolved_arcs": 0,
        }
        db = sage / "state.db"
        if db.exists():
            c = sqlite3.connect(db)
            c.text_factory = lambda b: b.decode("utf-8", "replace")
            try:
                row["sessions"] = c.execute("select count(*) from sessions").fetchone()[0]
                row["messages"] = c.execute("select count(*) from messages").fetchone()[0]
                row["user_messages"] = c.execute(
                    "select count(*) from messages where role='user'").fetchone()[0]
                row["tool_calls"] = c.execute(
                    "select count(*) from messages where role='tool'").fetchone()[0]
                row["chars"] = c.execute(
                    "select coalesce(sum(length(content)),0) from messages").fetchone()[0]
                row["models"] = sorted({
                    m for (m,) in c.execute("select distinct model from sessions") if m})
            except sqlite3.Error:
                pass
        mem = sage / "memories" / "MEMORY.md"
        if mem.exists():
            row["memory_bytes"] = mem.stat().st_size
        usage = sage / "skills" / ".usage.json"
        if usage.exists():
            try:
                u = json.loads(usage.read_text())
                row["agent_created_skills"] = sorted(
                    k for k, v in u.items()
                    if isinstance(v, dict) and v.get("created_by") == "agent")
            except Exception:
                pass
        eps = [e for e in episodes if e["student"] == name]
        row["episodes"] = len(eps)
        row["episodes_with_failures"] = sum(1 for e in eps if e["n_tool_failures"])
        row["resolved_arcs"] = sum(1 for e in eps if e["resolved"])
        per_student[name] = row

    tarballs = {}
    for t in sorted(Path(args.archives).glob("*/*.tar.gz")):
        tarballs[t.parent.name] = {"file": t.name, "bytes": t.stat().st_size,
                                   "sha256": sha256(t)}

    totals = {
        "students": len(per_student),
        "students_with_transcripts": sum(1 for r in per_student.values() if r["messages"]),
        "sessions": sum(r["sessions"] for r in per_student.values()),
        "messages": sum(r["messages"] for r in per_student.values()),
        "user_messages": sum(r["user_messages"] for r in per_student.values()),
        "tool_calls": sum(r["tool_calls"] for r in per_student.values()),
        "transcript_chars": sum(r["chars"] for r in per_student.values()),
        "agent_created_skills": sum(len(r["agent_created_skills"]) for r in per_student.values()),
        "episodes": len(episodes),
        "episodes_with_failures": sum(1 for e in episodes if e["n_tool_failures"]),
        "resolved_arcs": sum(1 for e in episodes if e["resolved"]),
        "episodes_retry_depth_ge2": sum(1 for e in episodes if e["retry_depth"] >= 2),
        "total_tool_failures": sum(e["n_tool_failures"] for e in episodes),
        "total_wall_hours": round(sum(e["wall_seconds"] for e in episodes) / 3600, 1),
    }

    Path(args.out).write_text(json.dumps(
        {"totals": totals, "per_student": per_student, "tarballs": tarballs},
        indent=2), encoding="utf-8")

    print(json.dumps(totals, indent=2))


if __name__ == "__main__":
    main()
