#!/usr/bin/env python3
"""Render scoped subgraphs (from filter_scope.py) to print-ready PNG + SVG.

Both panels are laid out ONCE on the union of the two graphs, then each is
drawn with those shared positions. A node present in both releases therefore
sits at the same coordinates in both panels, so the visible difference is the
added nodes and not a reshuffled layout -- which is the whole point of the
figure. Layout is seeded, so re-running reproduces the same image.

Additions are reported against 1.4.0 as a single step. The shipped graph was
only ever rebuilt at 1.1.0 and 1.4.0, so those are the only two states that
exist to compare; the releases in between were minor and the figure treats
1.4.0 as the next version of the profile.

What the figure does keep separate is the *kind* of addition, because that is
the confound paper 4.6 turns on: of the 25 added pages only 10 came from
mining transcripts, 11 are the size-cap split rerouting content the skill
already had, and 4 are neither. Colouring all 25 alike would
credit mining with the whole delta. Candidate placements are read from
candidates/HV2-*/candidate.yaml rather than hardcoded, so the figure cannot
silently disagree with the corpus.

Usage: render_static.py <baseline.json> <treatment.json> <out-prefix>
Writes <out-prefix>.png (300 dpi) and <out-prefix>.svg.
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

SEED = 20260904            # fixed: the figure must be reproducible
CARRIED_COLOR = "#b8c4d0"  # present in both releases
MINED_COLOR = "#d62728"    # HV2-0001..0010, mined from student transcripts
SPLIT_COLOR = "#1f77b4"    # pitfalls-* pages routed by the size-cap split
OTHER_COLOR = "#8c8c3f"    # other pages added over the interval
DROPPED_COLOR = "#444444"  # in 1.1.0, gone in 1.4.0

CAND_DIR = pathlib.Path(__file__).resolve().parent.parent / "candidates"

def candidate_placements():
    """The 10 v2 candidate pages, read from the candidate manifests."""
    out = set()
    for y in sorted(CAND_DIR.glob("HV2-*/candidate.yaml")):
        m = re.search(r'^placement:\s*"?([^"\n]+?)"?\s*$', y.read_text(), re.M)
        if m:
            out.add(m.group(1))
    return out


def load(path):
    d = json.load(open(path))
    G = nx.Graph()
    for n in d["nodes"]:
        G.add_node(n["id"], **n)
    for e in d["links"]:
        if e.get("source") in G and e.get("target") in G:
            G.add_edge(e["source"], e["target"])
    return G


def classify(G, carried_ids, placements, dropped=()):
    """Bucket nodes into carried / mined / split / other-added.

    Dropped nodes ride in the carried bucket: they were present in 1.1.0, so
    in panel (a) they should read as baseline content, not as an addition.
    The open ring drawn over them is what marks them as dropped.
    """
    buckets = {"carried": [], "mined": [], "split": [], "other": []}
    for nid, d in G.nodes(data=True):
        src = str(d.get("source_file", ""))
        if nid in carried_ids or nid in dropped:
            buckets["carried"].append(nid)
        elif src in placements:
            buckets["mined"].append(nid)
        elif pathlib.PurePath(src).name.startswith("pitfalls-"):
            buckets["split"].append(nid)
        else:
            buckets["other"].append(nid)
    return buckets


def draw(ax, G, pos, carried_ids, placements, title, dropped=()):
    b = classify(G, carried_ids, placements, dropped)
    nx.draw_networkx_edges(ax=ax, G=G, pos=pos, edge_color="#d8dee6",
                           width=0.6, alpha=0.85)
    for key, color, size in (("carried", CARRIED_COLOR, 13),
                             ("other", OTHER_COLOR, 30),
                             ("split", SPLIT_COLOR, 30),
                             ("mined", MINED_COLOR, 44)):
        if b[key]:
            nx.draw_networkx_nodes(ax=ax, G=G, pos=pos, nodelist=b[key],
                                   node_color=color, node_size=size,
                                   linewidths=0.3, edgecolors="white")
    if dropped:
        nx.draw_networkx_nodes(ax=ax, G=G, pos=pos, nodelist=list(dropped),
                               node_color="none", node_size=95,
                               linewidths=1.3, edgecolors=DROPPED_COLOR)
    ax.set_title(title, fontsize=11, pad=8)
    ax.set_axis_off()
    return b


def main(base_path, treat_path, out_prefix):
    A, B = load(base_path), load(treat_path)
    placements = candidate_placements()
    carried = set(A.nodes) & set(B.nodes)
    dropped = set(A.nodes) - set(B.nodes)

    # One layout over the union -> shared coordinates in both panels.
    U = nx.compose(A, B)
    pos = nx.spring_layout(U, seed=SEED, k=1.0, iterations=600)

    fig, axes = plt.subplots(1, 2, figsize=(14, 6.6))
    ba = draw(axes[0], A, pos, carried, placements,
              f"(a) 1.1.0 - baseline graph, pre-mining\n{A.number_of_nodes()} nodes, "
              f"{A.number_of_edges()} edges", dropped=dropped)
    bb = draw(axes[1], B, pos, carried, placements,
              f"(b) 1.4.0 - after mining and the size-cap split\n{B.number_of_nodes()} nodes, "
              f"{B.number_of_edges()} edges")

    def dot(color, size, label):
        return Line2D([], [], marker="o", linestyle="", markersize=size,
                      markerfacecolor=color, markeredgecolor="white",
                      label=label)

    handles = [
        dot(CARRIED_COLOR, 5, "present in both releases"),
        dot(MINED_COLOR, 8, "added by mining"),
        dot(SPLIT_COLOR, 6.5, "added by the size-cap limit split"),
        dot(OTHER_COLOR, 6, "added otherwise over the interval"),
        Line2D([], [], marker="o", linestyle="", markersize=8,
               markerfacecolor="none", markeredgecolor=DROPPED_COLOR,
               markeredgewidth=1.3, label="dropped in 1.4.0"),
    ]
    fig.legend(handles=handles, loc="lower center", ncol=5, frameon=False,
               fontsize=8.5, bbox_to_anchor=(0.5, 0.005))
    fig.suptitle("Sage Hermes Profile: Knowledge Subgraph of sage-waggle skill "
                 "from 1.1.0 to 1.4.0",
                 fontsize=12.5, y=0.975)
    fig.tight_layout(rect=(0, 0.06, 1, 0.955))

    for ext, kw in (("png", {"dpi": 300}), ("svg", {})):
        fig.savefig(f"{out_prefix}.{ext}", bbox_inches="tight", **kw)

    fmt = lambda b: " ".join(f"{k}={len(v)}" for k, v in b.items())
    print(f"{out_prefix}.png / .svg")
    print(f"  (a) {fmt(ba)} dropped={len(dropped)}")
    print(f"  (b) {fmt(bb)}")


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
