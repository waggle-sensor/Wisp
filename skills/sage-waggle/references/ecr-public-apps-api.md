# ECR public apps API — scheduleable plugins catalog

Lists **public** Edge Code Repository (ECR) apps already registered and available to schedule on nodes via SES / `sesctl` (and the portal). An app must appear in this catalog for `sesctl submit` to accept its image — Docker pull alone is not enough (see `sesctl-ecr-validation.md`, `ecr-catalog-api-and-thor-deploy.md`).

**Portal UI:** [portal.sagecontinuum.org/apps](https://portal.sagecontinuum.org/apps)  
**API base:** `https://ecr.sagecontinuum.org/api`

---

## List public apps (camp default)

| | |
|--|--|
| **URL** | `GET https://ecr.sagecontinuum.org/api/apps?public=true` |
| **Auth** | None for public listing |
| **Response** | JSON: `{ "data": [ …apps… ], "pagination": { "continuationToken": … } }` |

```bash
curl -sL "https://ecr.sagecontinuum.org/api/apps?public=true"
```

Optional: `limit` (e.g. `?public=true&limit=2`) for smaller pages.

Verified ~**360+** public app versions in the fleet catalog (sizeable JSON — filter client-side or use `limit` when exploring).

---

## Related GETs

| URL | Notes |
|-----|--------|
| `GET /api/apps` | Broader list (same shape); prefer `?public=true` when you only want scheduleable public plugins |
| `GET /api/apps/<namespace>/<name>` | All public versions for one app → `{ "data": [ … ] }` |
| `GET /api/apps/<namespace>/<name>/<version>` | Single version record (flat object, not wrapped in `data`) |

Example:

```bash
curl -sL "https://ecr.sagecontinuum.org/api/apps/andrewsm/goes-data"
curl -sL "https://ecr.sagecontinuum.org/api/apps/andrewsm/goes-data/0.1.1"
```

Registry image form used in job YAML: `registry.sagecontinuum.org/<namespace>/<name>:<version>` (same as catalog `id` with `:` → path style may vary; `id` is typically `"<namespace>/<name>:<version>"`).

---

## What each app object contains

Useful fields on each `data[]` entry:

| Field | Meaning |
|-------|---------|
| `id` | `"namespace/name:version"` catalog id |
| `namespace`, `name`, `version` | Coordinates of the app |
| `description` | Short human summary |
| `source.url` | GitHub (or other) source repo |
| `source.architectures` | e.g. `linux/arm64`, `linux/amd64` — check **arm64** for Thor |
| `source.dockerfile`, `branch`, `directory` | Build context |
| `inputs` | Declared plugin inputs (CLI/env) when present |
| `keywords`, `authors`, `homepage`, `license` | Metadata (often null) |
| `images` | Portal thumbnail / science-image asset paths (or null) |
| `frozen` | If true, version locked |
| `time_created`, `time_last_updated` | Timestamps |

Use this list to **discover** existing plugins before writing a new one, or to copy `namespace/name:version` into a job YAML for scheduling.

---

## Agent tips

1. “What public plugins can I schedule?” → `GET .../api/apps?public=true`, then narrow by keyword / `name` / arm64 in `source.architectures`.
2. Confirm a specific version before `sesctl submit` → `GET .../api/apps/<ns>/<name>/<ver>` (or list by name).
3. Private / unpublished apps will not show under `public=true` and will fail SES validation with “does not exist in ECR”.
4. Writing new versions needs a portal token (`Authorization: Sage <token>`) — see `ecr-catalog-api-and-thor-deploy.md` and `scripts/register-ecr-version.py`.
