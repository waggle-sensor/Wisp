# Hermes Agent Setup Guide

Run **Hermes Agent on your Thor** — your laptop is only an SSH client. Hermes handles files, terminal, and tools on the Thor; inference runs on the same machine via **Ollama** (Part 1) or over HTTPS to **NVIDIA Build** (Part 2) or **NRP Managed LLMs** (Part 2B).

Every participant has their **own Linux account** on the Thor. Hermes installs into your home directory (`~/.hermes/`) — agents are isolated by default. To share config or set up on a new machine, use a **profile distribution** ([Part 3](#part-3-transferring-the-brain)).

| Guide | Best for |
| ----- | -------- |
| [Part 1 — Thor + Ollama](#part-1-thor--ollama) | Local GPU inference via Ollama on your assigned Thor |
| [Part 2 — NVIDIA Hosted APIs](#part-2-nvidia-hosted-apis) | Cloud inference via NVIDIA Build (no Ollama needed) |
| [Part 2B — NRP Managed LLMs](#part-2b-nrp-managed-llms) | Cloud inference via NRP Nautilus (`minimax-m2` default) |
| [Part 3 — Transferring the brain](#part-3-transferring-the-brain) | Share agent config or move to a new machine via profile distribution |
| [Inference options compared](#inference-options-compared) | Local Thor vs NVIDIA vs NRP vs paid APIs — which model to use |
| [Switching between approaches](#switching-between-approaches) | Swap providers without reinstalling |
| [Hermes web dashboard](#hermes-web-dashboard) | Browser UI on your laptop via SSH tunnel + `hermes dashboard` |
| [Token economy](#token-economy) | Manage context, cost, and fair use across providers |
| [Updating the knowledge graph](#updating-the-knowledge-graph) | Refresh Graphify after skills/docs change (`/graphify … --update`) |

**Docs:** [Hermes Documentation](https://hermes-agent.nousresearch.com/docs/) · [Profile Distributions](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions)

---

# Part 1: Thor + Ollama

Hermes and Ollama both run on the Thor. Your laptop connects via SSH and attaches to a tmux session.

## At a glance

```
  Laptop (SSH)                    Thor GPU
┌──────────────────┐              ┌──────────────────────────┐
│  Terminal only   │   SSH        │  Hermes Agent            │
│  tmux attach     │─────────────►│  Ollama (localhost:11434)│
│                  │              │  Files, terminal, tools  │
└──────────────────┘              └──────────────────────────┘
```

**Flow:** SSH to Thor → Install Hermes CLI → Install Sage profile → Verify Ollama → Run in tmux

---

## Prerequisites

- [ ] **Your personal Linux account** on the assigned Thor blade (provided by camp organizers)
- [ ] SSH access: `ssh your-linux-user@thor-host` (use the username you were assigned)
- [ ] Ollama installed and running on the Thor (shared system service — ask an instructor if it's not running)
- [ ] At least one model pulled on the Thor (e.g. `gemma4:31b`)
- [ ] Laptop with a terminal/SSH client only — nothing is installed locally

### Before camp — Thor fleet prep (organizers, optional)

Camp works without these — the profile defaults to `terminal.backend: local` and students can run [Step 4B](#step-4b--cap-ollama-context-recommended) themselves. Optional fleet actions:

| Action | Why |
| --- | --- |
| Pre-create `gemma4-64k` on each Thor (`ollama create` from Modelfile) | Students skip Step 4B |
| `apt install catatonit` on Thors | Enables Hermes Docker sandbox if desired later |
| Pre-pull `docker.io/nikolaik/python-nodejs:python3.11-nodejs20` | Podman short-name fix for Docker backend |

---

## Your account, your agent

You SSH in as **your own Linux user** (e.g. `ssh jsmith@thor-host`), not a shared account. Hermes installs entirely under your home directory — no root or sudo needed.

| Shared on Thor | Private to your Linux account |
| --- | --- |
| Ollama + GPU inference | `~/.hermes/` (agent brain) |
| System packages (tmux, etc.) | tmux sessions (Linux isolates per user) |
| Thor hostname / SSH access | API keys in `~/.hermes/.env` |

- `~/.hermes/` — config, memories, skills, sessions
- `~/.local/bin/hermes` — CLI binary
- Other participants on the same Thor have their own `~/.hermes/` — you cannot see or overwrite each other's agents
- **Ollama is shared** (system-level); each user's Hermes connects to the same `localhost:11434`

---

## Step 1 — SSH into your Thor

```bash
ssh your-linux-user@thor-host
```

Replace `your-linux-user` with the Linux username you were assigned and `thor-host` with your blade hostname.

---

## Step 2 — Install Hermes CLI

Install the Hermes CLI into your home directory. Choose **Blank Slate** so the camp profile (Step 3A) provides the configuration.

```bash
curl -fsSL https://hermes-agent.nousresearch.com/install.sh | bash
```

| Choice | Select |
| ------ | ------ |
| Setup mode | **3. Blank Slate** — skip the wizard; profile install handles config |
| provider | **34. Leave unchanged** |
| Terminal backend | **Keep current (local)** |
| Your minimal agent is ready. What next? | **Start with everything disabled — finish now (most minimal)** |

Reload your shell and verify:

```bash
source ~/.bashrc   # or ~/.zshrc
hermes --version
```

---

## Step 3A — Install Sage profile (recommended)

> **Recommended.** Use this path unless profile install fails or you need a fully custom configuration.

The camp maintains a Hermes **profile distribution** in this repo at [`hermes-profile/`](hermes-profile/). It ships pre-configured SOUL, model settings, tools, and skills. See the [Profile Distributions guide](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions) for details.

**What the distribution ships vs. what stays private:**

| Shipped (distribution-owned) | Never shipped (user-owned) |
| --- | --- |
| SOUL.md, AGENTS.md, config.yaml, skills/, docs/, scripts/, mcp.json | `memories/`, `sessions/`, `auth.json`, `.env` |
| Updated via `hermes profile update` | Preserved across updates — your brain stays isolated |

> see [agent-knowledge-graph](hermes-profile/agent-knowledge-graph.html) for a visual representation of the agent's baseline knowledge. As your agent learns, the live graph updates under **`~/.hermes/profiles/sage/graphify-out/`** (e.g. `graph.html`) — not under the camp git clone.

### Install from local clone (recommended)

`hermes profile install github.com/org/repo` clones the **repo root** as the distribution — it does not support subpaths. Since the profile lives inside this monorepo, clone first:

```bash
git clone https://github.com/waggle-sensor/summer-camp-2026.git
#git checkout <branch> #if desired
cd summer-camp-2026
hermes profile install ./hermes-profile --name sage --alias
```

### What happens on install

1. Copies distribution files into `~/.hermes/profiles/sage/`
2. Shows manifest preview (name, version, required env vars)
3. Marks each `env_requires` key as `✓ set` or `needs setting`
4. Prompts for confirmation (pass `-y` to skip)
5. Writes `.env.EXAMPLE` — you copy to `.env`
6. With `--alias`, creates a `sage` wrapper command at `~/.local/bin/sage`

`~/.local/bin` is **not** on `PATH` on every host — notably for `root` on the
Thor/Debian node images, whose minimal `/root/.profile` omits the usual
`~/.local/bin` block. If `sage` is "command not found" right after install, the
wrapper exists and the directory is simply unreachable:

```bash
ls -l ~/.local/bin/sage                      # wrapper is there
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.bashrc && . ~/.bashrc
```

`hermes -p sage` works regardless — the wrapper is only a shorthand for it.

### Post-install

```bash
hermes profile use sage
cp ~/.hermes/profiles/sage/.env.EXAMPLE ~/.hermes/profiles/sage/.env
# Edit .env if needed — add API keys for Part 2; leave blank for Thor+Ollama
hermes profile info sage
hermes doctor

hermes setup tools #(optional) if you want to configure more tools
```

Launch with `hermes`.

> **Note:** Graphify will automatically be used by the agent. see [graphify-guide.md](hermes-profile/skills/sage-waggle/references/graphify-guide.md) or [graphify skills](hermes-profile/skills/graphify/SKILL.md) for more details.

### Pull camp config updates

```bash
hermes profile update sage --force-config
```

Replaces distribution-owned files (SOUL, skills, cron, mcp.json). **Preserves** your `config.yaml` tweaks and all user data (memories, sessions, `.env`). Pass `--force-config` only to reset config to the distribution default.

> **Security:** SOUL.md and skills are active on first chat. Cron jobs from the distribution are **not** auto-scheduled — run `hermes -p sage cron list` and enable explicitly.

---

## Step 3B — Manual setup (backup)

<details>
<summary><strong>Backup — manual interactive setup</strong> (use only if profile install fails or you need custom config)</summary>

Run the full installer wizard instead of the camp profile:

```bash
hermes setup
```

Work through the installer in this order. Values marked *example* depend on your Thor model.

### Setup mode

| Choice | Select |
| ------ | ------ |
| Setup mode | **2. Full setup** — configure providers and tools yourself |

### Model provider

| Field | Value |
| ----- | ----- |
| Provider | **Custom / OpenAI-compatible** (`custom` direct API) |
| API base URL | `http://127.0.0.1:11434/v1` |
| API key | Leave blank |
| Compatibility mode | **1. Auto-detect** |

> **Why `127.0.0.1`?** Hermes and Ollama run on the same Thor — no SSH tunnel needed.

### Model settings (*example*)

| Field | Example value | Notes |
| ----- | ------------- | ----- |
| Model name | `gemma4:31b` | Must match a model on the Thor |
| Context length | `256000` | Match your model's limit |
| Display name | `sage-thor-H020-gemma4-31b` | Any label that helps you identify this endpoint |

### Terminal & platforms

| Prompt | Select |
| ------ | ------ |
| Terminal backend | **Keep current (local)** — tools run on the Thor filesystem |
| Platforms (Mattermost, Slack, etc.) | Skip — press **Enter** |

### CLI tools

Enable these tools (toggle with **Space**, confirm with **Enter**):

| Enabled | Tool |
| ------- | ---- |
| ✓ | Web Search & Scraping |
| ✓ | Browser Automation |
| ✓ | Terminal & Processes |
| ✓ | File Operations |
| ✓ | Code Execution |
| ✓ | Vision / Image Analysis |
| ✓ | Text-to-Speech |
| ✓ | Skills |
| ✓ | Task Planning |
| ✓ | Memory |
| ✓ | Session Search |
| ✓ | Clarifying Questions |
| ✓ | Task Delegation |
| ✓ | Cron Jobs |
| ✓ | Computer Use |

Leave video generation, image generation, and integrations you don't need unchecked.

### Provider choices

| Category | Select |
| -------- | ------ |
| Browser | **Local Browser** (recommended, free) |
| Text-to-Speech | **Microsoft Edge TTS** (free) |
| Web Search | **DuckDuckGo (ddgs)** (free, no API key) |

### Finish install

Reload your shell and verify:

```bash
source ~/.bashrc
hermes --version
```

**Full installer prompts (reference):**

```
(○) 1. Quick Setup (Nous Portal)
(●) 2. Full setup
(○) 3. Blank Slate

API base URL: http://127.0.0.1:11434/v1
API key: <leave blank>
Choice [1-4]: 1   # Auto-detect

Model name: gemma4:31b
Context length: 256000
Display name: sage-thor-H020-gemma4-31b
```

> **Note:** Browser automation on a headless Thor may need extra setup (local browser vs. MCP). This is optional — not required for core agent use.

</details>

---

## Step 4 — Verify Ollama on the Thor

Run these on the Thor (in your SSH session):

**List models:**

```bash
curl http://127.0.0.1:11434/api/tags
```

**Verify the OpenAI-compatible endpoint:**

```bash
curl http://127.0.0.1:11434/v1/models
```

If both return model data, Hermes can connect.

---

## Step 4B — Cap Ollama context (recommended)

On Thor blades, the camp profile defaults to **`gemma4:31b`**. With Ollama's full auto-detected context (~262K tokens), the **first response can take 3–4+ minutes** and Hermes may look frozen. This is a known Thor issue — not a broken install.

**Diagnose:**

```bash
ollama ps    # CONTEXT column may show 262144
```

> **Important:** Hermes `context_length` in `config.yaml` only changes the **displayed** limit. It does **not** forward `num_ctx` to Ollama. The Modelfile (below) is what actually caps KV-cache allocation. Verify with `ollama ps`, not the Hermes status bar alone.

**Fix (no sudo)** — create a derived model with a smaller context window:

```bash
cat > /tmp/gemma-64k.modelfile << 'EOF'
FROM gemma4:31b
PARAMETER num_ctx 65536
EOF

ollama create gemma4-64k -f /tmp/gemma-64k.modelfile
ollama run gemma4-64k "hi"    # warm load once
ollama ps                      # expect CONTEXT 65536
hermes model                   # switch to gemma4-64k
```

The first response after the model has been idle still pays a ~25–30s model-load cost — that's normal.

**Extended reference:** [Setting Up Hermes on a Sage Thor Node](https://github.com/Miguel-Hernandez1/project-sage-notes/blob/main/docs/03-hermes-on-thor.md) (H00F-tested). See also [Token economy](#token-economy) for shared GPU etiquette.

---

## Step 5 — Run Hermes in tmux

tmux keeps Hermes running after you close your laptop or drop SSH.

**Check tmux is available** (should be pre-installed):

```bash
tmux -V
```

> If tmux is missing, ask an instructor. Participants typically have no sudo. Each user's tmux sessions are isolated by Linux — you don't need a unique session name to avoid collisions with other participants.

**Start and detach:**

```bash
tmux new -s hermes
# Inside the session:
hermes

# Detach: Ctrl-b then d
# Reattach from any SSH session:
tmux attach -t hermes

# List sessions:
tmux ls
```

**Optional detached start:**

```bash
tmux new -s hermes -d 'hermes'
tmux attach -t hermes
```

### Tmux scrollback (save session transcripts)

Long Hermes sessions can scroll past the default buffer. Increase scrollback once on the Thor:

```bash
echo 'set-option -g history-limit 50000' >> ~/.tmux.conf
# Restart tmux server or start a new session for the setting to take effect
```

**Save a full session transcript** — from **inside** the `hermes` tmux session (after `tmux attach -t hermes`):

```bash
chmod +x ~/summer-camp-2026/scripts/write-tmux.sh   # once
~/summer-camp-2026/scripts/write-tmux.sh
```

The script captures the full scrollback (with ANSI colors) to `~/AI-projects/tmux-logs/transcript_<timestamp>.ansi`. View with:

```bash
less -R ~/AI-projects/tmux-logs/transcript_*.ansi
```

**Hermes keeps its own history in SQLite, not in files.** The profile's
`sessions/` directory stays empty; conversations live in
`~/.hermes/profiles/sage/state.db` (tables `sessions` and `messages`). Don't
conclude a run was lost because `sessions/` is empty. To read one back:

```bash
hermes chat -p sage -r <session_id>          # session_id is printed on exit
cd ~/.hermes/profiles/sage && python3 -c "
import sqlite3
c = sqlite3.connect('file:state.db?mode=ro', uri=True)
for sid, n in c.execute('select session_id, count(*) from messages group by session_id'):
    print(sid, n)"
```

Scripted use: `hermes chat -p sage -Q -q '<question>'` prints only the answer on
stdout and `session_id: <id>` on stderr. Local Ollama on a Thor takes minutes
per answer with nothing on stdout until it finishes — a quiet run is normal, so
give it a generous timeout rather than assuming it failed.

---

## Step 6 — Reconfigure later (optional)

```bash
hermes model              # add or change model providers
hermes setup              # re-run setup wizard
hermes profile update sage --force-config   # pull camp profile updates
```

---

## Troubleshooting (Thor)

| Check | Command |
| ----- | ------- |
| Ollama running? | `curl http://127.0.0.1:11434/api/tags` |
| OpenAI endpoint? | `curl http://127.0.0.1:11434/v1/models` |
| Ollama context size? | `ollama ps` |
| Hermes health | `hermes doctor` |
| Reattach agent | `tmux attach -t hermes` |

**If Hermes can't connect:**

1. Confirm Ollama is running on the Thor (ask an instructor).
2. Confirm the model name in Hermes matches a model from `/v1/models`.
3. Run `hermes doctor` and check your profile config.

**First response very slow (3+ minutes)?**

See [Step 4B](#step-4b--cap-ollama-context-recommended) — cap context with a `gemma4-64k` Modelfile.

### Hermes Docker sandbox (exit 125) — why camp uses `local` backend

**Symptom:** tool calls fail instantly with `Docker exit status 125`.

**Cause:** on Thors, `docker` is actually **Podman**. Hermes launches its sandbox with Podman's `--init` flag, which requires the **`catatonit`** binary — not installed on current Thors.

**Camp default:** the profile ships `terminal.backend: local` — commands run directly in your Linux account without a container sandbox. This is intentional for camp.

**If you switched to Docker and hit exit 125:**

1. Switch back: `hermes config set terminal.backend local`
2. Optional fleet fix (ask help desk): `sudo apt install catatonit` and pre-pull `docker.io/nikolaik/python-nodejs:python3.11-nodejs20`

> This is Hermes's **tool sandbox** for shell/file commands — separate from **plugin** container builds via `pluginctl`.

### First plugin build on Thor — use `pluginctl`

For Sage plugin development on a Thor node, use **`pluginctl`** (not raw `podman build` for your first test):

```bash
git clone <your-plugin-repo>
cd <plugin-dir>
sudo pluginctl build .                         # builds + tags to node-local registry
sudo pluginctl run --name test <image-ref>     # image ref printed by build
sudo pluginctl logs test
sudo pluginctl rm test
```

**Notes:**

- `pluginctl` uses kubeconfig `/etc/rancher/k3s/k3s.yaml` — **`sudo` is required** on Thor for build, run, logs, and rm
- Use **fully-qualified** base images in Dockerfiles: `FROM docker.io/waggle/plugin-base:1.1.1-base` (Podman on Thor has no short-name registry default)
- ECR portal builds may still fail (runc bug) — `podman` + `k3s ctr images import` remains the side-load workaround; see the `sage-waggle` skill. **`pluginctl build` is the normal on-node development path.**

**References:**
- **pluginctl:** [Sage reference](https://sagecontinuum.org/docs/reference-guides/pluginctl) · [edge-scheduler tutorials](https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/pluginctl) · [build tutorial](https://github.com/waggle-sensor/edge-scheduler/blob/main/docs/pluginctl/tutorial_build.md)
- **Edge apps:** [tutorial series](https://sagecontinuum.org/docs/category/edge-apps)
- **sesctl** (fleet scheduling after ECR): [Sage reference](https://sagecontinuum.org/docs/reference-guides/sesctl) · [edge-scheduler tutorials](https://github.com/waggle-sensor/edge-scheduler/tree/main/docs/sesctl)

**tmux issues:**

- Thor rebooted → SSH back in and `tmux new -s hermes`
- Closed laptop → `tmux attach -t hermes` (agent keeps running on Thor)
- Can't see another user's session → expected; tmux sessions are per Linux account

To enable more tools later: `hermes setup tools` or edit `~/.hermes/.env`.

---

# Part 2: NVIDIA Hosted APIs

Hermes runs on the Thor and talks to **NVIDIA Build** over HTTPS. No Ollama required.

## At a glance

```
  Laptop (SSH)              Thor                    NVIDIA Build
┌──────────────┐     ┌──────────────────┐        ┌──────────────────────────┐
│  tmux attach │ SSH │  Hermes Agent    │  HTTPS │  integrate.api.nvidia    │
│              │────►│  (your account)  │───────►│  Managed GPU inference   │
└──────────────┘     └──────────────────┘  TLS   └──────────────────────────┘
```

No SSH tunnel. No Ollama. No local GPU to manage.

---

## Prerequisites

- [ ] SSH access to your Thor with Hermes installed ([Part 1](#part-1-thor--ollama))
- [ ] NVIDIA Developer account
- [ ] API key from [NVIDIA Build](https://build.nvidia.com/settings/api-keys)

If you used the camp profile (Step 3A), it may already define the NVIDIA provider — you only need to add your API key to `.env`.

---

## Step 1 — Create an account

Sign in or register at **[NVIDIA Build](https://build.nvidia.com/)**.

---

## Step 2 — Generate an API key

1. Go to **[API Keys](https://build.nvidia.com/settings/api-keys)**
2. Click **Get API Key**
3. Save the key — it looks like:

```text
nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Store it in **your** `~/.hermes/profiles/sage/.env` (or `~/.hermes/.env` for manual setup). API keys are never shared across Linux accounts.

---

## Step 3 — Choose a model

Browse the **[NVIDIA Model Catalog](https://build.nvidia.com/explore/discover)** and copy the exact model ID.

Popular options:

| Model ID |
| -------- |
| `z-ai/glm-5.2` |
| `meta/llama-3.3-70b-instruct` |
| `qwen/qwen3-235b-a22b` |
| `deepseek-ai/deepseek-r1` |
| `mistralai/mistral-large` |
| `nvidia/nemotron-3-ultra-550b-a55b` |

> Catalog IDs change over time — always copy from the catalog page.

---

## Step 4 — Configure Hermes

```bash
hermes model
```

| Setting | Value |
| ------- | ----- |
| Provider | **NVIDIA NIM** (build.nvidia.com or local NIM) |
| API Key | `nvapi-...` |
| Base URL | `https://integrate.api.nvidia.com/v1` |
| Model | Your catalog model ID |

Or add the key directly to `.env`:

```bash
# ~/.hermes/profiles/sage/.env
NVIDIA_API_KEY=nvapi-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

---

## Step 5 — Launch Hermes

```bash
tmux attach -t hermes    # if already running
# or start fresh:
tmux new -s hermes
hermes
```

All inference requests go to NVIDIA's hosted infrastructure from the Thor.

---

## Troubleshooting (NVIDIA)

1. API key must start with `nvapi-`.
2. Base URL must be exactly `https://integrate.api.nvidia.com/v1`.
3. Model ID must match the catalog exactly.
4. On the free tier, high demand can cause occasional delays.
5. Confirm the key is in **your** `.env`, not another user's.

**References:** [NVIDIA NIM API](https://build.nvidia.com/) · [API Reference](https://docs.nvidia.com/nim/large-language-models/latest/api-reference.html) · [Forum — connection issues](https://forums.developer.nvidia.com/t/not-connect-to-endpoint-https-integrate-api-nvidia-com-v1/324036)

---

# Part 2B: NRP Managed LLMs

Hermes runs on the Thor and talks to **[NRP Managed LLMs](https://nrp.ai/documentation/userdocs/ai/llm-managed/)** over HTTPS via the Envoy AI Gateway. No Ollama required. The camp profile ships **`minimax-m2`** ([NRP model card](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/#minimax-m2)) as the default NRP model — strong agentic tool calling and ~200K context.

## At a glance

```
  Laptop (SSH)              Thor                    NRP Nautilus
┌──────────────┐     ┌──────────────────┐        ┌──────────────────────────┐
│  tmux attach │ SSH │  Hermes Agent    │  HTTPS │  ellm.nrp-nautilus.io    │
│              │────►│  (your account)  │───────►│  Managed open-weights    │
└──────────────┘     └──────────────────┘  TLS   └──────────────────────────┘
```

---

## Prerequisites

- [ ] SSH access to your Thor with Hermes installed ([Part 1](#part-1-thor--ollama))
- [ ] NRP group membership with the **LLM flag** enabled (check the [namespaces page](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/))
- [ ] NRP LLM token from the [LLM token page](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/)

If you used the camp profile (Step 3A), the `nrp` custom provider is already in `config.yaml` — you only need to add your token to `.env`.

---

## Step 1 — Get an NRP LLM token

1. Confirm your NRP group has the LLM flag (see [API Access](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/)).
2. Create a token on the NRP LLM token page.
3. Store it in **your** `~/.hermes/profiles/sage/.env`:

```bash
# ~/.hermes/profiles/sage/.env
NRP_LLM_API_KEY=<your-token>
```

---

## Step 2 — Verify access

```bash
curl -H "Authorization: Bearer $NRP_LLM_API_KEY" https://ellm.nrp-nautilus.io/v1/models
```

You should see `minimax-m2` and other active models in the response.

---

## Step 3 — Switch to NRP in Hermes

```bash
hermes model
```

| Setting | Value |
| ------- | ----- |
| Provider | **`nrp`** (custom provider) |
| API Key env | `NRP_LLM_API_KEY` (from `.env`) |
| Base URL | `https://ellm.nrp-nautilus.io/v1` (pre-configured) |
| Model | **`minimax-m2`** |

Or edit `~/.hermes/profiles/sage/config.yaml` directly — the `nrp` provider and `minimax-m2` model are already defined under `custom_providers`.

> **Why minimax-m2?** Strong agentic coding / tool use and ~200K context on NRP. Browse the [model matrix](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/) to pick others (`gpt-oss`, `qwen3`, `gemma`, `kimi`, etc.) via `hermes model`. Note: NRP currently lists `minimax-m2` as **evaluating** — availability may change.

---

## Step 4 — Launch Hermes

```bash
tmux attach -t hermes    # if already running
# or start fresh:
tmux new -s hermes
sage                # or: hermes -p sage
```

All inference requests go to NRP's managed infrastructure from the Thor.

---

## Troubleshooting (NRP)

1. Confirm your group has the LLM flag — without it, the endpoint returns auth errors.
2. Token must be passed as `Authorization: Bearer <token>`.
3. Model ID is **`minimax-m2`** — use the short API alias from `/v1/models` (not a HuggingFace path).
4. Review the [Fair Use Policy](https://nrp.ai/documentation/userdocs/ai/llm-managed/fair-use-policy/) — per-model concurrency limits apply.
5. Confirm the token is in **your** `.env`, not another user's.

**References:** [NRP Managed LLMs](https://nrp.ai/documentation/userdocs/ai/llm-managed/) · [Available Models](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/) · [API Access](https://nrp.ai/documentation/userdocs/ai/llm-managed/api-access/) · [Client Configurations](https://nrp.ai/documentation/userdocs/ai/llm-managed/client-configs/)

---

# Part 3: Transferring the brain

Move agent configuration between machines or share it with your team via **profile distributions**. Use `export`/`import` only for local backup on the same machine.

## Mechanisms

| Mechanism | Purpose | Memories/sessions? | Credentials? |
| --- | --- | --- | --- |
| **`hermes profile install` / `update`** (distribution) | Team sharing, new Thor, or new machine — install config from git | No | No — each user fills `.env` |
| **`hermes profile export` / `import`** | Back up or restore a profile **on the same machine** | Yes | No (stripped) |

> **Team sharing and new machines:** Use a profile distribution — push config to git, then run `hermes profile install` or `hermes profile update` on each machine. Do **not** use `export`/`import` for handoffs between people or machines.
>
> **Personal memories and sessions are never shared** via distributions. Each Linux account keeps its own brain even when everyone installs the same profile.

**References:** [Hermes Memory](https://hermes-agent.nousresearch.com/docs/user-guide/features/memory) · [Profile Commands](https://hermes-agent.nousresearch.com/docs/reference/profile-commands) · [Profile Distributions](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions)

## What makes up the brain

| Component | Location | What it carries |
| --- | --- | --- |
| Personality | `SOUL.md` | Agent instructions and tone |
| Memories | `memories/MEMORY.md`, `USER.md` | Facts and user preferences |
| Skills | `skills/` | Reusable procedures |
| Sessions | `state.db` | Conversation history (searchable) |
| Config | `config.yaml` | Model, tools, settings |

## Profile distribution (team sharing and new machines)

Use this when you want the **same agent configuration** — SOUL, skills, model settings, tools — on multiple machines or Thor blades. Works for teammates, moving to a new Thor, or syncing your agent across machines you own.

### Install on a new machine

SSH into the new Thor as your Linux user, install the Hermes CLI ([Part 1, Step 2](#step-2--install-hermes-cli)), then install the profile:

```bash
# From the camp repo
git clone https://github.com/waggle-sensor/summer-camp-2026.git
cd summer-camp-2026
hermes profile install ./hermes-profile --name sage --alias
```

Fill in your credentials and verify:

```bash
hermes profile use sage
cp ~/.hermes/profiles/sage/.env.EXAMPLE ~/.hermes/profiles/sage/.env
# Edit .env — add your API keys
hermes profile info sage
hermes doctor
```

Memories and sessions from your old machine **do not transfer** — each machine builds its own. Your agent config (SOUL, skills, tools) is what syncs via git.

### Pull updates (teammates or additional machines)

```bash
hermes profile update sage --force-config
```

Updates replace distribution-owned files (SOUL, skills, cron) but **never** touch `memories/`, `sessions/`, or `.env`.

### Publish changes (authors)

Camp organizers and team leads publish via git — see [Profile Distributions: For authors](https://hermes-agent.nousresearch.com/docs/user-guide/profile-distributions#for-authors-publishing-a-distribution) and the checklist in [`hermes-profile/README.md`](hermes-profile/README.md).

```bash
# After editing SOUL.md, skills/, config.yaml, etc. in the profile repo:
git add distribution.yaml SOUL.md skills/ config.yaml
git commit -m "v1.1.0: updated camp SOUL and skills"
git tag v1.1.0
git push --tags
```

Anyone with the profile installed runs `hermes profile update sage` to pick up the changes.

## End of camp — contribute your brain (required)

> **Don't forget:** Before you leave camp, contribute what you learned back to the shared Sage agent.

All week you build a personal **brain** under `~/.hermes/profiles/sage/` — memories, skill tweaks, reference notes, debugging recipes. That knowledge stays on your Thor unless you contribute it. Camp organizers merge student contributions into [`hermes-profile/`](hermes-profile/) so everyone can run `hermes profile update sage` and inherit the improvements.

### How to contribute

1. **Review your brain** on the Thor:

```bash
ls ~/.hermes/profiles/sage/memories/
ls ~/.hermes/profiles/sage/skills/
cat ~/.hermes/profiles/sage/memories/MEMORY.md   # if you wrote memories
```

2. **Refresh the Graphify graph**. In a Hermes session:

```text
/graphify ~/.hermes/profiles/sage --update
```

(Use your real installed profile path if it differs — Hermes CWD is often `$HOME`, so pass an absolute path. Do **not** point this at the `summer-camp-2026` git clone.)

3. **Export your brain** to a tarball:

```bash
hermes profile export sage -o ~/sage-brain-export.tar.gz
```

4. **Upload the tarball** to your personal `sage-summer-camp-2026` repo (not the shared camp repo):

```bash
cd ~/sage-summer-camp-2026   # or wherever you cloned your personal repo
mkdir -p brain-exports
cp ~/sage-brain-export.tar.gz brain-exports/
git add brain-exports/sage-brain-export.tar.gz
git commit -m "Add Hermes sage brain export"
git push
```

5. **Instructors will pull from your repo**, extract shareable knowledge, and open PRs into [`hermes-profile/`](hermes-profile/) on your behalf.

### How to contribue [Claude Code]

Claude Code has no `hermes profile export`. Build a redacted `claude_backup/` folder from transcripts and Sage-related skills, then upload it to your personal repo.

1. **Create the backup folders:**

```bash
mkdir -p ~/claude_backup/transcripts ~/claude_backup/skills
```

2. **Export chat transcripts** from each useful Claude Code session (camp debugging, skill work, recipes worth keeping). In Claude Code:

```text
/export ~/claude_backup/transcripts/<short-name>.md
```

Pass a path so the file lands under `claude_backup/transcripts/` (without a path, `/export` opens a menu for clipboard or a local save). Repeat for each session worth contributing.

3. **Collect Sage-related skills.** In a Claude Code session, paste this prompt:

```text
Use your shell tool to find all sage-related skill files in ~/.claude/skills/ and ./.claude/skills/.
Read their contents and copy them into ~/claude_backup/skills/, preserving each skill's directory structure.
Skip unrelated skills. If a skill is a symlink, copy the real files (not the symlink alone).
```

4. **Redact secrets.** Still in Claude Code, paste this prompt:

```text
Look through ~/claude_backup/. Scan all transcripts and skill files for sensitive data
such as API keys, passwords, tokens, private URLs with credentials, or .env contents.
Replace each secret with [REDACTED] so this folder is safe to commit.
Do not delete useful debugging content — only redact secrets.
```

5. **Spot-check**, then package the backup:

```bash
# Quick sanity check — should find nothing that looks like a live key
rg -n 'sk-|api[_-]?key|token|password|Bearer ' ~/claude_backup || true

tar -czf ~/claude-brain-export.tar.gz -C ~ claude_backup
```

6. **Upload the tarball** to your personal `sage-summer-camp-2026` repo (not the shared camp repo):

```bash
cd ~/sage-summer-camp-2026   # or wherever you cloned your personal repo
mkdir -p brain-exports
cp ~/claude-brain-export.tar.gz brain-exports/
git add brain-exports/claude-brain-export.tar.gz
git commit -m "Add Claude Code brain export"
git push
```

7. **Instructors will pull from your repo**, extract shareable knowledge, and open PRs into [`hermes-profile/`](hermes-profile/) on your behalf.

## Same-machine backup (profile export/import)

Use `export`/`import` to snapshot or restore a profile **on your own machine** — for example before a risky config change, or to duplicate a profile under a new name. This is **not** the recommended way to share with teammates.

**Export:**

```bash
hermes profile list
hermes profile export sage -o ~/sage-backup.tar.gz
```

**Restore on the same machine:**

```bash
hermes profile import ~/sage-backup.tar.gz --name sage-restored
hermes profile use sage-restored
hermes doctor
```

**After import:**

- Reconfigure API keys in `.env` if needed (credentials are not included in exports)
- Run `hermes doctor`

## Comparison

| | `profile install` / `update` | `profile export` / `import` |
| --- | --- | --- |
| Use case | Team sharing, new Thor, new machine | Local backup (same machine only) |
| Share with teammates or other machines? | **Yes** (via git) | No |
| Scope | Distribution config (SOUL, skills, tools) | One profile + memories/sessions |
| Credentials | No — each user fills `.env` | Stripped |
| Format | git / local dir | `.tar.gz` |

---

# Inference options compared

Hermes always **runs on your Thor** (files, terminal, tools). What changes is **where the LLM lives**. The camp profile is wired so you can switch among these.

## 1. Local model on the Thor (Ollama) — Part 1

Run inference **on the same machine** as Hermes via Ollama (camp default often `gemma4:31b`).

- **Why it’s cool:** True on-device / edge-style agent — no cloud LLM required for the chat loop. Great for learning what agentic workflows feel like when the model sits next to the tools and sensors.
- **Tradeoff:** Can feel **slower** than frontier cloud APIs, especially on large models or long context. Shared GPU with classmates.
- **When it shines:** Smaller or coding-oriented models that fit local VRAM; offline-ish experiments; understanding edge constraints before you rely on the cloud.

Setup: [Part 1 — Thor + Ollama](#part-1-thor--ollama). Switch later with `hermes model` → **`local-sage-thor`**.

## 2. Big frontier models at NVIDIA (hosted APIs) — Part 2

Send prompts from the Thor to **NVIDIA Build** over HTTPS — among the largest / fastest hosted models available to camp.

- **Why it’s cool:** Frontier-class capability without filling Thor VRAM.
- **Tradeoff:** Rate limits apply (plan around about **40 requests per minute** — don’t hammer the API in tight loops). Needs `NVIDIA_API_KEY` and internet from the Thor.
- **When it shines:** Hard reasoning, big coding tasks, when local Ollama is too slow or too small.

Setup: [Part 2 — NVIDIA Hosted APIs](#part-2-nvidia-hosted-apis).

## 3. Hosted LLMs at NRP — Part 2B

Use **NRP Managed LLMs** (`https://ellm.nrp-nautilus.io/v1`) — NSF research infrastructure. Camp default model: **`minimax-m2`** (others like `gpt-oss`, `qwen3`, `gemma` are in the [NRP catalog](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/)).

- **Why it’s cool:** Strong open-weights models with a research fair-use policy; good middle path between “local only” and “NVIDIA frontier.”
- **Tradeoff:** Needs an NRP LLM token (`NRP_LLM_API_KEY`) and group LLM access; concurrency / fair-use limits apply (see [token economy](#token-economy)).
- **When it shines:** Longer coding / agentic sessions on NRP models without burning NVIDIA request budget.

Setup: [Part 2B — NRP Managed LLMs](#part-2b-nrp-managed-llms). Switch with `hermes model` → **`nrp`**.

## 4. Commercial APIs (optional — you pay)

You can also point Hermes at a **paid** provider (OpenAI, Anthropic, OpenRouter, MiniMax direct, etc.) with your own key.

- **Why someone does it:** Specific model not in NRP/NVIDIA catalogs, or personal preference.
- **Tradeoff:** **Real money** per token; you own the billing and keys.
- **When it shines:** Only if you knowingly want that model and accept the cost.

Use `hermes model` / provider setup in the Hermes docs; keep keys in **your** `.env` only.

> **Note:** A Commercial API is not required for this camp. The camp provides free and shared options for all students.

## Quick chooser

| Goal | Prefer |
| ---- | ------ |
| Learn edge-style agents; stay on-box | **1 — Thor + Ollama** |
| Max capability / speed for hard tasks | **2 — NVIDIA Build** (watch rate limits) |
| Strong hosted open models, camp default cloud path | **3 — NRP** (`minimax-m2`) |
| A vendor model you’re willing to pay for | **4 — Commercial API** |

Same Hermes install — swap with `hermes model` ([Switching between approaches](#switching-between-approaches)).

## Detail table

| | 1. Thor + Ollama | 3. NRP Managed LLMs | 2. NVIDIA Hosted APIs | 4. Commercial (optional) |
| --- | --- | --- | --- | --- |
| **Where Hermes runs** | Thor | Thor | Thor | Thor |
| **Where inference runs** | Thor (Ollama, local GPU) | NRP Nautilus (cloud) | NVIDIA Build (cloud) | Vendor cloud (you pay) |
| **Endpoint** | `http://127.0.0.1:11434/v1` | `https://ellm.nrp-nautilus.io/v1` | `https://integrate.api.nvidia.com/v1` | Provider-specific |
| **API key** | Not required | `NRP_LLM_API_KEY` (Bearer token) | `NVIDIA_API_KEY` (`nvapi-...`) | Your paid key in `.env` |
| **Default camp model** | `gemma4:31b` | `minimax-m2` | (user picks from catalog) | (you pick) |
| **Models** | Any Ollama model on the Thor | NRP catalog ([model matrix](https://nrp.ai/documentation/userdocs/ai/llm-managed/models/)) | NVIDIA catalog only | Vendor catalog |
| **Cost / limits** | Shared Thor GPU; may feel slower | NRP fair-use policy | ~**40 requests/min** (plan for it) | Per-token billing |

---

# Switching between approaches

All providers can be configured on the Thor. Switch anytime:

```bash
hermes model
```

Select the appropriate provider:

- **`local-sage-thor`** — 1. Thor + Ollama (`gemma4:31b`)
- **NVIDIA NIM** — 2. NVIDIA Build hosted APIs (rate-limited; ~40 req/min)
- **`nrp`** — 3. NRP Managed LLMs (`minimax-m2` default)
- Other / commercial providers — 4. optional paid APIs (your key, your bill)

---

# Hermes web dashboard

The [Hermes web dashboard](https://hermes-agent.nousresearch.com/docs/user-guide/features/web-dashboard) is a browser UI for sessions, config, skills, and chat. On Thor there is no local browser — keep the dashboard bound to **localhost on the Thor** and open it on your **laptop** through an SSH tunnel.

## 1. Port-forward from your laptop

In a **local** terminal (not on the Thor), forward port `9119`:

```bash
ssh -L 9119:127.0.0.1:9119 your-linux-user@thor-host
```

Leave that SSH session open while you use the dashboard. Optional background tunnel (no remote shell):

```bash
ssh -f -N -L 9119:127.0.0.1:9119 your-linux-user@thor-host
```

## 2. Start the dashboard on the Thor

```bash
# Use the sage profile if that is your active camp profile:
hermes -p sage dashboard --host 127.0.0.1 --port 9119 --no-open
# or, if sage is already the active profile / alias:
hermes dashboard --host 127.0.0.1 --port 9119 --no-open
```

`--no-open` skips trying to launch a browser on the headless Thor.

## 3. Open it on your laptop

In your laptop browser:

```text
http://127.0.0.1:9119 #or http://localhost:9119
```

When finished, stop the dashboard (`Ctrl-C` on the Thor) and close the SSH tunnel.

---

# Token economy

A practical guide for using context, compute, and provider quotas responsibly during summer camp. Covers `/usage`, `/compress`, provider switching costs, and **Thor-specific Ollama context** (why the first turn can take minutes on `gemma4:31b`).

**Full guide:** [token-economy.md](token-economy.md)

**Thor quick fix:** if your first Hermes response takes 3+ minutes, run [Step 4B — Cap Ollama context](#step-4b--cap-ollama-context-recommended) before blaming the agent.

---

# Updating The Knowledge Graph

After adding/changing skills or docs **with a graph already built** → refresh the graph on the **installed** profile (where Hermes actually runs). Create `.venv-graphify` under that path if missing. Hermes CWD is often `$HOME`, so always pass an absolute path.

**Use this path (students / day-to-day agent):**

```text
/graphify ~/.hermes/profiles/sage --update
```

Do **not** point `/graphify` at `…/summer-camp-2026/hermes-profile` for normal updates — that clone is not the live agent home. A graph built only in the repo will not be what `sage` queries.

Full `/graphify ~/.hermes/profiles/sage` again is start-from-scratch only — use `--update` for incremental adds.

To do a code and a llm semantic update then run this on your terminal
```sh
graphify extract ~/.hermes/profiles/sage
```
>NOTE: add [enviroment variables](https://github.com/Graphify-Labs/graphify#environment-variables) to determine which llm endpoint to use. Also the extract command does the incremental updates automatically by analyzing the graphify files. If no graphify files are detected then it will start from scratch.

**Instructors only** — the shipped baseline is **two graphs**, not one:

| Graph | Ignore file | Ships as | Purpose |
|---|---|---|---|
| **curated** | `.graphifyignore.curated` | `graphify-baseline-viz.tar.gz`, `agent-knowledge-graph.html` | Human-readable visualization — deliberately small so the HTML stays legible |
| **full** | `.graphifyignore.full` | `graphify-baseline.tar.gz` | What the agent queries (GraphRAG); far larger, never shipped as the main viz |

`graphify extract` always writes to `<profile>/graphify-out/` and has no
output-directory flag, so building both means swapping directories. Stash the
idle graph **outside** the profile — a sibling such as `graphify-out-full/`
matches no `.graphifyignore` rule and graphify will scan the stashed graph's own
cache as source material.

```bash
# From the distribution checkout (summer-camp-2026/hermes-profile):
STASH="$(mktemp -d)"                       # outside the profile, on purpose
mv graphify-out "$STASH/full"

# curated pass -> viz artifacts
mv graphify-out-viz graphify-out
../scripts/update_hermes_profile_graphify.sh --scope curated
tar -czf graphify-baseline-viz.tar.gz graphify-out
cp graphify-out/graph.html agent-knowledge-graph.html
mv graphify-out graphify-out-viz

# full pass -> query graph
mv "$STASH/full" graphify-out
../scripts/update_hermes_profile_graphify.sh --scope full
tar -czf graphify-baseline.tar.gz graphify-out
rmdir "$STASH"

# Strip the build machine's absolute paths before committing (see below)
../scripts/sanitize_graph_tarball.sh graphify-baseline.tar.gz
../scripts/sanitize_graph_tarball.sh graphify-baseline-viz.tar.gz
INSTALL_ROOT='$HOME/.hermes/profiles/sage' perl -pi -e \
  's{(?:/Users|/home)/[^/\s"]+/[^\s"]*?hermes-profile}{$ENV{INSTALL_ROOT}}g' \
  agent-knowledge-graph.html

git add agent-knowledge-graph.html graphify-baseline.tar.gz graphify-baseline-viz.tar.gz
git commit -m "Update knowledge graph baseline"
git push
```

**Always sanitize before committing.** Graphify records the absolute path of the
directory it extracted, so a freshly packed tarball carries the packager's home
directory in `graphify-out/.graphify_root`, `GRAPH_REPORT.md` (including dated
backup copies) and the `<title>` of `graph.html`.
`scripts/sanitize_graph_tarball.sh` rewrites the cosmetic ones to
`$HOME/.hermes/profiles/sage`, **deletes** `.graphify_root`, and repacks.
Verify with:

```bash
tar -tzf graphify-baseline.tar.gz | grep graphify_root   # -> no output
tar -xzf graphify-baseline.tar.gz -C /tmp/check && grep -rl '/Users/' /tmp/check   # -> no matches
```

**`.graphify_root` is deleted, not rewritten, and the install step must write
it back.** It is a functional file, not a cosmetic one, and there is no portable
value to ship: graphify reads it with `Path(text)` and does no shell expansion,
so a literal `$HOME/...` resolves to a bogus nested path, while a real absolute
path is the packager's machine. So the profile install writes it (see
`hermes-profile/README.md` and `AGENTS.md`):

```bash
printf '%s\n' "$HOME/.hermes/profiles/sage" > graphify-out/.graphify_root
```

Omitting that step is not safe. `graphify update` resolves the marker at
`Path(GRAPHIFY_OUT)/".graphify_root"` where `GRAPHIFY_OUT` defaults to the
*relative* name `graphify-out`, so it is looked up against the **CWD**. With no
marker — or with the CWD anywhere but the profile — it falls back to `Path(".")`
and walks that tree. Measured on a Thor node, 2026-09-03: run from `$HOME` with
no marker it scanned **8,746** files and created a stray `~/graphify-out`; with
a correct absolute marker and the CWD at the profile it scanned the right
**244**. Two rules follow: write the marker at install time, and always invoke
graphify from the profile directory.

Prefer the incremental path above over `--wipe`. `--wipe` deletes `graphify-out/`
*including its semantic cache*, turning a cheap refresh into a full paid
re-extract. The cache stays valid as long as the prompt fingerprint directory
(`graphify-out/cache/semantic/p<fingerprint>/`) is unchanged.

**Caveat on curated coverage.** `.graphifyignore.curated` admits `docs/` and
top-level skill entry points but not `skills/*/references/`. Reference pages
therefore appear only in the full query graph, and `agent-knowledge-graph.html`
will not visibly reflect changes confined to them — profile 1.4.0's skill split
moved bulk into 11 routed `pitfalls-*.md` reference pages, so the published
visualization gained only the new `docs/` entries even though the agent's
queryable knowledge grew substantially. This is the intended trade-off: widening
the curated scope to cover `references/` would make the HTML unreadable. If a
change needs to show up in the visualization, it has to land in `docs/`.
