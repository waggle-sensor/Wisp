# Figure 1 — sage-waggle knowledge subgraph, 1.1.0 vs 1.4.0

Two interactive Graphify renders, scoped to `skills/sage-waggle/**`, plus a
static two-panel export of the same pair for print.

| File | Release | Built at | Nodes | Edges | Pages | `pitfalls-*` |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `fig1a-sage-waggle-1.1.0.html` | 1.1.0 (pre-mining) | `396c687` 2026-08-10 | 178 | 129 | 108 | 0 |
| `fig1b-sage-waggle-1.4.0.html` | 1.4.0 | `233d5ef` 2026-09-03 | 203 | 147 | 133 | 11 |

`fig1-sage-waggle.png` (300 dpi) and `fig1-sage-waggle.svg` are the print
version: both releases side by side, laid out **once on the union of the two
graphs** with a fixed seed, so a node present in both panels sits at identical
coordinates. The visible difference is therefore the added nodes and not a
reshuffled layout. Page titles are deliberately not printed: the interactive
renders beside these carry them on hover, and the static pair is for showing
the shape of the delta at a glance.

**One interval, but coloured by kind.** 1.1.0 and 1.4.0 are the only two commits
at which the shipped graph was rebuilt, so they are the only two states that
exist to compare; the figure treats 1.4.0 as the next version of the profile and
does not break out the minor releases in between. What it does keep separate is
the *kind* of addition, because that is the confound (paper §4.6): **10 pages
came from mining transcripts**, 11 are the `pitfalls-*` pages the size-cap split
re-routed from content the skill already had, and 5 are neither (v1's three
pages, the subtree container node, and one page the 1.1.0 graph had failed to
index). Colouring all 25 alike would credit mining with 2.5x its actual
contribution. Candidate placements are read from
`candidates/HV2-*/candidate.yaml` at render time, so the figure cannot silently
disagree with the corpus.

Build commits are the `built_at_commit` field recorded in each `graph.json`, not
the branch tip; versions are `distribution.yaml` at those commits. Note the 1.1.0
graph indexes 108 of the 109 markdown pages in its own tree — it missed
`cloud-trigger-patterns.md` — so one node reads as added when it is really a stale
baseline artifact. See §4.6.

**Why scoped and not whole-profile.** Across the whole profile the graph grows
12,966 -> 13,243 nodes, but only 26 of the 349 newly contributing files are in
`sage-waggle`; the rest is unrelated skill growth over the same interval. The
curated visualization is worse: it excludes `**/references/**`, and every mined
page is a reference page, so the mining contribution renders as zero dots there.
Scoping to `sage-waggle` removes the unrelated-skill growth, though it does not
by itself isolate mining: the interval also contains v1's pages and the
size-cap split, which is why the figure colours by kind. No files were removed
from the subtree and no unrelated work landed in it. One *node* did drop — the
bare `pywaggle` concept node that Graphify had extracted from `SKILL.md`, which
disappeared when the split moved that content into routed pages. It is ringed in
panel (a). The other 17 pywaggle-related nodes survive and 1.4.0 adds 4 more.
See paper §4.6.

## Regenerate

Requires the two `graphify-baseline.tar.gz` artifacts and a graphify venv.

```bash
# 1. extract the full graph from each release
for ref in <baseline-ref> <treatment-ref>; do
  git show "$ref:hermes-profile/graphify-baseline.tar.gz" > /tmp/$ref.tgz
  mkdir -p /tmp/full-$ref && tar -xzf /tmp/$ref.tgz -C /tmp/full-$ref
done

# 2. scope each to the mining target
python3 tools/filter_scope.py /tmp/full-<ref>/graphify-out/graph.json \
        /tmp/sw-<ref>.json 'skills/sage-waggle/'

# 3. render (graphify venv; layout only, no LLM and no GPU)
python3 tools/render_scoped.py /tmp/sw-<ref>.json fig1x.html
```

```bash
# 4. static export (needs matplotlib + networkx; no graphify, no GPU)
python3 tools/render_static.py /tmp/sw-<baseline>.json /tmp/sw-<treatment>.json \
        figures/fig1-sage-waggle
```

`filter_scope.py` keeps an edge only when both endpoints survive the node filter.
`render_scoped.py` rebuilds the community map from the surviving nodes'
`community` / `community_name` attributes and calls `graphify.export.to_html`.
`render_static.py` pins `SEED = 20260904`; changing it changes the picture but
not the counts.

Both files were checked for absolute paths before commit; neither contains any.

---

# Figure 2 — the same two releases at whole-profile scope

The zoomed-out companion. Figure 1 asks *what did mining add to sage-waggle*;
Figure 2 asks *how large is that against everything else the harness carries*.

| File | Release | Built at | Nodes | Edges | sage-waggle nodes | Skill groups |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| `fig2a-overview-1.1.0.html` | 1.1.0 (pre-mining) | `396c687` 2026-08-10 | 666 | 357 | 131 | 13 |
| `fig2b-overview-1.4.0.html` | 1.4.0 | `233d5ef` 2026-09-03 | 777 | 390 | 156 | 15 |

`fig2-profile-overview.png` (300 dpi) and `.svg` are the print pair, sharing
Figure 1's union-layout technique and the same `SEED = 20260904`. Colour marks
sage-waggle in blue, the ten mined pages in red, and the eleven `pitfalls-*`
pages from the size-cap split in orange; every other skill is one grey bucket.
Per-skill hues were tried and dropped — a legend cannot name thirteen
unlabelled colours, so the reader could never tell which was which, and the
noise competed with the delta the figure exists to show. At this scale the
twenty-one added pages are twenty-one dots in a field of 777, which is the
point.

**Why this had to be rebuilt rather than reused.** The profile ships a curated
graph for humans (`agent-knowledge-graph.html`, from
`graphify-baseline-viz.tar.gz`). That tarball is *byte-identical* at 1.1.0 and
1.4.0 — blob `78ad763`, built at `868d039`, 2026-08-07 — so it was never rebuilt
across the releases this paper compares and cannot show what mining added. Worse,
the curated `.graphifyignore` excludes `**/references/**`, and every mined page
is a reference page: even a fresh build of the shipped curated scope would render
the mining as **exactly zero dots**. `tools/filter_curated.py` reproduces that
scope from the full graph and then re-admits one subtree with `--keep`, which is
what puts the harness at skill-card resolution and sage-waggle at page
resolution in the same picture.

**Communities are regrouped by skill.** The `community` ids in the full graph are
Louvain clusters over 13,243 nodes; filtering to curated scope shreds them — 777
surviving nodes landed in 420 communities, 297 of them singletons — which colours
the interactive render as noise. `--regroup-by-skill` assigns one community per
skill and pools skills contributing fewer than 5 nodes into a single
`other skills (N)` bucket; the `--keep` scope is exempt from pooling. The
interactive renders colour by that grouping and name it on hover. The static
export does not: it collapses everything outside the `--keep` scope into one
bucket, because a printed legend has no room to name the groups.

`filter_curated.py` mirrors `hermes-profile/.graphifyignore.curated` at
`233d5ef`. If that file changes, the tool must change with it.

## Regenerate

Steps 1 of Figure 1 above produces the full graphs. Then:

```bash
# 2. curated scope, sage-waggle re-admitted, communities regrouped by skill
python3 tools/filter_curated.py /tmp/full-<ref>/graphify-out/graph.json \
        /tmp/curated-<ref>.json --keep 'skills/sage-waggle/' --regroup-by-skill

# 3. interactive render (graphify venv)
python3 tools/render_scoped.py /tmp/curated-<ref>.json fig2x.html '<title>'

# 4. static export (matplotlib + networkx + scipy; no graphify, no GPU)
python3 tools/render_overview.py /tmp/curated-<baseline>.json \
        /tmp/curated-<treatment>.json figures/fig2-profile-overview
```

`render_overview.py` reads the ten placements from `candidates/HV2-*/candidate.yaml`
at render time, as Figure 1 does, and detects the split pages by the `pitfalls-`
filename prefix. Both static exports are deterministic: re-running either
reproduces the PNG byte for byte.
