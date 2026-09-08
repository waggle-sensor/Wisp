# Foundry v2 — running findings log

Chronological lab record. Each entry is a claim plus how it was checked, kept in
the order things were actually discovered so the write-up can reconstruct the
reasoning honestly (including the dead ends).

## F1 — v1 shipped an incomplete fix (correction to our own release)

**Found:** by hand, reading one student's transcripts, before triage returned.

v1's `thor-host-cpu-dev-first.md` (shipped in 1.2.0) prescribes:

> export `CUDA_VISIBLE_DEVICES=` … at the **top** of host scripts, before importing torch

Transcript evidence shows this is **not sufficient**. `import torch` *itself* enters
an uninterruptible D-state on Blackwell CUDA init even with `CUDA_VISIBLE_DEVICES=''`:

> `<user>   1734938 ... Dl 17:27 ... python scripts/train_and_evaluate.py`
> "They're in D state (uninterruptible), can't be killed even with SIGKILL."

The student's own MEMORY.md records the corrected rule:

> "UPDATE 2026-07-24: import torch ITSELF hangs in D-state (triggers CUDA runtime
> init even with CUDA_VISIBLE_DEVICES=''). D-state procs can't be killed with
> SIGKILL. Training scripts must NOT import torch at module level — gate behind
> env var inside function bodies so sklearn paths never touch torch."

The working fix in-transcript is a **subprocess probe with a timeout** plus lazy,
function-body-local torch imports, so sklearn code paths never touch torch.

Note the dating: v1's evidence came from the 2026-07-23 state of this student's
knowledge; the correction landed 2026-07-24. v1 mined the artifact, not the arc,
and so froze a claim the cohort had already superseded. **This is the clearest
argument for mining transcripts over artifacts.**

Episodes: `node-H021-20260724_153151_f3cf31-04`,
`...-20260723_212632_b287ca-03`, `...-20260727_142358_6b4b35-09`.

## F2 — HOME rewrite: a harness defect, cohort-wide

**Found:** triage shard 04_05, then verified independently by grep.

The agent's shell runs with `HOME` rewritten to
`/home/<user>/.hermes/profiles/sage/home`, so every `cd ~/project` or
`$HOME`-relative path resolves inside the profile directory and fails:

> `/usr/bin/bash: line 3: cd: /home/<user>/.hermes/profiles/sage/home/AI-Projects/birdnet: No such file or directory`

**Blast radius (measured, not estimated):**

| Metric | Value |
| --- | ---: |
| Students affected | **9 of 11** with transcripts |
| Episodes containing the rewritten path | **52** |
| Explicit `cd … No such file or directory` failures | 18 |

Affected paths are not just project dirs: `.ssh`, `.cache`, `.local`, `.venvs`,
`.config`. One consequence recorded in triage: a cold podman store under the
profile HOME caused a full **~5.5 GB base-image re-pull** because the user's
interactive shell already had the layer cached and the agent's did not.

This is the flagship v1-vs-v2 case. It is invisible to keyword mining — the
symptom is an ordinary "No such file or directory", indistinguishable from a
student typo — and it is invisible to artifact mining, because no student wrote a
skill about it; they just silently paid the tax 52 times. Only friction-ranked
transcript reading surfaces it.

Highest independence of anything in the corpus.

## F3 — Baseline self-contradiction on GPU flags (Podman node class)

Baseline `SKILL.md:660` states:

> "**Always** use `--runtime=nvidia` in documentation and scripts"

On the Podman node class this is simply wrong. One student's MEMORY.md:

> "`docker` is Podman 4.9.3 — only `--device nvidia.com/gpu=all` works for GPU;
> `--runtime nvidia` and `--gpus all` both fail."

Corroborated across three students independently (one explicit Podman/CDI note; one
"No sudo — use podman for builds"; one k3s registry TLS workaround via `podman save`). This is a **correction**, not an addition — the baseline actively
misleads on this node class.

## F4 — `runtimeClassName` / device-plugin gap (verified novel)

Triage claim: `pluginctl run` silently yields a CPU-only pod where the node runs no
nvidia-device-plugin, because pluginctl never sets `runtimeClassName`. Measured
cost in-episode: **27 ms/frame GPU vs ~1.4 s/frame CPU** (~50x).

Verified by grep: `runtimeClassName` appears **nowhere** in the baseline. Worse,
`runtime-packaging-patterns.md:106` asserts the opposite —
"GPU available via NVIDIA device plugin" — so the baseline steers an agent away
from the diagnosis.

## F5 — Sources with zero baseline coverage (spot checks)

- `YOLO_CONFIG_DIR` / "Ultralytics settings dir not writable" — no baseline hit.
  Appears in student paste output from a real `pluginctl run`.
- `sage-thor-vlm-serving` — an entire 11.5 KB agent-created skill (Podman+CDI GPU,
  unified-memory vLLM tuning, three distinct reproducible pitfalls, a ruled-out
  image table) that v1 did not mine at all.

## Method note — what these findings say about the two passes

F1 and F3 are **corrections**: cases where the shipped baseline is wrong or
incomplete. A pipeline that only ever *adds* material cannot produce them, and v1's
keyword-plus-additive design structurally could not. F2 is a **harness** defect
rather than a domain fact, which is a category no domain keyword list contains.

## F6 — RGB/BGR channel-order contradiction (empirically measured by a student)

Triage claim: pywaggle's `Camera` defaults to `format=RGB` and `ImageSample.__init__`
applies `cv2.cvtColor(data, COLOR_BGR2RGB)` on construction, so `snapshot.data[...,0]`
is **RED**, not blue.

The student did not assert this — they measured it:

> `snapshot.data mean per channel: [ 70.83785067 116.5195262 43.16166252]`
> `raw cv2 BGR mean per channel:   [ 42.92750985 115.93265991 70.93280802]`

Channels 0 and 2 are swapped, empirically.

**The baseline says the opposite.** `reolink-http-snapshot.md:54`:

> "Returns BGR numpy array, same format as `Camera.snapshot().data`"

So a plugin author following the baseline reasons about `snapshot.data` as raw cv2
BGR and publishes silently colour-swapped images — a failure with **no error
message at all**, which is precisely the class that survives to production.

Third correction found (with F1, F3). The v1 pipeline could not produce corrections
of this kind: bag-of-words overlap treats "BGR" appearing in the corpus as coverage,
when the corpus is confidently wrong.

## Interim tally of *correction*-type findings

| # | Correction | Baseline location | Independence |
| --- | --- | --- | ---: |
| F1 | `CUDA_VISIBLE_DEVICES=` insufficient; `import torch` D-states | `thor-host-cpu-dev-first.md` (**shipped by v1**) | 1 (+MEMORY) |
| F3 | `--runtime=nvidia` fails on Podman node class | `SKILL.md:660` | 3 |
| F4 | "GPU available via NVIDIA device plugin" not universal | `runtime-packaging-patterns.md:106` | 1 (50x measured) |
| F6 | `snapshot.data` is RGB, not BGR | `reolink-http-snapshot.md:54` | 1 (measured) |

## F7 — The baseline's canonical side-load step is impossible on camp accounts

**Found:** triage shard 00_01, verified directly against transcript + baseline.

Baseline `SKILL.md` instructs `sudo k3s ctr images import` in **five separate
places** (lines 655, 656, 657, 677, 680, 681) — it is the documented way to get a
locally built image into k3s, called "**CRITICAL**" and "required for local testing".

The actual camp sudoers allowlist, printed by `sudo -l` in-transcript:

> `(ALL) NOPASSWD: /usr/local/bin/kubectl, /usr/bin/docker, /usr/local/bin/docker,`
> `/usr/bin/docker-compose, /usr/local/bin/docker-compose, /usr/bin/runplugin, /usr/bin/pluginctl`

`k3s` is **not on the list**. The transcript shows exactly what a student hits:

> `=== sudo k3s kubectl nodes ===`
> `Sorry, try again.` … `sudo: 3 incorrect password attempts`

And the Hermes terminal has no TTY, so there is no password prompt to answer — the
documented procedure is not merely inconvenient, it is unreachable.

**Working alternatives found in-transcript:** `sudo pluginctl build` (builds *and*
pushes to the node registry, allowlisted), or a privileged import pod applied with
`sudo kubectl`. Both are on the allowlist.

This is the most consequential correction of the pass. It is not a missing fact —
it is a prominent, repeated, emphatic instruction in the shipped baseline that
cannot execute on the hardware the profile targets. Bag-of-words A/B would score
this topic as *fully covered* (every keyword present, six times over).

Independence: sudoers listing on H021; the same allowlist shape is relied on across
other students' successful `sudo pluginctl` / `sudo kubectl` calls.

## F8 — Fleet-wide tool outage with documented downstream harm

Three built-in web tools are dead on camp profiles: `web_search` fails with
"ddgs package is not installed" (**26 of 331 episodes**), no Chrome for the browser
tool (19), and the extract backend refuses (19). `pip install ddgs` does *not* fix
`web_search`.

Triage flagged a concrete consequence: one blocked agent filled ECR metadata images
with unrelated stock photos rather than reporting the tool as unavailable.

Classification note: this is **provisioning state, not platform knowledge**, and one
miner correctly argued for excluding it on those grounds. I keep it as a *cohort
finding* for the paper (it shaped 26 episodes of behaviour and is a real
agent-integrity failure mode) but it is **not** a candidate for promotion into the
profile — a profile page describing a broken package is stale the moment the fleet
is reprovisioned. Recorded under "operational findings", not "uptake".

## Note on miner disagreement (kept deliberately)

Shard 02_03 flagged that hits about Docker GPU flags and the dead web toolchain
"suggest the baseline may be drifting from the camp fleet's actual state" and asked
for targeted re-verification before promotion, warning that *a stale correction is
worse than none*. That is the right instinct and it is adopted: F3/F4 corrections
ship with an explicit `verify_on: instructor canary` field, and F8 is excluded from
promotion entirely. Disagreement between miners is recorded rather than resolved
away — it is evidence about the method's calibration.

## F9 — Retrieval failures, not coverage failures (the strongest evidence for the new A/B)

Shard 10_11 flagged two near-misses that are *not* missing knowledge at all:

1. An agent asserted "edge nodes do not have a disk" and made an architecture
   decision on it — **directly contradicting** the `/local-cache` material the
   baseline documents across three files.
2. An agent steered a student away from ECR as "broken fleet-wide" **eleven days
   after** `ecr-build-to-ses-cutover.md` recorded the fix. The blocker page won
   retrieval over the cutover page.

In both cases the baseline **contains the right answer and the agent did not get
it**. This is the failure mode v1's grader is blind to by construction: a
bag-of-words check confirms the tokens are present in the corpus and scores the
topic as covered, while the deployed agent confidently says the opposite.

It is also the direct justification for grading `retrieval@k` and scoring
actionability *only within retrieved text*: content that cannot be retrieved is
not coverage, and a stale page that outranks its own correction is a **regression**
the new harness can see and the old one cannot.

Actionable consequence for the release: staleness marking and cross-links matter as
much as new prose. Where two baseline pages disagree, the newer one must say so
explicitly and the older must point forward.

## F10 — Resolving a miner disagreement (a calibration result, not just a fact)

Two shards produced claims about `sudo` that **contradict each other**:

- Shard 00_01 (high): camp accounts have `NOPASSWD` sudo for an allowlist
  (`kubectl, docker, docker-compose, runplugin, pluginctl`); `k3s`/`ctr`/`crictl`
  are excluded.
- Shard 08_09 (medium): "The Hermes terminal tool on a camp Thor **cannot run
  `sudo`** — there is no tty … *every* `sudo pluginctl` / `sudo kubectl` call fails".

Both cite real quotes. They cannot both be right as stated, so I resolved it
against the corpus rather than trusting either:

| Signal | Count |
| --- | ---: |
| Episodes containing `sudo: a terminal is required…` | 9, across 5 students |
| Episodes containing an auto-approved **successful** sudo call | 92, across 8 students |

Then, which binaries appear near the TTY failures? Every one is **off** the
allowlist: `k3s`, `apt-get`, `nvidia-ctk`, `systemctl`, `usermod`, `cat`.

**Synthesised truth (what actually ships):** sudo works from the Hermes terminal
*only* for the NOPASSWD-allowlisted binaries. Any other binary needs a password,
and because the tool has no TTY and no askpass helper, it fails with
`a terminal is required to read the password` rather than prompting. The agent
should recognise that error as "this binary is not on the allowlist" — not as
"sudo is unavailable" — and either switch to an allowlisted path
(`sudo pluginctl build`, `sudo kubectl apply`) or hand the command to the student.

Shard 08_09's over-general claim would, if promoted verbatim, have taught the next
agent to stop using `sudo pluginctl` — a capability that demonstrably works 92
times. It was rated `medium`, which is the pipeline behaving correctly.

**Why this matters for the write-up:** it is direct evidence for the corroboration
stage doing real work. Independent miners disagreeing is not noise to average away;
it localises exactly where a claim needs adjudication against the corpus. A
single-pass keyword miner has no analogue of this — nothing to disagree with, and
no way to notice the over-generalisation. Recorded as a **method** result.

## F11 — A miner claim I could NOT reproduce (negative result, recorded)

Shard 06_07 reported: `skill_view("sage-waggle")` returns ~121.8k chars and is
"truncated/spilled", observed in 5 episodes across 4 students, contradicting
SOUL.md/AGENTS.md's "always load the skill".

**I could not reproduce the truncation claim.** Checked directly against the raw
`state.db` files rather than my own episode renders (my corpus builder truncates
tool results itself — 1,155 elisions — so episodes are *not* admissible evidence
for a truncation claim, a trap worth noting):

| Check | Result |
| --- | --- |
| `skill_view` results naming `sage-waggle` | 50 |
| …that requested the **whole skill** (no `file=`) | **0** |
| …that requested a single reference file | 50 |
| Payload sizes | min 1,061 / mean 12,152 / max 48,193 chars |
| Any `truncated` flag set | none |

Every observed call targets one reference (`stack-architecture-map.md` ×7,
`pluginctl-camp-guide.md` ×7, …). No full-body load appears in the corpus, so no
truncation event is visible in it. The miner's "121.8k" is close to the real file
size (114,441 chars / 115,244 bytes) and may come from a static size report or a
session outside the corpus, but I cannot verify it, so it does not ship.

**However, the underlying packaging problem is independently real and verified:**

**The limit, and where it comes from.** The enforced cap is **100,000 characters**,
not bytes:

> "Full SKILL.md: ≤ 100,000 chars (enforced as `MAX_SKILL_CONTENT_CHARS`, ~36k
> tokens)."
> — `skills/software-development/hermes-agent-skill-authoring/SKILL.md`

That page names the enforcing constant and cites
`tools/skill_manager_tool.py::_validate_frontmatter` as its source of truth. It is
**byte-identical in all 13 brains** that carry it, so it is not one agent's
invention. Two caveats: it ships with the Hermes install, **not** with the sage
profile (it is absent from the baseline), and we have **not read
`skill_manager_tool.py` directly** — this is strongly corroborated secondary
evidence, not the constant read from code. Reading that file on a node would settle
it.

**Measured against that limit — in characters:**

| Version | `sage-waggle/SKILL.md` | vs 100,000-char limit |
| --- | ---: | --- |
| 1.1.0 (`main`) | 114,441 chars | **+14.4%** |
| 1.2.0 (v1 release) | 115,072 chars | **+15.1%** (v1 *grew* it by 631) |

Corroborated from the write side by a student's MEMORY.md, which reports the
consequence rather than the constant:

> "sage-waggle SKILL.md body is 114KB (limit 100KB) — can't be patched in place via
> `skill_manage action=patch`; future updates require splitting the body… the
> in-place patch path aborts with a size error."

**Measurement correction.** Earlier revisions of this log, and of the paper, reported
these as *bytes* (115,244 B / 115,885 B) against a "100 KB" limit. The file contains
multi-byte characters, so byte counts overstate the overage: the cap is on characters
and the correct figures are the ones tabulated above. The direction of every
conclusion is unchanged — the file was already over before this pass, and v1 grew it
— but the magnitudes were wrong and are corrected throughout.

So: the *file is over limit* (verified, and v1 made it worse), while the *read-path
truncation* (unverified) is a separate claim I am dropping. Promoting the verified
half only.

This is the corroboration stage earning its keep in the other direction — catching
a plausible, confidently-stated, partly-wrong claim before it shipped. Worth a line
in the paper: LLM miners hallucinate specifics, and the defence is cheap mechanical
re-derivation from the primary source, not a second opinion from another LLM.

**Release consequence:** v2 must not add prose to `SKILL.md`. Any new material goes
in `references/`, and the release should *reduce* SKILL.md if it touches it at all.

## F12 — The A/B caught a regression the old grader could not, and it changed the artifact

Not a finding about the platform — a finding about the method, and the clearest
demonstration in this pass that the new harness does real work.

**First full A/B run**, k=3: 10/10 targeted improved, 0 regressions. Clean. But k=3
is generous, so I swept k:

```
k=1  IMPROVED 10  REGRESSION 1   <-- V2-R01-nvmap-regression
k=2  IMPROVED 10  REGRESSION 0
k=3  IMPROVED 10  REGRESSION 0
k=5  IMPROVED 10  REGRESSION 0
```

At k=1 the new `thor-host-torch-hang.md` (19.60) **outranked**
`direct-node-testing.md` (21.34 in control) for the nvmap query. That is exactly the
failure mode v1's bag-of-words grader is structurally blind to: adding a *correct*
page demoted a *different correct* page, and the two failures are easy to confuse —
one hangs forever, one fails fast with a permission error. An agent that lands on the
wrong one wastes the session.

**Fix attempt 1 made it worse.** I added a disambiguation banner naming the other
symptom (`NvRmMemInitNvmap Permission denied`, `/dev/nvmap`). Score went *up*, from
19.60 to **25.08** — I had fed the competing page's highest-signal query terms into
my own page. A human reading the banner would be helped; BM25 read it as "this page
is even more about nvmap".

**Fix attempt 2 worked.** Point to the right page *without restating its symptom
vocabulary*:

> **Scope:** this page covers only the case where a CUDA call never returns. A fast
> failure with a device-permission message is a different problem — see
> `references/direct-node-testing.md`.

`nvmap` now appears **zero** times in the new file. Result: **0 regressions at every
k in {1,2,3,5}**, 10/10 targeted improved throughout.

### Why this matters for the write-up

1. The regression was invisible at the default k and only appeared under a
   sensitivity sweep. **Report the sweep, not a single k.**
2. Retrieval-graded A/B is not a rubber stamp — it rejected a draft and forced a
   concrete edit to the shipped artifact.
3. There is a real tension worth naming: **cross-links that help a human reader can
   hurt a lexical retriever.** The resolution is to name the *neighbouring page* and
   describe the other symptom in your own words, never to quote its error strings.
   That is a writing rule the harness discovered, and it generalises to any
   BM25-indexed doc set.
4. It is also a caution about the harness itself: BM25 rewards term overlap, so a
   page can win retrieval for the wrong reason. Retrieval@k is a better proxy than
   bag-of-words, not ground truth. Live canary testing still matters.
