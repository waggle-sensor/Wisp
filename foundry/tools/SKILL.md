---
name: foundry-transcript-mining
description: Mine LLM agent conversation transcripts to find and fix defects in a shared agent profile. Use when improving documentation from a corpus of agent `state.db` transcripts, or when reproducing/extending the SAGE 2026 foundry-v2 study. Covers episode segmentation, LLM triage, corroboration, retrieval-graded A/B, and the 1.4.0 skill split.
license: Apache-2.0
allowed-tools: Bash
metadata:
  author: Sage Wisp foundry
  tags:
    - transcript-mining
    - documentation
    - retrieval-eval
    - agent-profiles
---

# Foundry — transcript mining tools

Reusable miners and harvest scripts. Frozen 1.4.0 campaign artifacts (candidates,
paper, evals, THEMES literals) live in `../harvest/1_4_0/`, not here.

They mine what agents **did** (SQLite transcripts) rather than what they **wrote**
(markdown artifacts), and grade every proposed doc page by retrieval before it ships.

**Read this first:** three scripts from this study are **not** reusable transforms.
They embed one campaign's findings as Python literals and live under
`../harvest/1_4_0/frozen/`. See *Generic vs. frozen* below.

## Pipeline

```
Stage 0  inventory                  cohort_stats.py
Stage 1  transcripts -> episodes    build_corpus.py
Stage 2  triage    (2a digests, 2b coverage map, then 6 LLM miners)
Stage 3  3a corroborate  ->  3b consolidate
Stage 4  retrieval A/B              retrieval_eval.py
Stage 5  bundle + human review      build_bundles.py / make_candidate.py
Stage 6  packaging split            split_blocks.py -> split_pitfalls.py
```

Every stage except 2's miners is deterministic, offline, and needs no LLM, GPU, or
network. The six miner shards are committed at `../evals/triage/triage_NN_NN.json`,
so the rest replays exactly.

## Available scripts

| Script | Stage | Arguments |
|---|---|---|
| `cohort_stats.py` | 0 | `--brains --archives --episode-index --out` |
| `build_corpus.py` | 1 | `--brains --out [--budget]` |
| `make_digests.py` | 2a | `--corpus [--batch-size]` |
| `baseline_index.py` | 2b | `--profile --out` |
| `corroborate.py` | 3a | `--triage-dir --episode-index --out` |
| `consolidate.py` | 3b | *(none — frozen in `../harvest/1_4_0/frozen/`)* |
| `retrieval_eval.py` | 4 | `--control --treatment --tasks --out --k` |
| `build_bundles.py` | 5 | *(none — frozen in `../harvest/1_4_0/frozen/`)* |
| `make_candidate.py` | 5 | `--id --root --clusters --cluster-ids --title --placement --action` |
| `split_blocks.py` | 6a | `--skill --out` |
| `split_pitfalls.py` | 6b | `--blocks [--skill] [--refs]` |
| `split_groups.py` | 6 | *(imported, not run — frozen in `../harvest/1_4_0/frozen/`)* |
| `filter_scope.py` | fig | `<graph.json> <path-prefix> <out.json>` |
| `filter_curated.py` | fig | `<graph.json> <out.json> [--regroup-by-skill]` |
| `render_scoped.py` | fig | `<in.json> <out.html> <title>` |
| `render_static.py` / `render_overview.py` | fig | `<in.json> <out-stem> <title>` |

## Generic vs. frozen

**Generic** — safe to point at any corpus: `build_corpus`, `make_digests`,
`baseline_index`, `corroborate`, `retrieval_eval`, `cohort_stats`, `split_blocks`,
`split_pitfalls`, `make_candidate`, and the five figure tools.

**Frozen** — these carry this study's findings as literal data, take no arguments,
and will not do anything useful on a different corpus:

| Script | Holds | Why it is code |
|---|---|---|
| `consolidate.py` | 28 `THEMES` | the analyst merge map, recorded as auditable data |
| `build_bundles.py` | 10 `BUNDLES` (HV2-0001..0010) | candidate id → themes → filename |
| `split_groups.py` | 11 `GROUPS` | pitfall block index → page (84 of 85 blocks; #48 is a verbatim duplicate, dropped) |

Stage 3b is a **human judgement** that was written down, not an algorithm. To mine a
new corpus you run Stages 1–3a, read `corroborated.json`, and write your own THEMES
table. Do not expect `consolidate.py` to cluster anything for you.

## Run the pipeline

From the Wisp repo root. `foundry/.work/` is gitignored — extracted brains and
intermediate corpora are too large for git.

```bash
# From the Wisp repo root. foundry/.work/ is gitignored.
python3 foundry/tools/build_corpus.py    --brains foundry/.work/brains --out foundry/.work/corpus
python3 foundry/tools/baseline_index.py  --profile . \
                                                   --out foundry/.work/corpus/baseline_map.json
python3 foundry/tools/make_digests.py    --corpus foundry/.work/corpus
# Stage 2: 6 parallel LLM miners read foundry/.work/corpus/digests/batch_*.txt -> foundry/.work/triage/*.json
python3 foundry/tools/corroborate.py     --triage-dir foundry/.work/triage \
    --episode-index foundry/.work/corpus/episode_index.json --out foundry/.work/corpus/corroborated.json
python3 foundry/harvest/1_4_0/frozen/consolidate.py     # 1.4.0 only; writes foundry/.work/corpus/consolidated.json
python3 foundry/harvest/1_4_0/frozen/build_bundles.py   # 1.4.0 only; writes foundry/harvest/1_4_0/candidates/
python3 foundry/tools/retrieval_eval.py \
    --control foundry/.work/control --treatment foundry/.work/treatment \
    --tasks foundry/harvest/1_4_0/evals/tasks.json \
    --out foundry/harvest/1_4_0/evals/ab_results.json --k 3
```

`consolidate.py` and `build_bundles.py` resolve `foundry/.work/corpus` and
`foundry/harvest/1_4_0` relative to the **Wisp repo root**, so they only run from there.

### Stage 6 — the packaging split

Run from the sage-waggle skill directory; `split_pitfalls.py` rewrites `SKILL.md` in
place and writes `references/pitfalls-*.md`.

```bash
python3 <tools>/split_blocks.py   --skill SKILL.md --out .work/split/blocks.json  # 85 blocks
python3 <tools>/split_pitfalls.py --blocks .work/split/blocks.json                # -> 85,771 chars
```

Verified reproducible: against the 1.3.0 release `SKILL.md` this regenerates the
shipped 1.4.0 artifact byte-for-byte — `SKILL.md` at 85,771 chars and all 11 pitfall
pages identical.

## The two ideas worth preserving

**1. Rank by friction, never gate on it.** Episode signals (`retry_depth`,
`resolved`, `user_frustration`) are deliberately *non-topical* — nothing in the
ranking encodes what you expect to find, which is what lets the method surface
subjects nobody put on a list. Stage 2 then reads **every** episode. The
lowest-friction batches produced ten findings, including an entire vLLM cluster; a
friction threshold would have discarded all of it.

**2. Grade retrieval and actionability, never keyword presence.** A task improves
only if a page that answers the question lands in the top *k* **and** the
symptom/cause/fix triad is present *within the retrieved text only*. Control and
treatment are ranked over their own corpora, so a new page that demotes an existing
answer registers as a regression. BM25 keeps it deterministic and LLM-free.

The second rule is load-bearing: there is a task in this corpus where the control
retrieves the right page **at rank 1** and still fails, because the page does not
contain the answer. Coverage is not the ability to act.

## Output contract

| Path | Written by | Contents |
|---|---|---|
| `.work/corpus/episodes/<eid>.md` | Stage 1 | one packed episode (~24k char budget) |
| `.work/corpus/episode_index.json` | Stage 1 | per-episode friction signals |
| `.work/corpus/digests/batch_NN.txt` | Stage 2a | miner input, hardest episodes first |
| `.work/corpus/baseline_map.json` | Stage 2b | 111 baseline files: title, lead, headings |
| `.work/corpus/corroborated.json` | Stage 3a | lexical clusters scored by independence |
| `.work/corpus/consolidated.json` | Stage 3b | 28 themes + merge map |
| `../harvest/1_4_0/candidates/HV2-*/` | Stage 5 | `candidate.yaml`, `PROVENANCE.json`, `evidence/`, `proposed/`, `RESULTS.md`, `REVIEW.md` |
| `../harvest/1_4_0/evals/*.json` | Stage 4 | A/B results, committed |

`retrieval_eval.py` output carries `control_fingerprint`, `control_files`,
`control_root`, `k`, `summary`, and per-task `{id, query, candidate, control,
treatment, verdict, split}`.

## Prerequisites

Stages 0–6 use the Python 3 standard library only — no third-party packages, no
network, no GPU. Only the three `render_*` figure tools have dependencies
(`matplotlib`, `networkx`, `graphify`); `filter_scope.py` and `filter_curated.py` are
stdlib too. Stage 2's miners need an LLM; nothing else does.

## Limitations

- **Stage 2 is not deterministic.** Miner outputs are committed so downstream stages
  replay exactly, but re-running the miners will not reproduce them.
- **Episodes are lossy.** The corpus builder truncates long tool results (1,155
  elisions). Episodes are **inadmissible evidence for any claim about output size or
  truncation** — go to the raw `state.db`. A pipeline's own lossiness can manufacture
  confirmation of exactly the claim you are checking (paper §6.3).
- **BM25 is a proxy.** It rewards term overlap; a page can win retrieval for the
  wrong reason.
- **Transcript evidence alone is not sufficient to ship a correction.** The hardware
  canary falsified a detail in one of ten candidates that read fine on the page.

## Troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `FileNotFoundError: 'foundry/.work/corpus/clusters_for_review.json'` | `consolidate.py` / `build_bundles.py` run from the wrong directory | run from the Wisp repo root |
| A/B reports a suspiciously perfect sheet | the suite may not retrieve the content you changed | check that some task actually loads it — see below |
| Control has fewer files than expected | graded against the wrong tree | compare `control_fingerprint` against the value in `../harvest/1_4_0/evals/ab_results.json` |
| `no '## Pitfalls' section in the given SKILL.md` | wrong file, or already split | pass the pre-split (1.3.0) `SKILL.md` |

**Before trusting any green result, ask what would have had to appear in this
evaluation for a failure to be visible.** Three times in this study the answer was
*nothing* — most sharply when the skill split scored a perfect 15/15 on a suite where
no task retrieved the moved content. A clean sheet from an instrument that cannot see
the change is not evidence of a safe change.

## References

- `../harvest/1_4_0/reports/paper.md` — full method (§3), results (§4), negative results (§6)
- `../README.md` — harvest → mine → A/B → merge loop
- `../harvest/1_4_0/evals/` — committed A/B results and triage shards
