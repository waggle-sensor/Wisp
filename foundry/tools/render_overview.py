#!/usr/bin/env python3
"""Static PNG/SVG of the curated overview with one subtree expanded.

The zoomed-out companion to Figure 1. Figure 1 answers "what did mining add to
sage-waggle"; this answers "how big is sage-waggle, and what mining added to it,
relative to the rest of the harness". Nodes are coloured by skill so the reader
can see the mined pages in the context of everything else the profile carries.

Input is filter_curated.py output built with --regroup-by-skill, which sets
community_name to the skill (or the pooled "other skills" bucket). Only the
focus skill is coloured; every other group renders as one background bucket.

Usage: render_overview.py <baseline.json> <treatment.json> <out-prefix>
"""
import json
import pathlib
import re
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import networkx as nx

SEED = 20260904
FOCUS = "sage-waggle"
FOCUS_COLOR = "#1f77b4"
MINED_COLOR = "#d62728"    # the ten mined pages, inside the focus skill
SPLIT_COLOR = "#ff9e2c"    # the pitfalls-* pages routed by the size-cap split
OTHER_COLOR = "#ccd3d9"    # everything that is not the mining target
# The rest of the harness is one bucket, one colour. Per-skill hues were
# decoration: the legend cannot name thirteen unlabelled colours, so a reader
# could never tell which green was which skill. What the figure is for is the
# size of the mining delta against everything else, and that reads better
# when everything else is quiet.


def is_split(source_file):
    """The pitfalls-* pages the 1.4.0 size-cap split routed out of SKILL.md."""
    return pathlib.PurePath(str(source_file or "")).name.startswith("pitfalls-")


def load(path):
    d = json.load(open(path))
    G = nx.Graph()
    for n in d["nodes"]:
        G.add_node(n["id"], **n)
    for e in d["links"]:
        if e.get("source") in G and e.get("target") in G:
            G.add_edge(e["source"], e["target"])
    return G


def palette(graphs):
    """Focus skill in blue, every other group in the single background colour."""
    groups = set()
    for G in graphs:
        groups |= {str(d.get("community_name", "")) for _, d in G.nodes(data=True)}
    colors = {g: OTHER_COLOR for g in groups}
    colors[FOCUS] = FOCUS_COLOR
    return colors


def draw(ax, G, pos, colors, placements, title):
    nx.draw_networkx_edges(ax=ax, G=G, pos=pos, edge_color="#e2e6ea",
                           width=0.5, alpha=0.9)
    buckets, mined, split = {}, [], []
    for nid, d in G.nodes(data=True):
        src = str(d.get("source_file", ""))
        if src in placements:
            mined.append(nid)
        elif is_split(src):
            split.append(nid)
        else:
            buckets.setdefault(str(d.get("community_name", "")), []).append(nid)
    # Long tail first, focus skill last, so the subject sits on top.
    for g in sorted(buckets, key=lambda g: (g == FOCUS, len(buckets[g]))):
        size = 18 if g == FOCUS else 10
        nx.draw_networkx_nodes(ax=ax, G=G, pos=pos, nodelist=buckets[g],
                               node_color=colors.get(g, OTHER_COLOR),
                               node_size=size, linewidths=0, alpha=0.95)
    for nodelist, color in ((split, SPLIT_COLOR), (mined, MINED_COLOR)):
        if nodelist:
            nx.draw_networkx_nodes(ax=ax, G=G, pos=pos, nodelist=nodelist,
                                   node_color=color, node_size=46,
                                   linewidths=0.4, edgecolors="white")
    ax.set_title(title, fontsize=11, pad=8)
    ax.set_axis_off()
    return mined, split


def candidate_placements():
    """The ten v2 candidate pages, read from the candidate manifests.

    Sourced from the corpus at render time so the figure cannot drift from it.
    """
    out = set()
    cand = pathlib.Path(__file__).resolve().parent.parent / "candidates"
    for y in sorted(cand.glob("HV2-*/candidate.yaml")):
        m = re.search(r'^placement:\s*"?([^"\n]+?)"?\s*$', y.read_text(), re.M)
        if m:
            out.add(m.group(1))
    return out


def main(base_path, treat_path, out_prefix):
    A, B = load(base_path), load(treat_path)
    placements = candidate_placements()

    colors = palette([A, B])
    U = nx.compose(A, B)
    pos = nx.spring_layout(U, seed=SEED, k=0.9, iterations=400)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.8))
    draw(axes[0], A, pos, colors, placements,
         f"(a) 1.1.0 — pre-mining\n{A.number_of_nodes()} nodes across the profile")
    mined, split = draw(axes[1], B, pos, colors, placements,
                        f"(b) 1.4.0 — after mining and the size-cap split\n"
                        f"{B.number_of_nodes()} nodes across the profile")
    nb, ns = len(mined), len(split)

    def dot(c, sz, lbl):
        return Line2D([], [], marker="o", linestyle="", markersize=sz,
                      markerfacecolor=c, markeredgecolor="white", label=lbl)

    handles = [
        dot(FOCUS_COLOR, 7, "sage-waggle (the mining target)"),
        dot(MINED_COLOR, 8, "added by mining"),
        dot(SPLIT_COLOR, 8, "added by the size-cap limit split"),
        dot(OTHER_COLOR, 5, "other skills in the harness"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=4, frameon=False,
               fontsize=9, bbox_to_anchor=(0.5, 0.005))
    fig.suptitle("Sage Hermes profile: Curated Knowledge Graph with sage-waggle skill "
                 "from 1.1.0 to 1.4.0",
                 fontsize=12.5, y=0.975)
    fig.tight_layout(rect=(0, 0.06, 1, 0.955))

    for ext, kw in (("png", {"dpi": 300}), ("svg", {})):
        fig.savefig(f"{out_prefix}.{ext}", bbox_inches="tight", **kw)
    print(f"{out_prefix}.png / .svg  |  (a) {A.number_of_nodes()} nodes  "
          f"(b) {B.number_of_nodes()} nodes, {nb} mined, {ns} split")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
