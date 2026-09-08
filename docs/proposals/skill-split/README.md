# sage-waggle SKILL.md split — profile 1.4.0

Released on `hermes-profile-1.4.0-skill-split`, cut from the 1.3.0 release branch.

## What changed

`skills/sage-waggle/SKILL.md` was **117,644 chars against a 100,000-char limit**
(`MAX_SKILL_CONTENT_CHARS`, documented in
`skills/software-development/hermes-agent-skill-authoring/SKILL.md`). It is a
character cap, not bytes. Being over it makes `skill_manage action=patch` abort.

`## Pitfalls` — 50,556 chars, 43% of the file, 85 flat bullets — was extracted into
11 topic-grouped pages under `references/pitfalls-*.md`. SKILL.md keeps a one-line
routing stub per entry: bold label, symptom, and the entry's key command.

| | chars |
| --- | ---: |
| 1.3.0 | 117,644 |
| **1.4.0** | **85,771** |
| headroom | 14,229 |

For scale: the next-largest skill in this profile is `graphify` at 38,370 chars and
the median of 250 skills is ~12,000. The authoring guide asks for 8-14k and says to
split past 20k.

## Content integrity

84 of 85 pitfall entries are on the new pages **byte-for-byte**. The 85th
(`**Sage portal username for storage auth**`) was an exact duplicate of another
bullet and was collapsed to one copy. All 11 pages are linked from SKILL.md and no
`references/` citation dangles.

## Verified by A/B

BM25 retrieval + actionability, control = the released 1.3.0 tree, k in {1,2,3,5}.
Two suites: the 15 original v2 tasks, and 15 new probes written specifically against
pitfall content (`skills/sage-waggle/evals/pitfall_probes.json`).

| suite | k=1 | k=2 | k=3 | k=5 |
| --- | --- | --- | --- | --- |
| pitfall probes | 8 IMP / 0 REG | 8 IMP / **1 REG** | 8 IMP / 0 REG | 4 IMP / 0 REG |
| original v2 tasks | 15 both_pass | 15 both_pass | 15 both_pass | 15 both_pass |

The original suite's perfect score is **not** the evidence here — none of those tasks
retrieve pitfall content, so they could not have detected a regression. The targeted
probes did: one fell from pass to fail and drove two fixes (stubs now carry their key
command; the catch-all group was split). Full account in `notes/04-skill-split.md` in
the logs repo.

## Known issues carried into 1.4.0

- **One probe still regresses at k=2** (`P04-k3s-reimport`): the correct page ranks 3,
  so k=2 misses it. Reported rather than tuned away — fixing it would mean fitting the
  corpus to a single probe. Clean at k=3 and k=5.
- **`## See Also` is still 20,492 chars** across 88 entries. Not compressed here: the
  hard limit is met with 14k to spare and touching it would put a second variable in
  this A/B. It is the next lever if more headroom is needed.
- **35 of 130 `references/` pages are never cited** from SKILL.md, so an agent reading
  the index cannot reach them. Costs no chars, but is the same disease as the one this
  release fixes.
- **Peer range still not met.** 85,771 is compliant but far from the 8-14k peers. Only
  a multi-skill split gets there, which changes the `description`/`triggers` surface
  every turn and needs its own A/B.

## Reproduce

`tools/split_pitfalls.py` and `tools/split_groups.py` (logs repo) regenerate the pages
and stubs deterministically from the `## Pitfalls` section.
