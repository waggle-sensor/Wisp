# Harvest 1.4.0 — transcript mining campaign

Frozen 2026 SAGE camp pass that shipped as Wisp / hermes-profile **1.4.0**.
Reusable miners live in [`../../tools/`](../../tools/SKILL.md). **Do not merge
these candidates again** — they are already in the live profile.

Where **v1** mined agent-written markdown with a keyword list, **this pass mined
`state.db` transcripts** and selected semantically.

## Layout

```
brains/         node-id public tarballs + MANIFEST.tsv (no usernames)
candidates/     HV2-0001..0010 — proposed pages + provenance
notes/          00-method · 01-findings-log · 02-results · 03-canary · 04-skill-split
reports/        paper.md · blog/
evals/          tasks.json, ab_results.json, triage shards
figures/        knowledge-graph before/after
frozen/         consolidate.py, build_bundles.py, split_groups.py (THEMES/BUNDLES literals)
```

Brains are named `node-H01D`, …; the shared blade is `node-H037a` / `node-H037b`.

## Results

**10/10 targeted tasks improved, 0 regressions, stable across k ∈ {1,2,3,5}**;
5/5 regression guards hold. Full numbers: [`notes/02-results.md`](notes/02-results.md).

Nine of ten candidates **correct** shipped guidance rather than adding topics.

A **live canary on `node-H039.sage` (2026-09-02)** verified 6 of the 10 on real
hardware and **corrected one candidate** that transcript evidence alone had got
subtly wrong. See [`notes/03-canary.md`](notes/03-canary.md).

Paper: [`reports/paper.md`](reports/paper.md). Reproduce: [`../../tools/SKILL.md`](../../tools/SKILL.md).

## Safety

Harvested scripts are never executed; brains are read-only; extracted profiles
stay untracked under `foundry/.work/` (gitignored). Committed keys are node ids,
not usernames.
