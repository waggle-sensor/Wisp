#!/usr/bin/env python3
"""Render a scoped graphify subgraph (from filter_scope.py) to interactive HTML.

Rebuilds the community map from the surviving nodes' own community /
community_name attributes, then calls graphify's HTML exporter. Layout only --
no LLM call, no GPU. Must run under the graphify venv.

Usage: render_scoped.py <scoped.json> <out.html> [title]
"""
import json, sys
import networkx as nx
from networkx.readwrite import json_graph
from graphify.export import to_html

src, dst, title = sys.argv[1], sys.argv[2], sys.argv[3]
data = json.load(open(src))
G = json_graph.node_link_graph(data, edges="links")
# communities: {cid: [node ids]} derived from the node attribute
comms = {}
labels = {}
for nid, d in G.nodes(data=True):
    c = d.get("community")
    if c is None:
        continue
    comms.setdefault(int(c), []).append(nid)
    if d.get("community_name"):
        labels[int(c)] = d["community_name"]
ok = to_html(G, comms, dst, community_labels=labels or None, node_limit=5000)
print(f"{dst}: written={ok} nodes={G.number_of_nodes()} edges={G.number_of_edges()} communities={len(comms)}")
