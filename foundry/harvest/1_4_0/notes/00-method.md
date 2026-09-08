# Foundry v2 — method

Lab notebook for the second mining pass over the 2026 SAGE camp Hermes brains.
Companion to the v1 notebook (`hermes/notes/mining_notes.md`, branch
`hermes-profile-1.2.0-foundry-uptake`), which this pass is designed to improve on
rather than replace. Timezone: America/Chicago.

## Why a second pass

v1 shipped three validated file-level patches into profile 1.2.0 and established
the provenance discipline this pass reuses (quarantine → diff → atomic evidence →
candidate → A/B → human review). Two of its own stated limitations set the agenda
here:

1. **Discovery was keyword-bounded.** v1 mined the *markdown artifacts* students'
   agents produced — 19 agent-created `SKILL.md` files plus `MEMORY.md` — and
   selected within them with a fixed keyword list in a Python file. A keyword list
   can only find gaps someone already anticipated. Whole categories are invisible
   to it by construction.

2. **The A/B over-credited the control.** v1's grader asked whether required tokens
   appeared *anywhere* in a 1.6 MB skill tree. Its limitations section names the
   consequence: HERMES-0002 scored 1/7 on targeted improvements because six of the
   seven keywords already existed somewhere in the corpus, unfindable and
   unactionable though they were.

There is also a third gap, which v1 did not flag because it never looked: the
**richest source in each brain was never opened**. Each `sage/state.db` is a SQLite
database holding the student's full conversation history with the agent — every
prompt, every tool call, every failure, every eventual fix.

| Source | v1 | v2 |
| --- | --- | --- |
| Agent-created `SKILL.md` (19) | mined | mined (re-read semantically) |
| `MEMORY.md` (10 files) | mined | mined |
| `state.db` transcripts | **not opened** | **primary source** |
| Selection mechanism | keyword list | LLM triage vs. baseline coverage map |
| A/B grading | bag-of-words over whole tree | retrieval@k + actionability in retrieved text |

The transcripts are where the learning actually happened. The skills are a lossy
summary the agent wrote afterwards; the transcript is the experiment.

## Corpus scale (Stage 0)

Measured by `tools/cohort_stats.py` over the 14 public brains:

| Quantity | Count |
| ---: | --- |
| Brains collected | 14 |
| Brains with transcripts | 11 |
| Sessions | 140 |
| Messages | 9,077 |
| User turns | 635 |
| Tool calls | 4,424 |
| Transcript characters | 13.5 M |
| Logged agent wall-time | 237.8 h |
| Agent-created skills | 19 (0 with evals) |

3 of 14 brains have no `state.db` traffic; they contribute only artifacts. The
19-skill / 0-eval figure reproduces v1's Stage 1 result, which is a useful check
that the two passes agree where they overlap.

## Pipeline

```
Stage 0  freeze + inventory        tools/cohort_stats.py
Stage 1  transcripts → episodes    tools/build_corpus.py
Stage 2  semantic triage           tools/make_digests.py + tools/baseline_index.py
                                   + 6 parallel LLM miners
Stage 3  corroborate + consolidate tools/corroborate.py + semantic consolidation
Stage 4  retrieval A/B             tools/retrieval_eval.py
Stage 5  human review + release    candidates/ → profile 1.3.0
```

### Stage 1 — episodes, not files

`build_corpus.py` segments each session into **episodes**: a user turn plus every
assistant/tool message answering it, packed to a ~24k-char budget so a long
debugging arc stays in one readable unit.

Each episode carries **structural** friction signals — chosen deliberately so that
nothing is topical, and the pipeline generalises to subjects we did not anticipate:

- `retry_depth` — longest run of consecutive failing calls to the *same* tool. The
  sharpest marker of a real knowledge gap: the agent kept trying and kept losing.
- `n_tool_failures`, `failure_rate`, `wall_seconds`
- `resolved` — a failure run that ends in a clean call. The highest-value shape,
  because the symptom *and* the fix are both in the transcript.
- `user_frustration` — short corrective user turns after a failure, matched on the
  *shape* of the turn (brevity + negation/correction), not a topic list.

Result: **331 episodes**, 174 with failures, **138 resolved arcs**, 60 with
`retry_depth ≥ 2`.

### Stage 2 — semantic triage against a coverage map

Friction ranks episodes; it does not select them. Every one of the 331 episodes is
digested (~2.2k chars: the ask, later user turns, tools used, heads of failing tool
results) and batched. Six LLM miners read every batch against a **baseline coverage
map** (`baseline_index.py`: all 111 sage-waggle + SOUL/AGENTS files with title, lead
paragraph and section headings).

The brief (`.work/corpus/TRIAGE_PROMPT.md`) instructs miners to judge novelty
semantically — *would the baseline agent have gotten this right?* — to name the
baseline files they checked, to read the full episode before promoting anything
ambiguous, and to de-identify. Crucially it forbids topic filtering: an episode
about an unexpected subject is as eligible as one on a covered topic.

This is the structural fix for limitation (1). Nothing is excluded in advance by
vocabulary.

### Stage 3 — corroboration as evidence

`corroborate.py` merges the six shards and scores clusters by **independence**
(distinct students), weighted by miner confidence and generality, with friction as
a tiebreaker. One student hitting a wall may be a local mistake; three students on
three nodes hitting the same wall is a property of the platform. Lexical clustering
is treated as a *hint* for a semantic consolidation pass, never as a decision.

### Stage 4 — retrieval A/B

`retrieval_eval.py` replaces v1's bag-of-words grader. Per task it grades two
things, and a task improves only if **both** hold:

1. **Retrieval** — BM25-rank the corpus against the task query; does a file that
   answers the question land in the top-k? Control and treatment are ranked over
   their own corpora, so a new file that *demotes* an existing answer shows up as a
   regression.
2. **Actionability** — is the required symptom/cause/fix triad present **within the
   retrieved top-k text only**, not anywhere in the tree?

A keyword scattered across three unrelated pages no longer earns a pass. BM25 is
deliberate: deterministic, dependency-free, no LLM, no GPU, re-runnable offline by
a reviewer — the same reproducibility bar v1 set.

## Safety and provenance

Unchanged from v1, and re-applied here: harvested scripts are never executed;
brains are read-only; every promoted claim carries student, episode ID, and a
verbatim de-identified quote; no usernames, home paths, hostnames or tokens reach
any published artifact. Extracted brains stay untracked (`.work/`, gitignored) —
only tooling, evidence excerpts and results are committed.

## Stage 0 appendix — baseline pinned

Control profile for this pass is `summer-camp-2026` **1.2.0** (the v1 release), not
1.1.0. v2 therefore measures improvement *on top of* v1's shipped work: any delta
credited here is delta v1 did not already capture.

Coverage map for triage was built from the **1.1.0** tree checked out in the working
clone (111 files). The A/B control is the **1.2.0** release tree (112 sage-waggle
files), extracted from `origin/hermes-profile-1.2.0-foundry-uptake` — see the
correction note in `02-results.md`.

## Stage 4 harness validation (run before any candidate exists)

Sanity run with **control == treatment == baseline 1.2.0**, k=3:

```
control=112 files  treatment=112 files  k=3
  IMPROVED 0   REGRESSION 0   both_pass 5   both_fail 10
```

Three things this establishes, all necessary before the harness can be trusted:

1. **No self-improvement artefact.** Identical corpora produce 0 improvements and
   0 regressions, as they must.
2. **The 5 regression guards are valid guards.** They pass on the *current*
   baseline, so if they later fail it is because v2 demoted an existing answer —
   not because the task was unsatisfiable to begin with.
3. **The 10 targeted gaps are real.** All fail on 1.2.0, so v2 is not being graded
   against straw tasks.

### The v1-vs-v2 grading difference, visible in the sanity run

Two targeted tasks report `actionable=1, retrieval_hit=0`:

```
[-] V2-T08-camera-zero-arg        ctrl(ret=0,act=1)
[-] V2-T09-plugin-offnode-thread  ctrl(ret=0,act=1)
```

The required phrases *are* present in the top-k text, but no file that actually
answers the question was retrieved. Under v1's bag-of-words rule these would score
as **covered** — the exact over-crediting its limitations section describes. Under
retrieval@k they correctly score as **failures**, because an agent cannot act on
text it never loads.

This is the mechanism behind the F9 field observations: agents asserting "edge nodes
have no disk" and "ECR is broken fleet-wide" while the baseline contained the right
answer all along.
