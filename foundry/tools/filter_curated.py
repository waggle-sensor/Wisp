#!/usr/bin/env python3
"""Reduce a full graphify graph to the CURATED overview scope, optionally
re-admitting one subtree.

Why this exists. The profile ships two graphs: a full one for agent queries and
a curated one for humans (`agent-knowledge-graph.html`). The curated
`.graphifyignore` drops `**/references/**` -- and every transcript-mined page is
a reference page, so the mined work is *exactly zero dots* in the artifact a
reader would naturally be shown (paper 4.6). Re-admitting one subtree with
--keep gives the zoomed-out view with the mining actually visible in it: the
rest of the harness at skill-card resolution, sage-waggle at page resolution.

We rebuild the curated scope here rather than reuse the shipped
`graphify-baseline-viz.tar.gz` because that tarball is byte-identical at 1.1.0
and 1.4.0 -- it was never rebuilt across the releases this paper compares, so it
cannot show what mining added. The rules below mirror
`hermes-profile/.graphifyignore.curated` at 233d5ef; if that file changes, this
must change with it.

Communities are re-grouped by skill (--regroup-by-skill). The community ids in
the full graph are Louvain clusters over the whole 13k-node graph; filtering to
the curated scope shreds them (777 nodes landed in 420 communities, 297 of them
singletons), which colours the render as noise. One community per skill is both
more legible and a truer description of how the harness is actually organised.

Usage: filter_curated.py <full-graph.json> <out.json> [--keep <prefix>]
                         [--regroup-by-skill]
"""
import collections
import json
import sys

# Mirrors .graphifyignore.curated. Kept as literal tuples rather than globs so
# the mapping back to that file stays obvious on review.
CODE_EXT = (".py", ".sh", ".ts", ".js", ".jsx", ".tsx", ".go", ".java", ".cu",
            ".cpp", ".c", ".h", ".hpp", ".yaml", ".yml", ".json", ".toml",
            ".xml", ".onnx", ".pt", ".engine")
MEDIA_EXT = (".mp4", ".mkv", ".wav", ".flac", ".png", ".jpg", ".jpeg", ".gif",
             ".webp")
OTHER_EXT = (".pyc", ".lock", ".db", ".sig", ".tar.gz")
DIR_EXCL = frozenset({"evals", "eval", "scripts", "validators", "fixtures",
                      "tests", "test", "examples", "schemas", "templates",
                      "assets", "prompts", "references", "__pycache__",
                      ".pytest_cache", ".claude-plugin", "graphify-out"})
ROOT_EXCL = ("home/", "pastes/", "cron/", "logs/", "sessions/")

# Inside a re-admitted subtree we still drop code, media and eval/test trees --
# the point is to surface its prose pages, not to dump its implementation.
KEEP_DIR_EXCL = frozenset({"evals", "eval", "scripts", "tests", "test",
                           "__pycache__"})


def curated_keep(source_file, keep_scope=None):
    p = str(source_file or "").replace("\\", "/")
    if not p:
        return False
    parts = p.split("/")
    if keep_scope and p.startswith(keep_scope):
        if p.endswith(MEDIA_EXT):
            return False
        if p.startswith("skills/") and p.endswith(CODE_EXT):
            return False
        return not any(seg in KEEP_DIR_EXCL for seg in parts)
    if p.startswith(ROOT_EXCL):
        return False
    if p.startswith("skills/_vendor/"):
        return False
    if p.endswith(MEDIA_EXT) or p.endswith(OTHER_EXT):
        return False
    if p.startswith("skills/") and p.endswith(CODE_EXT):
        return False
    return not any(seg in DIR_EXCL for seg in parts)


def skill_group(source_file):
    """Top-level grouping: the skill a page belongs to, else profile docs."""
    parts = str(source_file or "").replace("\\", "/").split("/")
    if len(parts) > 1 and parts[0] == "skills":
        return parts[1]
    return "(profile docs)"


def regroup_by_skill(nodes, min_size=5, always_keep=()):
    """Replace inherited community ids with one community per skill.

    Skills contributing fewer than min_size nodes are pooled into a single
    "other skills" group: at curated resolution most skills contribute one or
    two cards, and 255 separate colours is noise, not information. Anything in
    always_keep survives the pooling regardless of size.
    """
    counts = collections.Counter(skill_group(n.get("source_file")) for n in nodes)
    keep = {g for g, c in counts.items() if c >= min_size} | set(always_keep)
    pooled = f"other skills ({len(counts) - len(keep)})"
    names = sorted(keep) + ([pooled] if len(keep) < len(counts) else [])
    ids = {name: i for i, name in enumerate(names)}
    for n in nodes:
        g = skill_group(n.get("source_file"))
        g = g if g in keep else pooled
        n["community"] = ids[g]
        n["community_name"] = g
    return len(names)


def main(src, dst, keep_scope=None, regroup=False):
    g = json.load(open(src))
    keep = {n["id"] for n in g["nodes"]
            if curated_keep(n.get("source_file"), keep_scope)}
    nodes = [n for n in g["nodes"] if n["id"] in keep]
    links = [e for e in g["links"]
             if e.get("source") in keep and e.get("target") in keep]
    keep_name = skill_group(keep_scope + "x") if keep_scope else None
    ncomm = (regroup_by_skill(nodes, always_keep=(keep_name,) if keep_name else ())
             if regroup else None)
    out = dict(g)
    out["nodes"], out["links"] = nodes, links
    json.dump(out, open(dst, "w"))
    scoped = sum(1 for n in nodes
                 if str(n.get("source_file", "")).startswith(keep_scope or "\0"))
    print(f"{dst}: {len(nodes)} nodes, {len(links)} links"
          + (f", {scoped} in {keep_scope}" if keep_scope else "")
          + (f", {ncomm} skill groups" if ncomm else ""))


if __name__ == "__main__":
    args = sys.argv[1:]
    regroup = "--regroup-by-skill" in args
    args = [a for a in args if a != "--regroup-by-skill"]
    keep = None
    if "--keep" in args:
        i = args.index("--keep")
        keep = args[i + 1]
        args = args[:i] + args[i + 2:]
    main(args[0], args[1], keep, regroup)
