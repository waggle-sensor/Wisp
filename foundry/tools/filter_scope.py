#!/usr/bin/env python3
"""Filter a graphify graph.json to nodes whose source_file is under a prefix.

Used to build the sage-waggle-scoped figure: within that subtree the only
thing that changed between the two releases is the mined reference pages, so
the mining gain is the sole variable. Whole-profile graphs cannot show this --
they are dominated by unrelated skill growth.

Keeps an edge only when BOTH endpoints survive the node filter.
"""
import json, sys, collections

def main(src, dst, prefix):
    g = json.load(open(src))
    keep = {n["id"] for n in g["nodes"]
            if str(n.get("source_file", "")).startswith(prefix)}
    nodes = [n for n in g["nodes"] if n["id"] in keep]
    links = [e for e in g["links"]
             if e.get("source") in keep and e.get("target") in keep]
    out = {k: v for k, v in g.items() if k not in ("nodes", "links", "hyperedges", "graph")}
    out["graph"] = {}
    out["nodes"] = nodes
    out["links"] = links
    out["hyperedges"] = []
    json.dump(out, open(dst, "w"))
    files = {str(n.get("source_file", "")) for n in nodes}
    refs = {f for f in files if "/references/" in f}
    pit = {f for f in files if "pitfalls-" in f}
    print(f"{dst}: {len(nodes)} nodes, {len(links)} edges, "
          f"{len(files)} files ({len(refs)} references/, {len(pit)} pitfalls-)")
    return len(nodes), len(links), len(files), len(refs), len(pit)

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
