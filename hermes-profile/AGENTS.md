## graphify

This profile **requires** a knowledge graph at `graphify-out/` over `skills/` + `docs/` (god nodes, communities, cross-file relationships).

When the user types `/graphify`, use the bundled **`graphify`** skill before doing anything else. If the user wants to **rebuild incrementally** after the graph exists, use that skill before doing anything else.

**Do not** look for or invent a `scripts/setup-graphify.sh`. Camp Graphify is driven by skill **`graphify`**, which is more flexible than a one-off shell script.

### Where the live graph lives (non-negotiable)

**Always build, update, and query the graph under the installed Hermes profile:**

```text
~/.hermes/profiles/sage/
```

That is where Hermes loads skills/docs for `sage`. Put `graphify-out/` and `.venv-graphify/` **there**.

**Do not** run `/graphify` against the git clone (`…/summer-camp-2026/hermes-profile`). The clone is only for `hermes profile install` / `update` and for instructors packaging `graphify-baseline.tar.gz` into the distribution. A graph under the clone is **not** what the running agent uses.

### Camp rule — discover skills and docs through the graph

This Hermes profile ships a large skill/doc corpus (Sage/Waggle, Hugging Face, NVIDIA Jetson, …). **Do not** mass-read the skills tree to find which skill or reference to use.

Rules:
- For any question about **which skill, which reference, which doc, architecture, or how things connect** in this profile: first run `graphify query "<question>"` when `graphify-out/graph.json` exists under the **installed profile**. Use `graphify path "<A>" "<B>"` for relationships and `graphify explain "<concept>"` for focused concepts.
- **CWD is usually `$HOME` (e.g. `/root`), not the profile.** Always pass `~/.hermes/profiles/sage` (absolute) to `/graphify` — never assume `.` is the profile, and never use the camp repo path for day-to-day Graphify.

### Build / update with `/graphify` + `.venv-graphify` + optional tarball

| Situation | What to use |
|-----------|-------------|
| No `graphify-out/graph.json` yet | Unpack `graphify-baseline.tar.gz` in `~/.hermes/profiles/sage` if present (fast); else `/graphify ~/.hermes/profiles/sage` |
| Graph exists; query / navigate | skill **`graphify`** → `query` / `path` / `explain` (from that profile root) |
| Graph exists; added/changed skills or docs | `/graphify ~/.hermes/profiles/sage --update` |
| Need a **from-scratch** rebuild | `/graphify ~/.hermes/profiles/sage` again (full pipeline; not for incremental adds) |

#### Always use or create `.venv-graphify`

Install Graphify into **`.venv-graphify/`** at the **installed profile root**. Do **not** start with `which graphify` / `uv tool` / system `pip` (hangs or PEP 668). Hermes CWD is often `$HOME`.

```bash
# Installed profile only (not the git clone):
PROFILE="${HERMES_HOME:-$HOME/.hermes}/profiles/sage"
[ -d "$PROFILE/skills/graphify" ] || PROFILE="$HOME/.hermes/profiles/sage"
[ -d "$PROFILE/skills/graphify" ] || { echo "ERROR: installed sage profile not found at $PROFILE"; exit 1; }
cd "$PROFILE"

# Create venv if missing, then install CLI:
if [ ! -x .venv-graphify/bin/python ]; then
  python3 -m venv .venv-graphify
  .venv-graphify/bin/pip install -U pip
  .venv-graphify/bin/pip install -U 'graphifyy[ollama]'
fi
export PATH="$PROFILE/.venv-graphify/bin:$PATH"
GRAPHIFY="$PROFILE/.venv-graphify/bin/graphify"
PYTHON="$PROFILE/.venv-graphify/bin/python"
mkdir -p graphify-out
"$PYTHON" -c "import sys; open('graphify-out/.graphify_python','w',encoding='utf-8').write(sys.executable)"

# Prefer shipped tarball when graph is missing (skips multi-hour extract):
if [ ! -f graphify-out/graph.json ] && [ -f graphify-baseline.tar.gz ]; then
  tar -xzf graphify-baseline.tar.gz
fi

# Required: absolute scan root. Not shippable in the tarball (it would be the
# packager's path); without it `graphify update` scans the CWD — i.e. all of $HOME.
printf '%s\n' "$PROFILE" > graphify-out/.graphify_root
```

Always run `graphify` **from the profile directory**. `graphify update` resolves
`graphify-out/.graphify_root` relative to the CWD, so running it from `$HOME`
misses the marker entirely and falls back to scanning `.`.

Then in Hermes (absolute installed-profile path — CWD is often `$HOME`):

```text
/graphify ~/.hermes/profiles/sage
# after skills/docs change with an existing graph:
/graphify ~/.hermes/profiles/sage --update
```

Use `"$GRAPHIFY" query …` or `"$PYTHON" -c "…"` for skill bash blocks — not system `python3`.

#### Local Ollama notes (Thor)

When the skill / CLI needs a semantic extract against **local Ollama** (cold build without baseline, or doc-heavy `--update`):

1. **`OLLAMA_BASE_URL` must end with `/v1`** (OpenAI-compat). Example: `http://127.0.0.1:11434/v1` — bare `:11434` → HTTP 404 on every chunk.
2. Set **`OLLAMA_MODEL`** to an exact tag from `ollama list` (camp default often `gemma4:31b`).
3. Set **`OLLAMA_API_KEY=ollama`** (any non-empty string; Ollama ignores auth).
4. Prefer **`GRAPHIFY_OLLAMA_KEEP_ALIVE=0`** so extract does not pin VRAM after chunks.
5. Leave **`GRAPHIFY_OLLAMA_NUM_CTX` unset** (auto). Forcing `8192` truncates large markdown chunks (~57k) and hollows the graph. Use `--token-budget 25000` (and `--max-concurrency 1 --api-timeout 1800` if calling `graphify extract` directly).
6. Probe before a long extract: `curl` `/api/tags`, `/v1/models`, and a tiny `/v1/chat/completions` — expect HTTP 200.
7. Full extract over this corpus is **slow** (often 30+ minutes; can be hours). Prefer the baseline tarball; do not block forever in the foreground without telling the user.

Camp procedure detail: `skills/sage-waggle/references/graphify-guide.md`.

### After the graph exists

- Dirty `graphify-out/` files are expected after hooks or incremental updates; dirty graph files are not a reason to skip graphify. Only skip if the task is about stale/incorrect graph output, or the user explicitly says not to use it.
- If `graphify-out/wiki/index.md` exists, use it for broad navigation instead of raw source browsing.
- Read `graphify-out/GRAPH_REPORT.md` only for broad architecture review or when query/path/explain do not surface enough context.
- After modifying profile skill/doc files in this session, run `/graphify ~/.hermes/profiles/sage --update` via **`.venv-graphify`** (not a full rebuild unless starting over).
- Then load the **named** skill (`/skill sage-waggle`, `/skill jetson-llm-serve`, …) and follow it. Graphify finds; the skill teaches procedures.
- Still use Sage MCP for live nodes/data/jobs; Graphify does not replace MCP.
