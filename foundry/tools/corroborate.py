#!/usr/bin/env python3
"""Stage 3a - Merge triage shards and score candidate claims.

Six triage miners read disjoint slices of the corpus, so the same platform fact
can surface independently in several shards under different wording. That
independence is the strongest evidence we have: one student hitting a wall may
be a local mistake; three students on three nodes hitting the same wall is a
property of the platform.

This does the mechanical part - dedupe, count independent students, score - and
deliberately stops short of judging content. Merging near-duplicate *claims*
(same fact, different wording) needs a semantic reader and happens in the
consolidation stage that follows.

Scoring inputs, all of which downstream review can audit:
  independence   number of distinct students the claim appears under
  friction       structural cost of the episodes it came from (retry depth,
                 failures, wall time) - what the gap cost the cohort
  confidence     triage miner's own confidence
  generality     platform > toolchain > project-specific
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

CONF = {"high": 1.0, "medium": 0.6, "low": 0.3}
GEN = {"platform": 1.0, "toolchain": 0.8, "project-specific": 0.15}

STOP = set("""a an the and or of to in on for with is are be was were it this that
these those as at by from into if then than so not no do does did can could should
would when what which how why you your i we they them his her its my our""".split())


def keyset(text: str) -> set[str]:
    """Content words, used only as a cheap duplicate *hint* for human review."""
    return {w for w in re.findall(r"[a-z0-9_\-]{4,}", text.lower()) if w not in STOP}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--triage-dir", required=True)
    ap.add_argument("--episode-index", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    episodes = {e["episode_id"]: e for e in json.loads(Path(args.episode_index).read_text())}

    hits, shards = [], []
    for p in sorted(Path(args.triage_dir).glob("*.json")):
        try:
            d = json.loads(p.read_text())
        except Exception as e:
            print(f"  !! unreadable shard {p.name}: {e}")
            continue
        shards.append({
            "shard": p.name,
            "batches": d.get("batches"),
            "episodes_reviewed": d.get("episodes_reviewed"),
            "full_reads": len(d.get("full_reads", []) or []),
            "hits": len(d.get("hits", []) or []),
            "near_misses": len(d.get("near_misses", []) or []),
        })
        for h in d.get("hits", []) or []:
            h["_shard"] = p.name
            hits.append(h)

    # Attach the structural cost of the episode each claim came from. A claim
    # backed by a 45-minute 9-retry arc mattered more than one from a clean turn.
    for h in hits:
        ep = episodes.get(h.get("episode_id"), {})
        h["_friction"] = {
            "retry_depth": ep.get("retry_depth", 0),
            "n_tool_failures": ep.get("n_tool_failures", 0),
            "wall_seconds": ep.get("wall_seconds", 0.0),
            "resolved": ep.get("resolved", False),
        }
        if not h.get("student"):
            h["student"] = ep.get("student", "unknown")

    # Cheap lexical clustering: a *hint* for the semantic consolidator, never a
    # decision. Two claims cluster if their content words overlap heavily.
    clusters: list[dict] = []
    for h in sorted(hits, key=lambda x: -CONF.get(x.get("confidence", "low"), 0.3)):
        ks = keyset(h.get("claim", ""))
        placed = False
        for c in clusters:
            inter = len(ks & c["keys"])
            union = len(ks | c["keys"]) or 1
            if inter / union >= 0.45:
                c["hits"].append(h)
                c["keys"] |= ks
                placed = True
                break
        if not placed:
            clusters.append({"keys": ks, "hits": [h]})

    out = []
    for i, c in enumerate(clusters):
        hs = c["hits"]
        students = sorted({h.get("student", "unknown") for h in hs})
        shard_set = sorted({h["_shard"] for h in hs})
        conf = max(CONF.get(h.get("confidence", "low"), 0.3) for h in hs)
        gen = max(GEN.get(h.get("generality", "project-specific"), 0.15) for h in hs)
        friction = max(
            h["_friction"]["retry_depth"] * 2
            + min(h["_friction"]["n_tool_failures"], 20)
            + min(h["_friction"]["wall_seconds"] / 600.0, 5)
            for h in hs
        )
        # independence dominates; friction is a tiebreaker, not a driver
        score = round(len(students) * 3.0 * conf * gen + friction * 0.25 * gen, 2)
        out.append({
            "cluster_id": f"C{i:03d}",
            "claim": hs[0].get("claim"),
            "alt_phrasings": [h.get("claim") for h in hs[1:]],
            "kind": hs[0].get("kind"),
            "independence": len(students),
            "students": students,
            "shards": shard_set,
            "cross_shard": len(shard_set) > 1,
            "episodes": [h.get("episode_id") for h in hs],
            "confidence": max((h.get("confidence") for h in hs), key=lambda c: CONF.get(c, 0)),
            "generality": hs[0].get("generality"),
            "suggested_placement": hs[0].get("suggested_placement"),
            "why_novel": hs[0].get("why_novel"),
            "baseline_files_checked": sorted({
                f for h in hs for f in (h.get("baseline_files_checked") or [])
            }),
            "evidence": [
                {"episode_id": h.get("episode_id"), "student": h.get("student"),
                 "quote": h.get("evidence_quote"), "friction": h["_friction"]}
                for h in hs
            ],
            "score": score,
        })

    out.sort(key=lambda c: -c["score"])
    Path(args.out).write_text(
        json.dumps({"shards": shards, "clusters": out}, indent=2), encoding="utf-8"
    )

    print(f"shards: {len(shards)}  raw hits: {len(hits)}  clusters: {len(out)}")
    print(f"reviewed: {sum(s['episodes_reviewed'] or 0 for s in shards)} episode-slots")
    print(f"corroborated (>=2 students): {sum(1 for c in out if c['independence'] >= 2)}")
    for c in out[:20]:
        print(f"  {c['cluster_id']} score={c['score']:6.2f} n={c['independence']} "
              f"{c['kind'] or '?':14s} {(c['claim'] or '')[:80]}")


if __name__ == "__main__":
    main()
