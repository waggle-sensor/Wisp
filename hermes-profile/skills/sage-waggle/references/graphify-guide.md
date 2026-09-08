# Graphify — required skills/docs discovery for this profile

[Graphify](https://github.com/Graphify-Labs/graphify) is **required** on this Hermes profile. The profile ships ~250 skills and ~1.8K markdown files; the agent must discover the right skill/ref via the knowledge graph, not by grepping the tree.

There is **no** camp setup shell script. Use the bundled skill **`graphify`**.

**Live graph location:** always `~/.hermes/profiles/sage/` (the installed Hermes profile). That is where Hermes loads skills for `sage`. **Do not** build or update day-to-day graphs under the git clone (`…/summer-camp-2026/hermes-profile`) — the clone is only for install/`hermes profile update` and for instructors shipping `graphify-baseline.tar.gz`.

| | |
|--|--|
| **Upstream** | <https://github.com/Graphify-Labs/graphify> |
| **Bundled skill** | `skills/graphify/` — `/graphify ~/.hermes/profiles/sage` |
| **Always-on rules** | profile `AGENTS.md` |
| **Camp baseline** | `graphify-baseline.tar.gz` (optional fast init for `graphify-out/`) |
| **Corpus** | `skills/` + `docs/` (see `.graphifyignore`) |
| **PyPI** | `graphifyy` (CLI: `graphify`) |
| **Venv (required)** | **`.venv-graphify/`** under `~/.hermes/profiles/sage` — create if missing |

## Agent protocol (non-negotiable)

1. If `~/.hermes/profiles/sage/graphify-out/graph.json` exists → skill **`graphify`**: `query` / `path` / `explain` **before** mass-reading skills.
2. **Always use or create `.venv-graphify`** under the installed profile. Do **not** start with `which graphify` / `uv tool` / system `pip`.
3. If the graph is **missing** → unpack `graphify-baseline.tar.gz` in `~/.hermes/profiles/sage` if present, else **`/graphify ~/.hermes/profiles/sage`** (full build; can be slow on Ollama).
4. If the graph exists and files were **added or changed** → **`/graphify ~/.hermes/profiles/sage --update`**. Do **not** full-rebuild for incremental adds.
5. Load the **specific** skill the graph points to (`sage-waggle`, `jetson-llm-serve`, `hf-cli`, …).
6. Use Sage / HF MCP for live data; Graphify indexes **this profile’s** skills and docs only.

## Install + build (every Thor / every profile install)

After `hermes profile install ./hermes-profile --name sage --alias`:

**Hermes CWD is usually `$HOME`.** Always pass **`~/.hermes/profiles/sage`** (absolute) to `/graphify` — not the camp repo path.

### 1. Create (or reuse) the Graphify venv on the installed profile

```bash
cd ~/.hermes/profiles/sage

if [ ! -x .venv-graphify/bin/python ]; then
  python3 -m venv .venv-graphify
  .venv-graphify/bin/pip install -U pip
  .venv-graphify/bin/pip install -U 'graphifyy[ollama]'
fi
export PATH="$PWD/.venv-graphify/bin:$PATH"
```

### 2. Prefer the tarball; otherwise `/graphify`

```bash
# Fast path — unpack shipped baseline when present:
if [ ! -f graphify-out/graph.json ] && [ -f graphify-baseline.tar.gz ]; then
  tar -xzf graphify-baseline.tar.gz
fi
# Required: absolute scan root (the tarball ships without one — see below).
printf '%s\n' "$HOME/.hermes/profiles/sage" > graphify-out/.graphify_root
test -f graphify-out/graph.json && echo "graph ok"
```

If there is still no `graph.json`, in a Hermes session:

```text
/graphify ~/.hermes/profiles/sage
```

**Expect:** Full semantic extract over ~1.8K files is slow and shares VRAM with Ollama chat. Prefer the baseline tarball.

### Updating an existing graph

```text
/graphify ~/.hermes/profiles/sage --update
```

Or from the installed profile with the venv CLI:

```bash
cd ~/.hermes/profiles/sage
export PATH="$PWD/.venv-graphify/bin:$PATH"
.venv-graphify/bin/graphify update .
```

**Always `cd` to the profile first** — that `cd` is load-bearing, not tidiness.
`graphify update` looks for `graphify-out/.graphify_root` relative to the
**current directory**, so from `$HOME` it finds nothing, falls back to scanning
`.`, and walks your whole home tree (measured on a Thor node: 8,746 files, plus
a stray `~/graphify-out`). With the marker in place and the CWD at the profile
it scans the right ~244 files.

The shipped tarball deliberately contains no `.graphify_root`: graphify reads it
with `Path(text)` and does no shell expansion, so a literal `$HOME/...` becomes
a bogus path and a real absolute path would be the packager's machine. Write it
yourself after unpacking (step 2 above).

## Local Ollama — what we learned to make extract work

These matter when building/updating **without** (or beyond) the baseline tarball on Thor + Ollama:

| Rule | Why |
|------|-----|
| `OLLAMA_BASE_URL=http://127.0.0.1:11434/v1` | Must end with `/v1`. Bare `:11434` → `404 page not found` on every semantic chunk |
| `OLLAMA_MODEL=<exact ollama list tag>` | e.g. `gemma4:31b` — wrong tag also looks like 404 |
| `OLLAMA_API_KEY=ollama` | Any non-empty string; Ollama ignores auth but the OpenAI client sends a Bearer |
| `GRAPHIFY_OLLAMA_KEEP_ALIVE=0` | Avoid pinning the model in VRAM between chunks / after extract |
| Leave `GRAPHIFY_OLLAMA_NUM_CTX` **unset** | Auto-size from chunk. Forcing `8192` truncates ~57k markdown chunks → hollow graph |
| `--token-budget 25000` | Camp-sized chunks; pair with low VRAM only if you also lower `NUM_CTX` |
| `--max-concurrency 1 --api-timeout 1800` | Thor-friendly when calling `graphify extract` directly |
| Probe before long runs | `/api/tags`, `/v1/models`, tiny `/v1/chat/completions` must return HTTP 200 |

Manual extract (only if you need the CLI outside Hermes):

```bash
cd ~/.hermes/profiles/sage
source .venv-graphify/bin/activate

export OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
export OLLAMA_MODEL=gemma4:31b          # exact tag from `ollama list`
export OLLAMA_API_KEY=ollama
export GRAPHIFY_OLLAMA_KEEP_ALIVE=0
# Leave GRAPHIFY_OLLAMA_NUM_CTX unset

graphify extract . --backend ollama --token-budget 25000 --max-concurrency 1 --api-timeout 1800
```

### Probe Ollama OpenAI-compat

```bash
export OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
export OLLAMA_API_KEY=ollama
export OLLAMA_MODEL=gemma4:31b

curl -s "$OLLAMA_BASE_URL/models" -H "Authorization: Bearer $OLLAMA_API_KEY" | head
curl -s -o /tmp/out.json -w "%{http_code}\n" -X POST "$OLLAMA_BASE_URL/chat/completions" \
  -H "Authorization: Bearer $OLLAMA_API_KEY" -H "Content-Type: application/json" \
  -d "{\"model\":\"$OLLAMA_MODEL\",\"messages\":[{\"role\":\"user\",\"content\":\"ping\"}],\"max_tokens\":8}"
cat /tmp/out.json
```

Expect HTTP **200**. Native `/api/tags` being healthy does **not** prove `/v1/...` works.

### `externally-managed-environment` (PEP 668)

Do **not** `pip install` into system Python. Create `.venv-graphify` and install `graphifyy` there.

## Query examples

```bash
source .venv-graphify/bin/activate
graphify query "pluginctl sideload ECR acpi" --graph graphify-out/graph.json
graphify path "sage-waggle" "jetson-llm-serve" --graph graphify-out/graph.json
graphify explain "pywaggle upload_file" --graph graphify-out/graph.json
```

## Security

Do not put secrets into `skills/` / `docs/` before extracting. Profile `.env` stays user-owned and outside the graph corpus.
