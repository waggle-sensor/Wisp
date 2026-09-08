# Foundry v2 — results

Baseline (control) = `summer-camp-2026` hermes-profile **1.2.0**, i.e. the v1 release.
Everything below is delta *on top of* v1's shipped work.

## Funnel

```
14 brains  ->  11 with transcripts
 9,077 messages / 4,424 tool calls / 13.5M chars / 237.8 logged agent-hours
      |
      v  Stage 1  segmentation
   331 episodes   (174 with failures, 138 resolved arcs, 60 retry_depth>=2)
      |
      v  Stage 2  semantic triage, 6 parallel miners, every episode read
    53 hits       (~173 full-episode reads; 23 high / 30 medium confidence)
      |
      v  Stage 3  corroboration + semantic consolidation
    51 lexical clusters  ->  28 themes
      |
      v  Stage 3b human/analyst judgement
    19 promoted  ·  9 held  ·  12 correction themes (10 promoted -> 9 candidates)
      |
      v  Stage 5  bundling
    10 candidate bundles (HV2-0001 .. HV2-0010), full provenance
      |
      v  Stage 4  retrieval A/B vs 1.2.0
    10/10 targeted IMPROVED  ·  0 regressions  ·  5/5 guards hold
```

## A/B (deterministic, offline, re-runnable)

Control = 112 markdown files under `sage-waggle` (profile 1.2.0). Treatment = 122
(control + 10 proposed). Grading = BM25 retrieval@k **and** actionability within retrieved text.

| k | IMPROVED | REGRESSION | both_pass | both_fail |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 10 | 0 | 5 | 0 |
| 2 | 10 | 0 | 5 | 0 |
| 3 | 10 | 0 | 5 | 0 |
| 5 | 10 | 0 | 5 | 0 |

Stable across the sweep. The 5 `both_pass` rows are regression guards, which pass in
control *and* treatment — that is the desired result: pre-existing knowledge stayed
retrievable while 10 new pages were added.

Raw: `evals/ab_results.json`, `evals/sensitivity_k.json`, tasks in `evals/tasks.json`.

## Candidates

| ID | Title | n | Correction? | Baseline it contradicts |
| --- | --- | ---: | --- | --- |
| HV2-0001 | Agent HOME rewrite | **9** | gap | — (uncovered) |
| HV2-0002 | sudo NOPASSWD allowlist & image import | 2 | **yes** | `SKILL.md` ×6: `sudo k3s ctr images import` |
| HV2-0003 | pluginctl GPU needs runtimeClassName | 2 | **yes** | `runtime-packaging-patterns.md:106` |
| HV2-0004 | Podman/CDI GPU passthrough | 2 | **yes** | `SKILL.md:660`, `docker-build-deploy.md:73` |
| HV2-0005 | Host PyPI torch D-state hang | 1 | **yes** | `thor-host-cpu-dev-first.md` (**v1's own**) |
| HV2-0006 | conda-forge/pixi has no sm_110 | 1 | **yes** | host envs uncovered |
| HV2-0007 | `snapshot.data` is RGB not BGR | 1 | **yes** | `reolink-http-snapshot.md:54` |
| HV2-0008 | Camera offline dev (+ no camera attached) | 1 | **yes** | camera guidance assumes a camera |
| HV2-0009 | Off-node `Plugin()` thread failure | 1 | **yes** | "Local testing" section |
| HV2-0010 | Node-local registry x509 trust | 1 | **yes** | ImagePullBackOff causes |

**9 of 10 candidates correct shipped guidance rather than merely adding to it.** v1
produced zero corrections; its keyword-plus-additive design could not.

## Headline: the four the old method could not have found

1. **HOME rewrite (HV2-0001)** — 9/11 students, 52 episodes, the highest-independence
   finding in the corpus. Invisible to keyword mining (the symptom is a generic
   `No such file or directory`) and invisible to artifact mining (no student wrote a
   skill about it — they just paid the tax 52 times).
2. **The impossible procedure (HV2-0002)** — `SKILL.md` instructs
   `sudo k3s ctr images import` six times, calling it CRITICAL; `k3s` is not on the
   sudoers allowlist and the terminal has no TTY. A bag-of-words A/B scores this
   topic as thoroughly covered.
3. **v1 correcting itself (HV2-0005)** — v1 mined an artifact frozen 2026-07-23; the
   same student superseded it on 07-24 after discovering `import torch` itself
   D-states. Mining artifacts froze a claim the cohort had already outgrown.
4. **Silent wrongness (HV2-0007)** — `snapshot.data` is RGB while the baseline says
   BGR. No error is ever raised; a student settled it by measuring channel means.

## Held (9 themes, deliberately not promoted)

`T21` fleet-wide web-tool outage (transient provisioning state — shaped 26 episodes
and is reported as a cohort finding, but a page about a missing pip package goes
stale on reprovision) · `T22` provider-layer bug (outside profile scope) · `T23`
camera audio probing (site-specific hardware) · `T24` birdnet API (version-specific)
· `T25` git-lfs · `T26` cv2-absent Dockerfile line (needs a container check first) ·
`T27` no node-to-node primitive (negative claim, one episode) · `T28`
TFLite/YAMNet toolchain (**strongest held candidate** — genuinely novel, needs its
own page and a live re-run) · `T11` SKILL.md over size limit (a packaging action,
not a content page).

## Method results (as valuable as the findings)

- **Cross-shard convergence.** Independent miners on disjoint slices found the HOME
  rewrite (3 shards), host-torch failures (3), and the GPU-flag correction (3).
- **Friction ranks, it must not gate.** The lowest-friction batches produced 10 hits
  including the entire vLLM cluster. A friction threshold would have lost them.
- **Lexical clustering under-merges by design.** 51 clusters from 53 hits, 1
  corroborated; it split the top finding across 6 clusters. Semantic consolidation is
  not optional — see F10.
- **Miner disagreement is signal.** Two shards contradicted each other on sudo; the
  corpus (92 successes vs 9 TTY failures, all on non-allowlisted binaries) shows the
  truth is the conjunction. The over-general phrasing would have taught the next
  agent to abandon a working capability.
- **LLM miners hallucinate specifics.** The `skill_view` truncation claim could not
  be reproduced (all 50 calls pass `file=`; no truncation flag ever set). The defence
  is cheap mechanical re-derivation from the primary source, not a second LLM.
- **The A/B rejected a draft.** At k=1 a new page demoted the nvmap page; the first
  fix made it *worse* (quoting the neighbour's error strings raised BM25 from 19.6 to
  25.08). Final rule: name the neighbouring page, describe its symptom in your own
  words, never import its error text. See F12.

## Limitations

- **Canary covers 6 of 10 candidates** (`notes/03-canary.md`). The rest are textual
  only. Notably the canary *corrected* HV2-0004 — `--gpus all` exits 0 and injects
  nothing rather than erroring — so text-only evidence produced one subtly wrong
  claim that only hardware caught. Assume the same risk applies to the four untested.
- **The canary ran as root; students were non-root `%develop` members.** Config-level
  findings transfer directly; student-permission *experience* was read from config.
- **BM25 is a proxy.** It rewards term overlap, so a page can win retrieval for the
  wrong reason. Better than bag-of-words; not ground truth.
- **3 of 14 brains have no transcripts** and contribute only artifacts.
- **Independence is bounded by cohort size.** Most themes rest on 1-2 students; only
  the HOME rewrite has broad corpus-wide confirmation.
- **Episodes are lossy.** The corpus builder truncates tool results (1,155 elisions),
  which makes episodes inadmissible for any claim about output size or truncation.
- **No student outcome study.** We measure profile quality, not learning.

## Reproduce

```bash
python3 hermes/foundry-v2/tools/build_corpus.py    --brains .work/brains --out .work/corpus
python3 hermes/foundry-v2/tools/baseline_index.py  --profile ../summer-camp-2026/hermes-profile \
                                                   --out .work/corpus/baseline_map.json
python3 hermes/foundry-v2/tools/make_digests.py    --corpus .work/corpus
# Stage 2: 6 parallel LLM miners over .work/corpus/digests -> .work/triage/*.json
python3 hermes/foundry-v2/tools/corroborate.py     --triage-dir .work/triage \
    --episode-index .work/corpus/episode_index.json --out .work/corpus/corroborated.json
python3 hermes/foundry-v2/tools/consolidate.py
python3 hermes/foundry-v2/tools/build_bundles.py
python3 hermes/foundry-v2/tools/retrieval_eval.py \
    --control ../summer-camp-2026/hermes-profile/skills/sage-waggle \
    --treatment .work/treatment --tasks hermes/foundry-v2/evals/tasks.json \
    --out hermes/foundry-v2/evals/ab_results.json --k 3
```

Stages 1, 3b, 4, 5 are deterministic and need no network, GPU or LLM. Stage 2 is the
only LLM-dependent step; its outputs are committed under `evals/` and the candidate
bundles so the rest replays without re-running the miners.

---

## Correction — control was initially the wrong baseline

**What happened.** Both new branches were cut from `main`. v1's release
(`hermes-profile-1.2.0-foundry-uptake`) was never merged to `main`, so the working
clone's profile is **1.1.0** (`distribution.yaml: version: 1.1.0`, 109 sage-waggle
markdown files) — not the 1.2.0 this notebook had pinned as control throughout.

The first A/B therefore compared v2 against **1.1.0**, which does not contain v1's
three shipped pages (`thor-host-cpu-dev-first.md`,
`plugin-verification-invariants.md`, `ml-plugin-patterns-thor-base-image.md`). That
is the *easier* comparison, and it silently inflated the claim: v2 would have been
credited for ground v1 had already taken.

**Fix.** The true 1.2.0 tree was extracted from the v1 branch
(`git archive origin/hermes-profile-1.2.0-foundry-uptake`) into `.work/control_120`
(112 files) and every number in this document was re-derived against it.

**Re-run against the correct control — result is unchanged:**

| k | IMPROVED | REGRESSION | both_pass | both_fail |
| ---: | ---: | ---: | ---: | ---: |
| 1 | 10 | 0 | 5 | 0 |
| 2 | 10 | 0 | 5 | 0 |
| 3 | 10 | 0 | 5 | 0 |
| 5 | 10 | 0 | 5 | 0 |

**And the stricter control produced the pass's single best illustration.** On
`V2-T05-host-torch-hang`, against 1.2.0:

```
control   top-3: thor-host-cpu-dev-first.md, ecr-build-proc-acpi-failure.md, SKILL.md
          retrieval_hit=True   actionable=False   missing: ['D-state', 'module level']
treatment top-3: thor-host-torch-hang.md, thor-host-cpu-dev-first.md, thor-conda-forge-no-sm110.md
          retrieval_hit=True   actionable=True
```

v1's own page **is retrieved first** — the topic is squarely covered, and a
bag-of-words grader would score it a clean pass. But the page does not contain
`D-state` or the module-level-import rule, so an agent that loads it still cannot
solve the problem: it will set `CUDA_VISIBLE_DEVICES=` and hang anyway.

That is the retrieval-vs-actionability distinction in one row, on real shipped text,
and it is only visible because the control was made *harder*. Worth using as the
figure for this section.

**Process note.** The error surfaced from an incidental check of
`distribution.yaml` while staging the second repo, not from the pipeline. The
pipeline would happily have reported the inflated number. A baseline-provenance
assertion (hash or version check on the control corpus before grading) belongs in
`retrieval_eval.py` — logged as future work, not silently patched here.

---

## Release — profile 1.3.0

Branch `summer-camp-2026@hermes-profile-1.3.0-release`, commit `bd0f9e0`.

All ten candidates merged into `skills/sage-waggle/references/`, indexed in
`SKILL.md`, `distribution.yaml` bumped to 1.3.0.

### The base-tree trap, hit a second time

The release branch is cut from **`hermes-profile-1.2.0-foundry-uptake`, not `main`** —
the same wrong-baseline hazard recorded above, in its more damaging form.

`main` is still 1.1.0 (109 `sage-waggle` files) because v1's release was never merged
there. Building 1.3.0 on `main` would have:

1. shipped v2's ten pages while **silently dropping v1's three**
   (`thor-host-cpu-dev-first.md`, `plugin-verification-invariants.md`,
   `ml-plugin-patterns-thor-base-image.md`), plus `evals.json` and the
   `ml-plugin-patterns.md` edits;
2. left `thor-host-torch-hang.md` — which explicitly *supersedes*
   `thor-host-cpu-dev-first.md` — pointing at a file not present in the tree;
3. invalidated the A/B, which was graded against a 112-file control.

The release base was confirmed by fingerprint before merging: 112 files,
`971479c99bb63355`, identical to the A/B control. **Fingerprint the tree you release
from, not just the tree you grade against.**

`main` remains 1.1.0. Merging v1 to `main` is a separate open decision.

### Post-merge verification, on the released tree

Re-run against the **actual released tree** rather than the staged treatment copy, so
the `SKILL.md` index edit is included in what is graded:

| k | IMPROVED | REGRESSION | guards |
| ---: | ---: | ---: | ---: |
| 1 | 10 | 0 | 5/5 |
| 2 | 10 | 0 | 5/5 |
| 3 | 10 | 0 | 5/5 |
| 5 | 10 | 0 | 5/5 |

Raw: `evals/ab_released_130.json`, `evals/sensitivity_k_released_130.json`.

Also checked mechanically: every `references/*.md` cross-reference in the merged tree
resolves; `nvmap` appears 0 times in `thor-host-torch-hang.md` (the F12 writing rule
held through the merge); all ten pages are reachable from the `SKILL.md` index.

### Debt carried into 1.3.0, deliberately

`SKILL.md` is **117,644 chars against a 100,000-char limit** — 17.6% over. It was
already 14.4% over at 1.1.0, v1 grew it by 631 chars, and indexing these ten added
2,572 more.

The limit is `MAX_SKILL_CONTENT_CHARS`, documented in
`skills/software-development/hermes-agent-skill-authoring/SKILL.md` (identical across
all 13 brains carrying it, citing `tools/skill_manager_tool.py`). It is a **character**
cap; earlier revisions of these notes measured bytes and overstated the overage.

This is a knowing violation of F11's release rule ("v2 must not add prose to
`SKILL.md`"). The tension is real and worth stating plainly: `SKILL.md` is the index
that makes references discoverable, and retrieval is exactly what the A/B measures.
Shipping ten unindexed pages would have weakened the result the release rests on.
Splitting the file is theme **T11** and needs its own A/B — it is the first thing a
v3 pass should do.
