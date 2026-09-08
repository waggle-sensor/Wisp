# GitHub MCP Server

Connect Hermes to GitHub (repos, issues, PRs, Actions, code search) via the official MCP server.

| | |
|--|--|
| **MCP Registry** | <https://github.com/mcp/github/github-mcp-server> |
| **Source / docs** | <https://github.com/github/github-mcp-server> |
| **Remote endpoint** | `https://api.githubcopilot.com/mcp/` |
| **Read-only remote** | `https://api.githubcopilot.com/mcp/readonly` (optional narrower surface) |

What it enables: browse/query repos and files, manage issues and PRs, inspect Actions runs, code analysis helpers — through MCP tools instead of raw `gh`/`curl` to the GitHub API.

---

## Remote server (recommended on Thor)

Hosted by GitHub — no local Docker required.

**Auth:** GitHub **Personal Access Token** as Bearer header (Hermes / most non-VS-Code hosts). Classic or fine-grained PAT with scopes appropriate to what you need (minimum often `repo`; add `read:org` / Actions scopes if required).

Never commit the token. Put it in the profile `.env` (user-owned, not in the distribution).

### Add with Hermes CLI

```bash
# Interactive — paste PAT when prompted for auth, enable tools you want
hermes mcp add github --url "https://api.githubcopilot.com/mcp/"

# Verify
hermes mcp list
```

After adding, start a **new** Hermes session. Tools show up as `mcp_github_*` (names vary by toolset).

### Equivalent config shape

Hermes HTTP MCP entry (conceptually — exact file may be profile `mcp.json` or config after `hermes mcp add`):

```json
{
  "mcp_servers": {
    "github": {
      "url": "https://api.githubcopilot.com/mcp/",
      "headers": {
        "Authorization": "Bearer <GITHUB_PAT>"
      },
      "enabled": true,
      "timeout": 120
    }
  }
}
```

Optional env name used in Wisp docs: `GITHUB_MCP_PAT` or `GITHUB_PERSONAL_ACCESS_TOKEN` — copy into the Bearer header; do not ship real tokens in git.

### Toolsets / headers (advanced)

Remote server supports toolset filtering and modes via URL path or headers (see [remote-server.md](https://github.com/github/github-mcp-server/blob/main/docs/remote-server.md)):

| Mode | Example |
|------|---------|
| Default | `https://api.githubcopilot.com/mcp/` |
| Read-only | `https://api.githubcopilot.com/mcp/readonly` |
| Insiders | `https://api.githubcopilot.com/mcp/insiders` or header `X-MCP-Insiders: true` |

Common toolset groups: `context`, `repos`, `issues`, `pull_requests`, `actions`, `code_security`, `users`, …

---

## Local server (optional)

If remote HTTP is blocked: Docker image `ghcr.io/github/github-mcp-server` with env `GITHUB_PERSONAL_ACCESS_TOKEN`. Prefer remote on event Thors unless Docker is required.

Deprecated: npm `@modelcontextprotocol/server-github` (no longer supported upstream as of 2025).

---

## Event usage tips

1. Prefer GitHub MCP when you need **live** code/PRs/issues from `waggle-sensor`, participant forks, or pywaggle — the skill’s `waggle-sensor-repos-index.md` is a static catalog.
2. Keep Sage MCP (`mcp.sagecontinuum.org`) for nodes/data/jobs; use GitHub MCP for source control; Hugging Face MCP for Hub models/docs.
3. Use least privilege: for read-only browsing, point at `/mcp/readonly` or a PAT with read-only scopes.
4. Re-auth / new session after changing MCP config (same quirk as Sage MCP).

## Security

- Tokens stay in `.env` / Hermes auth store — never in skills, job YAMLs, or this repo.
- Rotate PATs if exposed; revoke at <https://github.com/settings/tokens>.
