#!/usr/bin/env python3
"""Embed the four figure HTMLs into figures/compare-graphs.html.

The comparison page must be self-contained: browsers block sibling iframes
when the page is opened as a file, and Cursor's preview often does the same.
"""
from __future__ import annotations

import html as htmlmod
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIGURES = ROOT / "figures"

GRAPHS = [
    {
        "key": "fig1a",
        "file": "fig1a-sage-waggle-1.1.0.html",
        "title": "Figure 1a: sage-waggle skill, release 1.1.0",
        "fig": "1",
        "scope": "Zoom · sage-waggle only",
        "meta": "Fig 1a · 1.1.0 · 178 nodes",
        "loading": "Loading sage-waggle graph…",
    },
    {
        "key": "fig1b",
        "file": "fig1b-sage-waggle-1.4.0.html",
        "title": "Figure 1b: sage-waggle skill, release 1.4.0",
        "fig": "1",
        "scope": "Zoom · sage-waggle only",
        "meta": "Fig 1b · 1.4.0 · 203 nodes",
        "loading": "Loading sage-waggle graph…",
    },
    {
        "key": "fig2a",
        "file": "fig2a-overview-1.1.0.html",
        "title": "Figure 2a: all skills, release 1.1.0",
        "fig": "2",
        "scope": "All skills",
        "meta": "Fig 2a · 1.1.0 · 666 nodes · 13 skill groups",
        "loading": "Loading all-skills graph…",
    },
    {
        "key": "fig2b",
        "file": "fig2b-overview-1.4.0.html",
        "title": "Figure 2b: all skills, release 1.4.0",
        "fig": "2",
        "scope": "All skills",
        "meta": "Fig 2b · 1.4.0 · 777 nodes · 15 skill groups",
        "loading": "Loading all-skills graph…",
    },
]

TILE_CSS = """
    html, body { height: 100% !important; width: 100% !important; }
    html:not(.show-sidebar) #sidebar { display: none !important; }
    html.show-sidebar #sidebar { display: flex !important; }
    #graph { flex: 1 1 auto; min-width: 0; min-height: 0; }
"""


PALETTE = [
    "#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F",
    "#EDC948", "#B07AA1", "#FF9DA7", "#9C755F", "#BAB0AC",
    "#8CD17D", "#B6992D", "#499894", "#D37295", "#A0CBE8",
]


def _parse_js_array(html: str, name: str) -> tuple[list, re.Match[str]]:
    m = re.search(rf"const {name} = (\[.*\]);", html)
    if not m:
        raise ValueError(f"missing const {name}")
    return json.loads(htmlmod.unescape(m.group(1))), m


def _dump_js_array(obj: list) -> str:
    return json.dumps(obj, ensure_ascii=False, separators=(", ", ": ")).replace(
        "<", "\\u003c"
    )


def _node_hex(node: dict) -> str:
    color = node.get("color") or {}
    if isinstance(color, dict):
        return str(color.get("background") or "#BAB0AC")
    return str(color)


def _paint(hex_color: str) -> dict:
    return {
        "background": hex_color,
        "border": hex_color,
        "highlight": {"background": "#ffffff", "border": hex_color},
    }


def _group_key(label: str) -> str:
    label = htmlmod.unescape(label or "")
    if label.startswith("other skills"):
        return "other skills"
    return label


SAGE_WAGGLE_PURPLE = "#8B5CF6"
OTHER_SKILLS_GREEN = "#3D9B4A"
# Greens that would compete with "other skills" on Figure 2.
GREEN_HEXES = {
    OTHER_SKILLS_GREEN,
    "#59A14F",
    "#8CD17D",
    "#43A047",
    "#2CA02C",
    "#37A34A",
}


def _norm_hex(color: str) -> str:
    return (color or "").upper()


def _write_nodes_and_legend(html: str, nodes: list, legend: list, legend_m: re.Match[str]) -> str:
    html = (
        html[: legend_m.start(1)]
        + _dump_js_array(legend)
        + html[legend_m.end(1) :]
    )
    nodes_m = re.search(r"const RAW_NODES = (\[.*\]);", html)
    if not nodes_m:
        raise ValueError("missing const RAW_NODES after legend rewrite")
    return html[: nodes_m.start(1)] + _dump_js_array(nodes) + html[nodes_m.end(1) :]


def _paint_by_name(html: str, name_to_color: dict[str, str]) -> str:
    nodes, _ = _parse_js_array(html, "RAW_NODES")
    legend, legend_m = _parse_js_array(html, "LEGEND")
    for node in nodes:
        key = _group_key(node.get("community_name") or "")
        if key in name_to_color:
            node["color"] = _paint(name_to_color[key])
    for entry in legend:
        key = _group_key(entry["label"])
        if key in name_to_color:
            entry["color"] = name_to_color[key]
    return _write_nodes_and_legend(html, nodes, legend, legend_m)


def apply_fig2_focus_colors(html: str) -> str:
    """sage-waggle is purple; the pooled other-skills bucket is green.
    Any other Figure 2 community that was already green is moved off that hue.
    """
    legend, _ = _parse_js_array(html, "LEGEND")
    name_to_color = {_group_key(e["label"]): e["color"] for e in legend}
    reserved = {_norm_hex(SAGE_WAGGLE_PURPLE), _norm_hex(OTHER_SKILLS_GREEN)}
    used = {_norm_hex(c) for c in name_to_color.values()} | reserved

    def next_safe() -> str:
        for candidate in PALETTE:
            n = _norm_hex(candidate)
            if n not in used and n not in {_norm_hex(c) for c in GREEN_HEXES}:
                used.add(n)
                return candidate
        extras = ["#F28E2B", "#E15759", "#4E79A7", "#EDC948", "#9C755F", "#BAB0AC", "#D37295", "#499894", "#B6992D"]
        for candidate in extras:
            n = _norm_hex(candidate)
            if n not in used:
                used.add(n)
                return candidate
        return "#BAB0AC"

    for key, color in list(name_to_color.items()):
        if key in ("sage-waggle", "other skills"):
            continue
        if _norm_hex(color) in reserved or _norm_hex(color) in {_norm_hex(c) for c in GREEN_HEXES}:
            name_to_color[key] = next_safe()

    name_to_color["sage-waggle"] = SAGE_WAGGLE_PURPLE
    name_to_color["other skills"] = OTHER_SKILLS_GREEN
    return _paint_by_name(html, name_to_color)


def recolor_to_match(target_html: str, source_html: str) -> str:
    """Reuse the source graph's community colours so a name (or node id)
    present in both panels keeps the same colour. New groups take the next
    unused Tableau colour instead of shifting the whole legend.
    """
    src_legend, _ = _parse_js_array(source_html, "LEGEND")
    tgt_nodes, _ = _parse_js_array(target_html, "RAW_NODES")
    tgt_legend, legend_m = _parse_js_array(target_html, "LEGEND")

    name_to_color: dict[str, str] = {}
    for entry in src_legend:
        name_to_color[_group_key(entry["label"])] = entry["color"]

    used = set(name_to_color.values())
    extra = 0
    for entry in tgt_legend:
        key = _group_key(entry["label"])
        if key in name_to_color:
            continue
        assigned = None
        for _ in range(len(PALETTE)):
            candidate = PALETTE[extra % len(PALETTE)]
            extra += 1
            if candidate not in used:
                assigned = candidate
                used.add(candidate)
                break
        name_to_color[key] = assigned or PALETTE[extra % len(PALETTE)]

    for node in tgt_nodes:
        key = _group_key(node.get("community_name") or "")
        color = name_to_color.get(key, _node_hex(node))
        node["color"] = _paint(color)
    for entry in tgt_legend:
        entry["color"] = name_to_color[_group_key(entry["label"])]

    return _write_nodes_and_legend(target_html, tgt_nodes, tgt_legend, legend_m)


def prepare_graph_html(raw: str, *, hide_hyperedges: bool = False) -> str:
    html = raw.replace("</style>", TILE_CSS + "\n</style>", 1)
    html = html.replace(
        "const network = new vis.Network",
        "const network = window.network = new vis.Network",
        1,
    )
    if hide_hyperedges:
        html = html.replace("const hyperedges = [", "const hyperedges = []; // [", 1)
    return html


def tile_markup(spec: dict) -> str:
    return f"""  <article class="tile" data-fig="{spec['fig']}" data-key="{spec['key']}" data-src="{spec['file']}">
    <div class="tile-bar">
      <div class="label">
        <span class="scope">{spec['scope']}</span>
        <span class="meta">{spec['meta']}</span>
      </div>
      <div class="actions">
        <button type="button" class="expand">Expand</button>
      </div>
    </div>
    <div class="frame-wrap">
      <div class="loading">{spec['loading']}</div>
      <iframe title="{spec['title']}"></iframe>
    </div>
  </article>"""


PAGE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Compare graphs — sage-waggle zoom vs all skills, 1.1.0 vs 1.4.0</title>
<style>
  :root {
    --bg: #0b0b14;
    --panel: #12121f;
    --tile: #161625;
    --stroke: #2a2a4e;
    --text: #e8e8ef;
    --muted: #8b8ba0;
    --dim: #5c5c72;
    --zoom: #4E79A7;
    --wide: #F28E2B;
    --before: #76B7B2;
    --after: #59A14F;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html, body { height: 100%; }
  body {
    background: var(--bg);
    color: var(--text);
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    display: flex;
    flex-direction: column;
    overflow: hidden;
  }

  header {
    flex: 0 0 auto;
    padding: 12px 16px 10px;
    border-bottom: 1px solid var(--stroke);
    background: var(--panel);
  }
  .header-top {
    display: flex;
    align-items: flex-start;
    justify-content: space-between;
    gap: 16px;
    flex-wrap: wrap;
  }
  h1 {
    font-size: 15px;
    font-weight: 600;
    letter-spacing: 0.01em;
    line-height: 1.3;
  }
  .lede {
    margin-top: 4px;
    font-size: 12px;
    color: var(--muted);
    max-width: 72ch;
    line-height: 1.45;
  }
  .lede strong { color: var(--text); font-weight: 600; }

  .toolbar {
    display: flex;
    align-items: center;
    gap: 8px;
    flex-wrap: wrap;
  }
  .seg {
    display: flex;
    border: 1px solid var(--stroke);
    border-radius: 6px;
    overflow: hidden;
  }
  .seg button {
    background: transparent;
    color: var(--muted);
    border: 0;
    border-right: 1px solid var(--stroke);
    padding: 6px 10px;
    font-size: 12px;
    cursor: pointer;
    white-space: nowrap;
  }
  .seg button:last-child { border-right: 0; }
  .seg button:hover { color: var(--text); background: #1c1c30; }
  .seg button.active { background: #1e2a44; color: var(--text); }
  .hint {
    font-size: 11px;
    color: var(--dim);
  }

  .scope-key {
    display: flex;
    gap: 16px;
    margin-top: 10px;
    flex-wrap: wrap;
  }
  .scope-chip {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 12px;
    color: var(--muted);
  }
  .scope-chip b { color: var(--text); font-weight: 600; }
  .bar {
    width: 4px;
    height: 14px;
    border-radius: 1px;
    flex-shrink: 0;
  }
  .bar.zoom { background: var(--zoom); }
  .bar.wide { background: var(--wide); }

  .stage {
    flex: 1;
    min-height: 0;
    display: grid;
    grid-template-columns: 132px 1fr 1fr;
    grid-template-rows: 36px 1fr 1fr;
    gap: 8px;
    padding: 10px 12px 12px;
  }
  body.view-zoom .stage,
  body.view-wide .stage {
    grid-template-rows: 36px 1fr;
  }
  body.view-zoom .row-wide,
  body.view-zoom .tile[data-fig="2"],
  body.view-wide .row-zoom,
  body.view-wide .tile[data-fig="1"] {
    display: none;
  }

  .colhead {
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-size: 12px;
    letter-spacing: 0.04em;
    text-transform: uppercase;
    color: var(--muted);
    border: 1px solid var(--stroke);
    border-radius: 6px;
    background: var(--panel);
  }
  .colhead .ver {
    color: var(--text);
    font-weight: 650;
    font-size: 13px;
    letter-spacing: 0;
    text-transform: none;
  }
  .dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    flex-shrink: 0;
  }
  .dot.before { background: var(--before); }
  .dot.after { background: var(--after); }
  .corner { border: 0; background: transparent; }

  .rowhead {
    display: flex;
    flex-direction: column;
    justify-content: center;
    gap: 6px;
    padding: 10px 10px 10px 12px;
    border: 1px solid var(--stroke);
    border-radius: 6px;
    background: var(--panel);
    min-height: 0;
  }
  .rowhead.zoom { border-left: 4px solid var(--zoom); }
  .rowhead.wide { border-left: 4px solid var(--wide); }
  .rowhead .fig {
    font-size: 11px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: var(--dim);
  }
  .rowhead h2 {
    font-size: 14px;
    font-weight: 650;
    line-height: 1.25;
  }
  .rowhead p {
    font-size: 11px;
    color: var(--muted);
    line-height: 1.4;
  }

  .tile {
    position: relative;
    display: flex;
    flex-direction: column;
    min-height: 0;
    border: 1px solid var(--stroke);
    border-radius: 6px;
    overflow: hidden;
    background: var(--tile);
  }
  .tile[data-fig="1"] { border-top: 2px solid var(--zoom); }
  .tile[data-fig="2"] { border-top: 2px solid var(--wide); }
  .tile-bar {
    flex: 0 0 auto;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 8px;
    padding: 6px 8px 6px 10px;
    background: #10101c;
    border-bottom: 1px solid var(--stroke);
    font-size: 12px;
  }
  .tile-bar .label {
    display: flex;
    align-items: baseline;
    gap: 8px;
    min-width: 0;
  }
  .tile-bar .scope {
    font-weight: 650;
    white-space: nowrap;
  }
  .tile-bar .meta {
    color: var(--muted);
    overflow: hidden;
    text-overflow: ellipsis;
    white-space: nowrap;
  }
  .tile-bar .actions { display: flex; gap: 4px; flex-shrink: 0; }
  .tile-bar button {
    background: #1a1a2e;
    color: var(--muted);
    border: 1px solid var(--stroke);
    border-radius: 4px;
    padding: 3px 8px;
    font-size: 11px;
    cursor: pointer;
  }
  .tile-bar button:hover { color: var(--text); border-color: #4a4a6e; }
  .frame-wrap {
    position: relative;
    flex: 1;
    min-height: 0;
    background: #0f0f1a;
  }
  iframe {
    position: absolute;
    inset: 0;
    width: 100%;
    height: 100%;
    border: 0;
    background: #0f0f1a;
  }
  .loading {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    color: var(--dim);
    pointer-events: none;
    z-index: 1;
  }
  .tile.ready .loading { display: none; }
  .tile.failed .loading { color: #E15759; }

  .tile.expanded {
    position: fixed;
    inset: 8px;
    z-index: 40;
    border-top-width: 3px;
  }
  body.has-expanded .stage > :not(.expanded) { visibility: hidden; }

  @media (max-width: 900px) {
    .stage {
      grid-template-columns: 1fr 1fr;
      grid-template-rows: auto auto 1fr auto 1fr;
    }
    body.view-zoom .stage,
    body.view-wide .stage {
      grid-template-rows: auto auto 1fr;
    }
    .corner { display: none; }
    .rowhead { grid-column: 1 / -1; flex-direction: row; align-items: center; }
    .rowhead p { display: none; }
  }
</style>
</head>
<body>
<header>
  <div class="header-top">
    <div>
      <h1>Sage Hermes knowledge graphs &mdash; 1.1.0 vs 1.4.0</h1>
      <p class="lede">
        Four interactive knowledge graphs comparing two releases, at two zoom levels.
        Hover a node for its title; expand a tile to use search and the legend.
      </p>
    </div>
    <div class="toolbar">
      <div class="seg" role="group" aria-label="Layout">
        <button type="button" class="active" data-view="four">Four tiles</button>
        <button type="button" data-view="zoom">Zoom pair only</button>
        <button type="button" data-view="wide">All-skills pair only</button>
      </div>
      <span class="hint">Esc closes an expanded tile</span>
    </div>
  </div>
  <div class="scope-key">
    <div class="scope-chip">
      <span class="bar zoom"></span>
      <span><b>Figure 1 &mdash; zoom:</b> <code>skills/sage-waggle/**</code> only. 178 &rarr; 203 nodes. This is where added pages are legible one by one.</span>
    </div>
    <div class="scope-chip">
      <span class="bar wide"></span>
      <span><b>Figure 2 &mdash; all skills:</b> whole curated harness. 666 &rarr; 777 nodes, of which 131 &rarr; 156 are sage-waggle. The mining delta is a small local cluster.</span>
    </div>
  </div>
</header>

<main class="stage">
  <div class="corner"></div>
  <div class="colhead">
    <span class="dot before"></span>
    <span><span class="ver">1.1.0</span> &nbsp;pre-mining baseline</span>
  </div>
  <div class="colhead">
    <span class="dot after"></span>
    <span><span class="ver">1.4.0</span> &nbsp;after mining</span>
  </div>

  <div class="rowhead zoom row-zoom">
    <div class="fig">Figure 1</div>
    <h2>Zoom: sage-waggle skill</h2>
    <p>Cropped to one skill so the added pages are visible.</p>
  </div>
__TILES_ZOOM__
  <div class="rowhead wide row-wide">
    <div class="fig">Figure 2</div>
    <h2>Wide: all skills</h2>
    <p>Every skill in the curated harness. sage-waggle is one skill among many.</p>
  </div>
__TILES_WIDE__
</main>

<script>
const GRAPH_HTML = __GRAPH_HTML__;
(function () {
  const body = document.body;
  const tiles = Array.from(document.querySelectorAll(".tile"));

  function setSidebar(iframe, show) {
    try {
      const doc = iframe.contentDocument;
      if (!doc || !doc.documentElement) return;
      doc.documentElement.classList.toggle("show-sidebar", show);
    } catch (err) { /* ignore */ }
  }

  function nudgeOne(iframe) {
    try {
      const net = iframe.contentWindow && iframe.contentWindow.network;
      if (net && typeof net.fit === "function") net.fit({ animation: false });
    } catch (err) { /* ignore */ }
  }

  function nudgeNetworks() {
    tiles.forEach(function (tile) {
      const iframe = tile.querySelector("iframe");
      setSidebar(iframe, tile.classList.contains("expanded"));
      nudgeOne(iframe);
    });
  }

  function collapse() {
    tiles.forEach(function (tile) {
      tile.classList.remove("expanded");
      const btn = tile.querySelector(".expand");
      if (btn) btn.textContent = "Expand";
    });
    body.classList.remove("has-expanded");
  }

  function expand(tile) {
    const already = tile.classList.contains("expanded");
    collapse();
    if (!already) {
      tile.classList.add("expanded");
      body.classList.add("has-expanded");
      tile.querySelector(".expand").textContent = "Close";
    }
    requestAnimationFrame(nudgeNetworks);
  }

  function setView(view) {
    body.classList.remove("view-zoom", "view-wide");
    if (view === "zoom") body.classList.add("view-zoom");
    if (view === "wide") body.classList.add("view-wide");
    document.querySelectorAll(".seg button").forEach(function (btn) {
      btn.classList.toggle("active", btn.getAttribute("data-view") === view);
    });
    collapse();
    requestAnimationFrame(nudgeNetworks);
  }

  document.querySelectorAll(".seg button").forEach(function (btn) {
    btn.addEventListener("click", function () { setView(btn.getAttribute("data-view")); });
  });

  tiles.forEach(function (tile) {
    const iframe = tile.querySelector("iframe");
    const html = GRAPH_HTML[tile.getAttribute("data-key")];
    iframe.addEventListener("load", function () {
      if (!html) {
        tile.classList.add("failed");
        tile.querySelector(".loading").textContent = "Graph HTML missing";
        return;
      }
      tile.classList.add("ready");
      setSidebar(iframe, false);
      nudgeOne(iframe);
      setTimeout(function () { nudgeOne(iframe); }, 400);
    });
    if (!html) {
      tile.classList.add("failed");
      tile.querySelector(".loading").textContent = "Graph HTML missing";
      return;
    }
    iframe.srcdoc = html;
    tile.querySelector(".expand").addEventListener("click", function () { expand(tile); });
  });

  document.addEventListener("keydown", function (event) {
    if (event.key === "Escape") {
      collapse();
      requestAnimationFrame(nudgeNetworks);
    }
  });

  window.addEventListener("resize", nudgeNetworks);
})();
</script>
</body>
</html>
"""


def main() -> None:
    raw: dict[str, str] = {}
    for spec in GRAPHS:
        raw[spec["key"]] = (FIGURES / spec["file"]).read_text(encoding="utf-8")

    raw["fig1b"] = recolor_to_match(raw["fig1b"], raw["fig1a"])
    raw["fig2b"] = recolor_to_match(raw["fig2b"], raw["fig2a"])
    raw["fig2a"] = apply_fig2_focus_colors(raw["fig2a"])
    raw["fig2b"] = recolor_to_match(raw["fig2b"], raw["fig2a"])
    raw["fig2b"] = apply_fig2_focus_colors(raw["fig2b"])

    graphs = {}
    for spec in GRAPHS:
        graphs[spec["key"]] = prepare_graph_html(
            raw[spec["key"]],
            hide_hyperedges=spec["fig"] == "2",
        )

    payload = json.dumps(graphs, ensure_ascii=False).replace("<", "\\u003c")
    zoom = "\n".join(tile_markup(s) for s in GRAPHS if s["fig"] == "1")
    wide = "\n".join(tile_markup(s) for s in GRAPHS if s["fig"] == "2")
    html = (
        PAGE.replace("__TILES_ZOOM__", zoom)
        .replace("__TILES_WIDE__", wide)
        .replace("__GRAPH_HTML__", payload)
    )
    out = FIGURES / "compare-graphs.html"
    out.write_text(html, encoding="utf-8")
    print(f"{out}: {out.stat().st_size} bytes")


if __name__ == "__main__":
    main()
