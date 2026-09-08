#!/usr/bin/env python3
"""Stage 5 - Emit candidate bundles with provenance from consolidated themes.

Mirrors the v1 candidate layout so the two passes are diffable by a reviewer:
candidate.yaml / PROVENANCE.json / evidence/excerpts.md / proposed/ / RESULTS.md.

Every promoted claim must be walkable backwards - from a line of proposed profile
text, to the theme, to the students and episode ids, to a verbatim de-identified
quote from the conversation that produced it. That traceability is the point of the
bundle; the prose is just the deliverable.
"""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("foundry/harvest/1_4_0")
CORPUS = Path("foundry/.work/corpus")

# candidate id -> (themes, proposed filename, title)
BUNDLES = {
    "HV2-0001": (["T01"], "agent-shell-environment.md", "Agent HOME rewrite on camp Thor nodes"),
    "HV2-0002": (["T02"], "sudo-allowlist-and-image-import.md", "sudo NOPASSWD allowlist and image import"),
    "HV2-0003": (["T03"], "pluginctl-gpu-runtimeclass.md", "pluginctl GPU requires runtimeClassName"),
    "HV2-0004": (["T04"], "podman-cdi-gpu-passthrough.md", "Podman/CDI GPU passthrough"),
    "HV2-0005": (["T05"], "thor-host-torch-hang.md", "Host PyPI torch D-state hang"),
    "HV2-0006": (["T06"], "thor-conda-forge-no-sm110.md", "conda-forge/pixi torch has no sm_110"),
    "HV2-0007": (["T07"], "pywaggle-snapshot-channel-order.md", "snapshot.data is RGB not BGR"),
    "HV2-0008": (["T08", "T12"], "pywaggle-camera-offline-dev.md", "Camera offline development"),
    "HV2-0009": (["T09"], "pywaggle-offnode-local-testing.md", "Off-node Plugin() thread failure"),
    "HV2-0010": (["T10"], "node-registry-x509-trust.md", "Node-local registry x509 trust"),
}


def main() -> None:
    consolidated = json.loads((CORPUS / "consolidated.json").read_text())
    themes = {t["theme_id"]: t for t in consolidated["themes"]}
    raw_hits = {}
    for p in sorted(Path("foundry/.work/triage").glob("*.json")):
        for h in json.loads(p.read_text()).get("hits", []) or []:
            raw_hits.setdefault(h.get("episode_id"), []).append(h)
    episodes = {e["episode_id"]: e for e in json.loads((CORPUS / "episode_index.json").read_text())}
    ab = json.loads((ROOT / "evals" / "ab_results.json").read_text())
    ab_by_cand = {}
    for t in ab["tasks"]:
        ab_by_cand.setdefault(t.get("candidate"), []).append(t)

    for cid, (tids, fname, title) in BUNDLES.items():
        d = ROOT / "candidates" / cid
        (d / "evidence").mkdir(parents=True, exist_ok=True)
        ts = [themes[t] for t in tids]
        students = sorted({s for t in ts for s in t["students"]})
        eps = sorted({e for t in ts for e in t["episodes"]})
        corrections = [t for t in ts if t["is_correction_of_baseline"]]

        indep = max(t["independence"] for t in ts)
        indep_src = next((t["independence_source"] for t in ts
                          if t.get("independence_source")), None)
        (d / "candidate.yaml").write_text(
            f"""id: {cid}
title: "{title}"
action: {"modify_guidance" if corrections else "add"}
placement: "skills/sage-waggle/references/{fname}"
status: proposed
source_pass: foundry-v2
baseline: sage 1.2.0
themes: [{', '.join(tids)}]
independence: {indep}
{f"independence_source: {indep_src}" + chr(10) if indep_src else ""}students_in_evidence: [{', '.join(students)}]
episodes_n: {len(eps)}
is_correction: {str(bool(corrections)).lower()}
""" + ("baseline_conflict: |\n" + "".join(
                f"  {t['baseline_conflict']}\n" for t in corrections) if corrections else "")
            + "claims:\n" + "".join(f"  - {t['canonical_claim']}\n" for t in ts),
            encoding="utf-8")

        (d / "PROVENANCE.json").write_text(json.dumps({
            "id": cid,
            "pass": "foundry-v2",
            "method": "state.db transcript -> episode segmentation -> LLM triage vs "
                      "baseline coverage map -> cross-student corroboration -> "
                      "semantic consolidation -> retrieval@k A/B",
            "baseline": "summer-camp-2026 hermes-profile 1.2.0",
            "themes": ts,
            "students": students,
            "episodes": eps,
            "ab_tasks": ab_by_cand.get(cid, []),
        }, indent=2), encoding="utf-8")

        lines = [f"# {cid} — evidence", "",
                 f"**{title}**  ·  independence: {indep} student(s)  ·  {len(eps)} episode(s)", ""]
        for t in ts:
            lines += [f"## {t['theme_id']} — {t['title']}", "",
                      f"- **Claim:** {t['canonical_claim']}",
                      f"- kind: `{t['kind']}` · confidence: {t['confidence']} · "
                      f"generality: {t['generality']} · cross-shard: {t['cross_shard']}",
                      f"- merged from clusters: {', '.join(t['merged_from'])}"]
            if t["baseline_conflict"]:
                lines.append(f"- **Baseline conflict:** {t['baseline_conflict']}")
            if t["notes"]:
                lines.append(f"- **Notes:** {t['notes']}")
            lines.append("")
            for eid in t["episodes"]:
                ep = episodes.get(eid, {})
                for h in raw_hits.get(eid, []):
                    q = (h.get("evidence_quote") or "").strip()
                    if not q:
                        continue
                    lines += [f"### `{eid}`",
                              f"friction: retry_depth={ep.get('retry_depth',0)} "
                              f"failures={ep.get('n_tool_failures',0)} "
                              f"wall={ep.get('wall_seconds',0)}s "
                              f"resolved={ep.get('resolved',False)}", "",
                              "> " + q.replace("\n", "\n> "), ""]
        (d / "evidence" / "excerpts.md").write_text("\n".join(lines), encoding="utf-8")

        tasks = ab_by_cand.get(cid, [])
        rl = [f"# {cid} — A/B results", "",
              "Retrieval@k (BM25) + actionability within retrieved text. "
              "Control = profile 1.2.0 sage-waggle (112 md). Treatment = control + proposed (122 md).", "",
              "| task | control ret/act | treatment ret/act | verdict |", "| --- | --- | --- | --- |"]
        for t in tasks:
            c, x = t["control"], t["treatment"]
            rl.append(f"| `{t['id']}` | {int(c['retrieval_hit'])}/{int(c['actionable'])} "
                      f"| {int(x['retrieval_hit'])}/{int(x['actionable'])} | **{t['verdict']}** |")
        rl += ["", "Stable across k in {1,2,3,5}: 10/10 targeted improved, 0 regressions "
                   "(see `../../evals/sensitivity_k.json`).", "",
               "**Not validated here:** live on-node behaviour. These graders measure "
               "retrievability and actionability of text, not hardware outcomes. "
               "Instructor canary required before fleet-wide trust — see REVIEW.md."]
        (d / "RESULTS.md").write_text("\n".join(rl), encoding="utf-8")

        (d / "REVIEW.md").write_text(
            f"""# {cid} — human review

- [ ] Claim is accurate and de-identified
- [ ] Placement is right (reference vs SOUL vs new skill)
- [ ] Does not duplicate existing baseline content
- [ ] Cross-links name neighbouring pages without importing their error strings
      (see findings log F12 — quoting a neighbour's symptom text distorts retrieval)
{"- [ ] **Correction**: confirm the baseline text it contradicts is genuinely wrong on current fleet state" if corrections else ""}

**Reviewer:** _unassigned_
**Decision:** _pending_

## Verification status

Deterministic retrieval A/B only. No live Thor canary was run in this pass.
{"**This candidate contradicts shipped guidance** — a stale correction is worse than none. Verify on a current node before merging." if corrections else ""}
""", encoding="utf-8")

        print(f"{cid}  n={indep}  themes={','.join(tids)}  "
              f"{'CORRECTION' if corrections else 'add'}  {len(eps)} episodes")


if __name__ == "__main__":
    main()
