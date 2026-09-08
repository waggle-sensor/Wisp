# T11 — splitting `sage-waggle/SKILL.md` under `MAX_SKILL_CONTENT_CHARS`

Theme T11 was held back from the 1.3.0 release because splitting SKILL.md needed its
own A/B. This is that pass. Branch: `hermes-profile-1.4.0-skill-split`.

## The problem, restated correctly

Two limits, from `skills/software-development/hermes-agent-skill-authoring/SKILL.md`:

- **Hard:** 100,000 chars (`MAX_SKILL_CONTENT_CHARS`). `sage-waggle` was at **117,644**
  — 17,644 over. This is what makes `skill_manage action=patch` abort.
- **Soft:** *"Peer skills sit at 8-14k chars… If you're pushing past 20k, split into
  `references/*.md`."*

The soft limit explains the hard one. Measured against the other 250 skills in the
profile, `sage-waggle` was not marginally over — it was a **3x outlier**:

| skill | chars |
| --- | ---: |
| `sage-waggle` | **117,644** |
| `graphify` (next largest) | 38,370 |
| `hf-cli` | 31,227 |
| median of 250 | ~12,000 |

Trimming 15% to squeak under 100,000 would have treated the symptom. v1 grew the file
by 631 chars and the 1.3.0 index added 2,572; it regrows on every pass.

## Where the weight was

```
50,556  43.0%  ## Pitfalls          85 bullets, median 508 chars, 13 over 800
24,901  21.2%  ## Plugin Development
20,593  17.5%  ## See Also          88 entries
21,594  18.3%  11 other sections
```

`## Pitfalls` alone was larger than the largest sibling skill in the entire profile,
and it was 85 flat bullets with no subheadings.

## What was done

`## Pitfalls` extracted into 11 topic-grouped `references/pitfalls-*.md` pages, with a
one-line routing stub left in SKILL.md per entry: bold label, symptom clause, and the
entry's **key command**. 13 of the 85 bullets already ended in a `references/…`
pointer, so this extends an established pattern rather than inventing one.

One bullet (`**Sage portal username for storage auth**`, 213 chars) appeared **twice,
verbatim**, and was collapsed to one copy. All other 84 blocks are on the pages
byte-for-byte — verified by substring assertion, not by eye.

| | chars |
| --- | ---: |
| before | 117,644 |
| after | **85,771** |
| headroom under 100,000 | 14,229 |

## The A/B, and what it caught

Control = the released 1.3.0 tree. Treatment = the split tree. `retrieval_eval.py`,
BM25, k ∈ {1,2,3,5}, no LLM.

**The first run's result was misleading.** The 15 original v2 tasks returned 15/15
`both_pass` at every k — zero regression, and zero signal: *none of those tasks probe
pitfall content*. Grading a change to `## Pitfalls` against tasks that never retrieve
it measures nothing. A clean sheet from the wrong instrument is not evidence.

So 15 new probes were written against pitfall content specifically
(`evals/pitfall_probes.json`), each phrased as the symptom a student would type.

| suite | k=1 | k=2 | k=3 | k=5 |
| --- | --- | --- | --- | --- |
| pitfall probes (15) | 8 IMP / 0 REG | 8 IMP / **1 REG** | 8 IMP / 0 REG | 4 IMP / 0 REG |
| original v2 tasks (15) | 15 both_pass | 15 both_pass | 15 both_pass | 15 both_pass |

The targeted suite found a **real regression** the original suite could not see:
`P04-k3s-reimport` fell from pass to fail. Two causes, both fixed:

1. **The stub dropped the searchable token.** The trimmed one-liner lost
   `sudo docker save … | sudo k3s ctr images import -`, the exact string a searcher
   types. Fixed generally, not for P04: every stub now carries its block's key
   command span.
2. **A catch-all group acted as noise.** `pitfalls-workflow-and-docs` mixed doc
   discipline, SSH/tmux and notifications, so it matched many queries weakly and
   outranked the correct page. Split into `pitfalls-doc-surfaces`,
   `pitfalls-dev-workflow-and-access`, and `pitfalls-secrets-and-notifications`
   (9 groups → 11).

After both fixes, k=3 and k=5 are clean. **One regression remains at k=2 only**, and
it is reported rather than tuned away: the correct page sits at rank 3, so k=2 misses
it while k=1 fails in both arms. Chasing it would mean fitting the corpus to one probe.

## Why the split helps retrieval, mechanically

A 117k SKILL.md is one enormous BM25 document that matches *something* in nearly every
query. Measured across all 30 queries:

| | SKILL.md in top-3 | median rank |
| --- | --- | --- |
| control (117k monolith) | 10/30 | 6 |
| split (86k) | 5/30 | 7 |

Control's SKILL.md ranks higher more often — but as a **catch-all**, not a precise
match. That is exactly why 8 probes improved: a focused page beats a monolith on its
own topic. It is also exactly why P04 regressed at k=2 — content guaranteed-present in
a document that always ranks becomes one hop away. Both directions are the same
mechanism, and the honest summary is that the split trades a broad weak signal for a
narrow strong one.

## Held back

- **`## See Also` (20,492 chars, 88 entries)** — not compressed. The hard limit is
  already met with 14k to spare, and compressing it in the same commit would put two
  variables in one A/B. It is the obvious next lever if more headroom is wanted.
- **35 of 130 `references/` pages are never cited** from SKILL.md — unreachable by an
  agent reading the index. Costs no chars (references do not count toward the cap) but
  is the same disease: material added without a routing path. Left for its own pass.
- **Splitting into multiple skills** (`sage-waggle-plugin-dev`, `-ops`, …) is the only
  route to the 8-14k peer range, but it changes the `description`/`triggers` surface
  every turn and invalidates this baseline. Not forced by the limit; door left open.

## Reproduce

```
python3 tools/retrieval_eval.py --control <released 1.3.0 sage-waggle> \
    --treatment <1.4.0 sage-waggle> --tasks evals/pitfall_probes.json \
    --out /tmp/out.json --k 3
```

`tools/split_pitfalls.py` + `tools/split_groups.py` regenerate the pages and stubs
deterministically from `## Pitfalls`.

## Lesson for the write-up

This is the third instance in the pass of the same failure: **an instrument that
cannot see the thing being changed reports success.** v1's bag-of-words A/B
over-credited control; the wrong control tree was used twice; and here the original
task suite returned a perfect score on a change it did not measure. The 15/15 was
true and worthless. Whenever the artifact under test changes, ask what would have to
appear in the eval for a failure to be visible — and if nothing would, the eval is
not evidence.
